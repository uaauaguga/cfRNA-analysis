# How to use
- This pipeline can be easily integrated in exSeek framework
- copy editCalling_pe.snakemake to exSeek/snakemake
- midifiy bin/exseek.py
  - add name of the snakemake file to the steps tuple
  - steps = (
    'quality_control',
    'quality_control_clean',
    'bigwig',
    'editCalling_pe',
    'editCalling_pe_v2',
    'callSNP',
    'mapping_long_pe_v2',
    'count_matrix', 
    'call_domains', 
    'merge_domains',
    'combine_domains',
    'chimericRNA',
    'normalization', 
    'pico_quality_control_pe',
    'feature_selection', 
    'differential_expression', 
    'evaluate_features',
    'igv',
    'overview_pe',
    'mapping_long_pe_UMI',
    'update_sequential_mapping',
    'update_singularity_wrappers')
