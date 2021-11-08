# Directly download tasks when not available in HF Datasets, or HF Datasets version
#   is not suitable
SQUAD_TASKS = {"squad_v1", "squad_v2"}
DIRECT_SUPERGLUE_TASKS_TO_DATA_URLS = {
    "wsc": "https://dl.fbaipublicfiles.com/glue/superglue/data/v2/WSC.zip",
    "multirc": "https://dl.fbaipublicfiles.com/glue/superglue/data/v2/MultiRC.zip",
    "record": "https://dl.fbaipublicfiles.com/glue/superglue/data/v2/ReCoRD.zip",
}

OTHER_DOWNLOAD_TASKS = {
    "abductive_nli",
    "arct",
    "fever_nli",
    "swag",
    "qamr",
    "qasrl",
    "newsqa",
    "mctaco",
    "mctest160",
    "mctest500",
    "mrqa_natural_questions",
    "mutual",
    "mutual_plus",
    "piqa",
    "winogrande",
    "ropes",
    "acceptability_definiteness",
    "acceptability_coord",
    "acceptability_eos",
    "acceptability_whwords",
    "senteval_bigram_shift",
    "senteval_coordination_inversion",
    "senteval_obj_number",
    "senteval_odd_man_out",
    "senteval_past_present",
    "senteval_sentence_length",
    "senteval_subj_number",
    "senteval_top_constituents",
    "senteval_tree_depth",
    "senteval_word_content",
}

DIRECT_DOWNLOAD_TASKS = set(
    list(SQUAD_TASKS) + list(DIRECT_SUPERGLUE_TASKS_TO_DATA_URLS) + list(OTHER_DOWNLOAD_TASKS)
)

base_hf_datasets_tasks = {
    "snli",
    "commonsenseqa",
    "hellaswag",
    "cosmosqa",
    "socialiqa",
    "scitail",
    "quoref",
    "adversarial_nli_r1",
    "adversarial_nli_r2",
    "adversarial_nli_r3",
    "arc_easy",
    "arc_challenge",
    "race",
    "race_middle",
    "race_high",
    "quail",
}

hendrycks_test_tasks = ['abstract_algebra', 'anatomy', 'astronomy', 'business_ethics', 'clinical_knowledge', 'college_biology', 'college_chemistry', 'college_computer_science', 'college_mathematics', 'college_medicine', 'college_physics', 'computer_security', 'conceptual_physics', 'econometrics', 'electrical_engineering', 'elementary_mathematics', 'formal_logic', 'global_facts', 'high_school_biology', 'high_school_chemistry', 'high_school_computer_science', 'high_school_european_history', 'high_school_geography', 'high_school_government_and_politics', 'high_school_macroeconomics', 'high_school_mathematics', 'high_school_microeconomics', 'high_school_physics', 'high_school_psychology', 'high_school_statistics', 'high_school_us_history', 'high_school_world_history', 'human_aging', 'human_sexuality', 'international_law', 'jurisprudence', 'logical_fallacies', 'machine_learning', 'management', 'marketing', 'medical_genetics', 'miscellaneous', 'moral_disputes', 'moral_scenarios', 'nutrition', 'philosophy', 'prehistory', 'professional_accounting', 'professional_law', 'professional_medicine', 'professional_psychology', 'public_relations', 'security_studies', 'sociology', 'us_foreign_policy', 'virology', 'world_religions']
hendrycks_test_hf_datasets_tasks = {}
for task in hendrycks_test_tasks:
    hendrycks_test_hf_datasets_tasks.update(task + "_val")
    hendrycks_test_hf_datasets_tasks.update(task + "_test")

OTHER_HF_DATASETS_TASKS = base_hf_datasets_tasks.union(hendrycks_test_hf_datasets_tasks)