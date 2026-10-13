from s2 import search
qs = ["Illuminating the shadows private supplementary tutoring PISA 2022",
      "Effect of Shadow Education on Hong Kong Student Wellbeing PISA 2018",
      "Heterogeneous Effects of Participation in Shadow Education on Mental Health Taiwan",
      "Mental Health Costs of Shadow Education duration depressive Chinese adolescents",
      "Confronting the shadow education system what government policies for what private tutoring",
      "Shadow education as worldwide curriculum studies",
      "private tutoring sleep time depressive symptoms adolescents",
      "Global patterns of the use of shadow education student family national influences",
      "private tutoring student well-being", "shadow education anxiety", "private tutoring life satisfaction adolescents",
      "PISA 2022 tutoring wellbeing", "PISA 2022 out-of-school lessons anxiety"]
for q in qs:
    print("##", q)
    for w in search(q):
        print(f'  {w["paperId"][:12]} {w.get("year")} c={w.get("citationCount")} | {(w.get("title") or "")[:110]} | {(w.get("externalIds") or {}).get("DOI")}')
