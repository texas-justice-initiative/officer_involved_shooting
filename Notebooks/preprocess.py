import pandas as pd
import numpy as np


def convert_date_cols(df, col_date='date'):

    """
    Convert string format of date to numpy datetime (replace the old columns)
    :param pd.DataFrame df:
    :param str col_date: substring to identify the columns to convert
    :return: dataframe with new replaced columns
    """

    cols_date = df.columns[df.columns.str.contains(col_date)]
    for col in cols_date:
        df[col] = pd.to_datetime(df[col])
    return df


def get_duplicates_from_cols(df, cols_to_use, what_to_keep='first'):

    """
    Check duplicated rows by using the combination of multiple columns
    This is a workaround in the case where one doesn't have unique identifiers for a dataset
    :param pd.DataFrame df:
    :param list cols_to_use: columns to use to create unique combination
    :param str what_to_keep: arguments needed for the duplicated function of pandas,
    decide which instance to keep
    :return:
    """

    # drop na to avoid confusion
    df_non_na = df[cols_to_use].dropna().copy()
    inds_duplicates_to_drop = df_non_na[df_non_na[cols_to_use].duplicated(keep=what_to_keep)].index
    df_duplicates = df.loc[inds_duplicates_to_drop, cols_to_use]
    df_unique = df.drop(index=inds_duplicates_to_drop)

    return df_unique, df_duplicates


def crosstab_by_topN_cities(df, col_interest, col_incident_loc='incident_county',
                            N=5, ratio=False):

    """
    Select top N location(county, city, etc.) based on the total number of incidents
    Sort them by total number (descending) and then compute the crosstab (pd.crosstab)
    for the column of interest (col_interest). df_pop_county has index as county names
    and a single column that shows population of each county
    :param pd.DataFrame df:
    :param str col_interest: column names to visualize
    :param col_incident_loc: colum names that have county (location) information
    :param int N: no. of top counties to compute
    :param bool ratio: if True, normalize the data and return the ratio. Otherwise, integer counts
    :return:
    """

    # get the index of the locations based on its total counts
    topN_loc_indices = df.groupby(col_incident_loc)[col_interest].count().sort_values(
        ascending=False)[:N].index

    # transpose so that our interest becomes columns
    df_crosstab = pd.crosstab(df[col_interest], df.loc[df[col_incident_loc].isin(topN_loc_indices), col_incident_loc]).T
    df_crosstab['TOTAL'] = df_crosstab.sum(axis=1)

    if 'race' in col_interest:
        col_list = ['WHITE', 'BLACK', 'HISPANIC', 'OTHER']

        # some category might be missing
        if df_crosstab.shape[1] < len(col_list)+1:
            missing_cols = list(set(col_list) - set(df_crosstab.columns))
            for col in missing_cols:
                df_crosstab[col] = 0

    else:
        col_list = list(np.sort(df[col_interest].unique()))

    df_crosstab = df_crosstab.loc[:, col_list + ['TOTAL']]

    if ratio:
        df_crosstab = df_crosstab.sort_values(by='TOTAL', ascending=False)
        df_crosstab_ratio = df_crosstab.apply(lambda x: x/x['TOTAL'], axis=1).drop('TOTAL', axis=1)
        return df_crosstab_ratio
    else:
        return df_crosstab.sort_values(by='TOTAL', ascending=False)


def pct(df, axis):

    """
    Compute percentage by normalizing based on the total sum
    :param pd.DataFrame df:
    :param int axis: 0 for rows, 1 for columns
    :return: normalized dataframe
    """

    if axis == 1:
        return df.apply(lambda x: x/df.sum(axis=axis))*100
    if axis == 0:
        return df.apply(lambda x: x/df.sum(axis=axis), axis=1)*100


def count_agencies_by_year_type(df, agency_names, N=5):

    """
    Count the number of agencies by agency type (police, sheriff, and others)
    by year and county.
    :param pd.DataFrame df: officer or civilian dataset
    :param list or np.array agency_names: list of columns that have agency names,
    e.g., 'agency_name_1'
    :param int N: number of counties to visualize
    :return:
    """

    # select the agency names and remove empty values
    df_agency_names = df[agency_names].values.ravel()
    df_agency_names = df_agency_names[~pd.isnull(df_agency_names)]

    # categorize agency names based on substring
    dict_agency_names_all = dict()
    dict_agency_names_all['police'] = [s for s in df_agency_names if 'POLICE' in s]
    dict_agency_names_all['sheriff'] = [s for s in df_agency_names if 'SHER' in s]
    dict_agency_names_all['other'] = [s for s in df_agency_names
                                      if 'POLICE' not in s and 'SHER' not in s]
    # select the top N agencies
    dict_agency_topN = dict()
    for key, val in dict_agency_names_all.items():
        dict_agency_topN[key] = pd.Series(val).value_counts()[:N].index

    # count the agency names by year and focus on the top N agencies
    years = sorted(df['year'].unique())
    df_agency_count = dict()
    for year in years:
        df_year = df[df['year']==year]
        df_agency_names = df_year[agency_names].values.ravel()
        df_agency_names = df_agency_names[pd.isnull(df_agency_names) == False]

        dict_agency_names = dict()
        dict_agency_names['police'] = [s for s in df_agency_names if 'POLICE' in s]
        dict_agency_names['sheriff'] = [s for s in df_agency_names if 'SHER' in s]
        dict_agency_names['other'] = [s for s in df_agency_names if 'POLICE' not in s and 'SHER' not in s]

        dict_results = dict()
        for key, val in dict_agency_names.items():
            temp = pd.Series(val).value_counts()
            temp_topN = temp[temp.index.isin(dict_agency_topN[key])]
            dict_results['n_' + key] = len(np.unique(dict_agency_names[key]))
            dict_results[key + '_top'] = temp_topN

        df_agency_count[year] = dict_results
    df_agency_count = pd.DataFrame(df_agency_count).T

    # Using this information, create a dataframe for plotting
    df_agency_count_plot = dict()
    for key in dict_agency_names.keys(): # agency types
        temp = pd.concat(df_agency_count[key + '_top'].values, axis=1).fillna(0).T
        temp.index = years
        if key is 'police':
            temp.columns = [s.split('POLICE')[0].strip() for s in temp.columns]
        elif key is 'sheriff':
            temp.columns = [s.split('SHER')[0].strip() for s in temp.columns]
        df_agency_count_plot[key] = temp

    return df_agency_count, df_agency_count_plot
