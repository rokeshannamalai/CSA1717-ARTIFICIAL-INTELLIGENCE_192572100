# Article Review companion code
# Academic analysis only; no patient data are used.
article = {
    "title": "Reinforcement learning assisted oxygen therapy for COVID-19 patients under intensive care",
    "authors": "Hua Zheng, Jiahao Zhu, Wei Xie, Judy Zhong",
    "year": 2021,
    "doi": "10.1186/s12911-021-01712-6",
    "dataset_size": 1372,
    "algorithm": "Deep Deterministic Policy Gradient (DDPG)"
}

results = {
    "standard_care_mortality_percent": 7.94,
    "rl_mortality_percent": 5.37,
    "absolute_reduction_percentage_points": 2.57,
    "oxygen_reduction_l_per_min": 1.28
}

print("ARTICLE:", article["title"])
print("AUTHORS:", article["authors"])
print("DOI:", article["doi"])
print("DATASET:", article["dataset_size"], "critically ill COVID-19 patients")
print("ALGORITHM:", article["algorithm"])
print("\nREPORTED RESULTS")
for k,v in results.items():
    print(k, "=", v)

print("\nCRITICAL EVALUATION")
print("Retrospective observational data -> possible confounding.")
print("Cross-validation is useful but external/prospective validation is needed.")
print("Recommended extension: multi-hospital external validation + safety constraints.")
