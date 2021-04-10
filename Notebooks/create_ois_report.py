import papermill as pm

# data summary notebook
pm.execute_notebook(
   'Notebooks/1.0-hs-papermill-data_summary.ipynb',
   'Notebooks/1.0-hs-papermill-data_summary_output.ipynb',
   parameters=dict(
       df_cd_filename = 'Data/Preprocessed/civilian_preprocessed_20162020.pkl',
       df_os_filename = 'Data/Preprocessed/officer_preprocessed_20162020.pkl',
       census_filename = 'Data/Interim/census_county_race_2010.pkl',
       years_from = 2016,
       years_to = 2020,
       width_heatmap = 14,
   )
)