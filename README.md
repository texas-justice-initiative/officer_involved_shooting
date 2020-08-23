# TJI's Officer-Invovled Shooting (OIS) Report 2020
TJI has been collecting the datasets about OIS incidents (for both officers and civilians) in Texas since 2015. As of Aug 2020, TJI is finalizing to publish a data journalism report on the OIS incidents in Texas. This repository has the following information about the report:
- Jupyter notebooks for data preprocessing for the OIS datasets and the census datasets
- Jupyter notebooks for all the analyses in the report (Data Summary and Data Insight sections)
- Raw and preprocessed datasets
- Python script used for data preprocessing and visualization

## Data
### Raw
- **Website**: civilian and officer datsets downloaded from the TJI website (downloaded in June 2020).
- **Census**: census (Texas Demographics Center) and mortality (Texas Department of State Health Services) datasets

### Interim
- `OAG_report_summary.csv`: Summary of OAG reports from 2016 to 2019 
- `census_county_race_2010.pkl`: Preprocessed census data for populations by county (using the actual 2010 census data not the annual estimates)
- `census_county_race_age_2010.pkl`: Preprocessed census data for population by race, gender and age

### Preprocessed
Preprocessed civilian and officer datasets both in the csv and pkl formats. See `1.0-hs-preprocess_OIS_data_OIS_report.ipynb` for the details of data preprocessing process.

## Notebooks
- `1.0-hs-preprocess_tx_census_data.ipynb`: Prerocessing of the census data (c.f., the mortality data was scraped from the DSHS website).
- `1.0-hs-preprocess_OIS_data_OIS_report.ipynb`: Preprocessing of the OIS data (both civilian and officer datasets)
- `1.0-hs-data_summary_OIS_report.ipynb`: Analyses for the Data Summary section of the report
- `1.1-hs-data_insight_OIS_report.ipynb`: Analyses for the Data Insight section of the report
- `preprocess.py`: Preprocessing script for all notebooks
- `plot.py`: Visulization script for all figures in the report

## Figures
All image files are created as `eps` files. `Figures_Notebook.zip` has all figures created from the Jupyter notebooks (`/Notebooks`). `Figures_Final.zip` have the final version of the figures that are used in the report. These figures are identical to the notebook figures except for the colors in some.

**Style Guide**: Image styling guide that the graphic designer [Ally Curtis](https://www.alysondesign.com/) created. The data insight and summary notebooks have most of the information in this guide.

Please contact [Hongsup Shin](hongsup.shin@pm.me) for any questions.