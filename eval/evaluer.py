"""Évalue l'agent : chaque question a une réponse de référence calculée en SQL ; l'agent réussit si ce
nombre apparaît dans sa réponse (tolérance 0,5 %, arrondis compris).
Usage : python eval/evaluer.py   ->   eval/resultats.md
"""
import asyncio, json, re, sys, time
from pathlib import Path

from dotenv import load_dotenv

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI.parent))
load_dotenv(ICI.parent / "analyste_bq" / ".env")

from google.adk.runners import InMemoryRunner
from google.cloud import bigquery
from google.genai import types

from analyste_bq.agent import root_agent

NOMBRE = re.compile(r"\d[\d\s  ]*(?:[.,]\d+)?")


def nombres(texte):
    """'52 207,10 €' -> 52207.1 ; tolère espaces fines et virgule décimale."""
    out = []
    for m in NOMBRE.findall(texte):
        s = re.sub(r"[\s  ]", "", m).replace(",", ".")
        try:
            out.append(float(s))
        except ValueError:
            pass
    return out


def trouve(attendu, texte):
    return any(abs(n - attendu) <= max(0.005 * abs(attendu), 0.05) for n in nombres(texte))


async def demander(question):
    r = InMemoryRunner(agent=root_agent, app_name="eval")
    s = await r.session_service.create_session(app_name="eval", user_id="eval")
    sql, reponse = [], ""
    msg = types.Content(role="user", parts=[types.Part(text=question)])
    async for ev in r.run_async(user_id="eval", session_id=s.id, new_message=msg):
        for p in ev.content.parts if ev.content else []:
            if p.function_call and p.function_call.name == "execute_sql":
                sql.append(p.function_call.args.get("query", ""))
            elif p.text and ev.is_final_response():
                reponse += p.text
    return sql, reponse


async def main():
    bq = bigquery.Client(project="portfolio-data-vr", location="EU")
    questions = json.loads((ICI / "questions.json").read_text(encoding="utf-8"))
    lignes, ok = [], 0
    for q in questions:
        attendu = float(list(bq.query(q["sql"]).result())[0][0])
        t0 = time.time()
        for essai in range(3):  # quota gratuit (429) ou modèle saturé (503) : on attend et on réessaie
            try:
                sql, rep = await demander(q["question"])
                break
            except Exception as e:  # après 3 essais : compté comme échec, pas masqué
                sql, rep = [], f"ERREUR : {type(e).__name__} {str(e)[:150]}"
                await asyncio.sleep(65)
        reussi = trouve(attendu, rep)
        ok += reussi
        lignes.append((q, attendu, reussi, round(time.time() - t0, 1), sql, rep))
        print(q["id"], "OK" if reussi else "ÉCHEC", attendu, flush=True)
        await asyncio.sleep(20)  # quota gratuit Gemini (requêtes par minute)

    md = [f"# Résultats de l'évaluation\n\n**{ok} / {len(questions)} réponses justes** "
          f"(modèle `{root_agent.model}`, {time.strftime('%d/%m/%Y')}).\n",
          "| # | Question | Attendu | Résultat | Durée |", "|---|---|---:|:---:|---:|"]
    for q, att, r, d, _, _ in lignes:
        att_fr = f"{att:,.2f}".replace(",", " ").replace(".", ",")
        md.append(f"| {q['id']} | {q['question']} | {att_fr} | {'✅' if r else '❌'} | {d:.0f} s |")
    md.append("\n## Détail\n")
    for q, att, r, d, sql, rep in lignes:
        md += [f"### {q['id']} — {q['question']}\n", f"Attendu : `{att:.2f}` — {'juste' if r else 'faux'}\n",
               "SQL de référence :\n```sql\n" + q["sql"] + "\n```\n",
               "SQL de l'agent :\n```sql\n" + ("\n-- requête suivante\n".join(sql) or "(aucun)") + "\n```\n",
               "Réponse de l'agent :\n\n> " + rep.strip().replace("\n", "\n> ") + "\n"]
    (ICI / "resultats.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{ok}/{len(questions)}")


if __name__ == "__main__":
    assert trouve(52207.1, "CA : 52 207,10 €") and not trouve(52207.1, "51 000 €")  # auto-contrôle du parseur
    asyncio.run(main())
