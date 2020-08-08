import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
colors_year = plt.get_cmap('magma')(np.linspace(0.5, 1, 5)[::-1][1:])   # default year color

# commonly used variables
race_list = ['WHITE', 'BLACK', 'HISPANIC', 'OTHER']
years = range(2016, 2020)
age_names = np.array(['1-4', '5-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75+'])
incident_causes_list = ['Emergency/Request for Assistance', 'Other', 'Traffic Stop',
                        'Execution of a Warrant', 'Hostage/Barricade/Other Emergency']
incident_causes_list_print = ['Emergency/Request\nfor Assistance', 'Other', 'Traffic Stop',
                              'Execution of\na Warrant',
                              'Hostage/Barricade/\nOther Emergency']


def plot_stackedbar_year_county(df, title, total_count=False, n_county=10,
                                figsize=(7, 4), colors=None, fname=None, fontsize=10,
                                bbox_to_anchor=(1.1, 1)):

    """
    Create a horizontal stacked bar plot of the no. of incidents by county and by year (stacked)
    :param pd.DataFrame df: dataset
    :param str title: figure title
    :param bool total_count: whether to show the total count with yticklabels
    :param int n_county: no. counties show on the y axis
    :param tuple figsize: figure size
    :param list or np.array colors: figure colors
    :param str fname: path name for saving (if not None, it saves)
    :param int fontsize: figure text fontsize
    :param tuple bbox_to_anchor: location of figure legend
    :return: matplotlib figure
    """

    if colors is None:
        colors = colors_year

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # select the counties to show on the y axis (descending order based on its total counts)
    inds_in_order = df['incident_county'].value_counts()[:n_county][::-1].index

    # compute the counts and slice the data based on the counties to show
    df_year_county = df.groupby(['incident_county', 'year'])['date_incident']\
        .count().unstack().fillna(0)
    df_year_county_plot = df_year_county[::-1].loc[inds_in_order, :]

    # plotting
    df_year_county_plot.plot(kind='barh', stacked=True, width=0.75, ax=ax,
                             color=colors, legend=False)
    annotate(ax, 'h', threshold=0, fontsize=fontsize)
    ax.set(xlabel='')
    ax.set_title(title, fontsize=fontsize)

    # add total number of incidents to the yticklabels
    if total_count:
        ax.set_yticklabels(
            [s + ' ({})'.format(int(n))
             for s, n in zip(df_year_county_plot.index, df_year_county_plot.sum(axis=1))],
            fontsize=fontsize)

    fig.tight_layout()
    fig.legend(years, ncol=1, bbox_to_anchor=bbox_to_anchor, fontsize=fontsize)
    
    if fname is not None:
        fig.savefig(fname, bbox_inches='tight')    
        
        
def plot_pie(df, col, figsize=(4, 4), fontsize=10, colors=None,
             fname=None, remove_labels=False, title=None, bbox_to_anchor=(0.75, 0.1)):

    """
    Create a donut plot of the no. of incidents either by gender or race
    :param pd.DataFrame df: dataset
    :param str col: column to visualize (gender or race)
    :param tuple figsize:
    :param str fontsize:
    :param list or np.array colors:
    :param str fname:
    :param bool remove_labels: if True, each segment of the plot reveals its label
    :param str title:
    :param tuple bbox_to_anchor:
    :return: matplotlib figure
    """

    if colors is None:
        colors = colors_year
    wedge_size = 0.5    # if it's 0 it becomes a pie plot (not a donut)

    # compute the counts
    counts = df[col].value_counts()
    total = sum(counts)
    if 'race' in col:
        counts = counts.loc[race_list]  # rearrange the rows for consistency

    fig, ax = plt.subplots(1, 1, figsize=figsize)

    if not remove_labels:
        # show the counts and % within the chart
        def my_fmt(x):
            # function that computes percentage
            return '{:.1f}%\n({:.0f})'.format(x, total*x/100)
        _, texts, autotexts = ax.pie(counts, labels=counts.index, autopct=my_fmt, colors=colors,
                                     wedgeprops=dict(width=wedge_size, edgecolor='w'))
        for autotext, text in zip(autotexts, texts):
            autotext.set_fontsize(fontsize)
            text.set_fontsize(fontsize)
    else:
        ax.pie(counts, startangle=90, labels=None, colors=colors,
               wedgeprops=dict(width=wedge_size, edgecolor='w'))
        pct_counts = counts/counts.sum()*100

        # if we don't show the labels within the chart, then count and % are shown in the legend
        legend_txt = ['{:.1f}% {}'.format(n, s.capitalize())
                      for s, n in zip(counts.index, pct_counts)]
        fig.legend(legend_txt, ncol=counts.shape[0], bbox_to_anchor=bbox_to_anchor, fontsize=10)

    ax.set_title(title, fontsize=fontsize)
    fig.tight_layout()
    if fname is not None:
        fig.savefig(fname, bbox_inches='tight')                


def plot_heatmap_county_race_year(df, df_type='civilian', n_county=10, total_count_yticks=True,
                                  total_count_cols=True, total_count_xticks=True,
                                  figsize=(12, 3.5),
                                  cmap='viridis',
                                  annot_fontsize=10, 
                                  title=None,
                                  fontsize=10,
                                  fname=None):

    """
    Create a heatmap of no. incidents by year (subplot), race (xticks), and county (yticks)
    :param pd.DataFrame df: dataset
    :param str df_type: 'civilian' or 'officer' type
    :param int n_county: no. counties on the y axis
    :param bool total_count_yticks: if True, show the total counts across all subplots with yticks
    :param bool total_count_cols: if True, show the total counts in a year with title
    :param bool total_count_xticks: if True, show the total counts across all rows with xticks
    :param tuple figsize:
    :param str cmap: matplotlib colormap name
    :param int annot_fontsize: fontsize of the annotated text in the heatmap
    :param title:
    :param fontsize:
    :param fname:
    :return: matplotlib figure
    """

    assert df_type == 'civilian' or 'officer'

    # select the counties to visualize based on the total number of incidents
    topN = df['incident_county'].value_counts()[:n_county].index
    gb = df.groupby(['year', df_type + '_race', 'incident_county'])
    vmax = gb['date_incident'].count().max()
    
    fig, axes = plt.subplots(1, len(years), figsize=figsize, sharey=True)
    for i, (ax, year) in enumerate(zip(axes, years)):

        # compute the count for each year, by county and by race
        temp = gb['date_incident'].count().unstack().loc[year].loc[:, topN].T

        # if there are no incidents from certain race groups in a county, that rows are missing.
        # this should be resolved for visualization. Thus, we add nan in this case.
        # nans are visualized as a gray cell in the heatmap.
        missing_races = set(race_list) - set(temp.columns)
        if len(missing_races) > 0:
            for missing_race in missing_races:
                temp[missing_race] = np.nan
        temp = temp[race_list]
        sns.heatmap(temp, annot=True, annot_kws={"size": annot_fontsize}, cbar=False, fmt='.3g',
                    cmap=cmap, vmin=0, vmax=vmax, ax=ax)
        ax.set(ylabel='', xlabel='')
        
        if total_count_cols:
            ax.set_title('{} ({})'.format(year, int(temp.sum().sum())), fontsize=fontsize)
        else:
            ax.set_title(year, fontsize=fontsize)
        if total_count_xticks:
            ax.set_xticklabels([s + '\n({})'.format(int(n))
                                for s, n in zip(race_list, temp.sum(axis=0))], rotation=0)
        else:
            ax.set_xticklabels(race_list, rotation=0)
    if total_count_yticks:
        temp = gb['date_incident'].count().unstack().loc[:, topN].T
        axes[0].set_yticklabels([s + ' ({})'.format(int(n))
                                 for s, n in zip(temp.index, temp.sum(axis=1))])

    fig.suptitle(title, x=0.5, y=1.05)
    fig.tight_layout()
    if fname is not None:
        fig.savefig(fname, bbox_inches='tight')                

        
def plot_heatmap_age_race_year(df, total_count_yticks=True, total_count_cols=True,
                               total_count_xticks=True,
                               figsize=(12, 3), 
                               cmap='viridis',
                               fontsize=10,
                               annot_fontsize=10, 
                               title=None,
                               fname=None):

    """
    Create a heatmap of no. of incidents by year (column), race (xticks) and age groups (yticks)
    :param pd.DataFrame df: dataset
    :param bool total_count_yticks: if True, show the total counts across all subplots with yticks
    :param bool total_count_cols: if True, show the total counts in a year with title
    :param bool total_count_xticks: if True, show the total counts across all rows with xticks
    :param tuple figsize:
    :param str cmap:
    :param int fontsize:
    :param int annot_fontsize:
    :param str title:
    :param str fname:
    :return: matplotlib figure
    """

    gb = df.groupby(['year', 'civilian_race', 'civilian_age_binned'])
    vmax = gb['date_incident'].count().max()
    
    fig, axes = plt.subplots(1, len(years), figsize=figsize, sharey=True)
    for i, (ax, year) in enumerate(zip(axes, years)):

        temp = gb['date_incident'].count().unstack().loc[year]

        # Filling in the missing age groups for visualization consistency
        missing_ages = set(range(len(age_names))) - set(temp.columns)
        if len(missing_ages) > 0:
            for missing_age in missing_ages:
                temp[missing_age] = np.nan
            temp = temp[range(len(age_names))]
        temp = temp.T.loc[range(len(age_names)), :]

        # if there are no incidents from certain race groups in a county, that rows are missing.
        # this should be resolved for visualization. Thus, we add nan in this case.
        # nans are visualized as a gray cell in the heatmap.
        missing_races = set(race_list) - set(temp.columns)
        if len(missing_races) > 0:
            for missing_race in missing_races:
                temp[missing_race] = np.nan
        temp = temp[race_list]

        sns.heatmap(temp, annot=True, annot_kws={"size": annot_fontsize}, cbar=False, fmt='.3g', 
                    cmap=cmap, vmin=0, vmax=vmax, ax=ax)
        ax.set(ylabel='', xlabel='')

        if total_count_cols:
            ax.set_title('{} ({})'.format(year, int(temp.sum().sum())), fontsize=fontsize)
        else:
            ax.set_title(year, fontsize=fontsize)
        if total_count_xticks:
            ax.set_xticklabels([s + '\n({})'.format(int(n))
                                for s, n in zip(race_list, temp.sum(axis=0))], rotation=0)
        else:
            ax.set_xticklabels(race_list, rotation=0)
    if total_count_yticks:
        temp = df['civilian_age_binned'].value_counts().sort_index().to_frame().T
        missing_ages = set(range(len(age_names))) - set(temp.columns)
        if len(missing_ages) > 0:
            for missing_age in missing_ages:
                temp[missing_age] = np.nan
            temp = temp[range(len(age_names))]
        temp = temp.T.loc[range(len(age_names)), :].fillna(0)
        axes[0].set_yticklabels([s + ' ({})'.format(int(n))
                                 for s, n in zip(age_names, temp['civilian_age_binned'])],
                                rotation=0)

    axes[0].set_ylabel('Age Groups')
    fig.suptitle(title, x=0.5, y=1.05)
    fig.tight_layout()
    if fname is not None:
        fig.savefig(fname, bbox_inches='tight')
        

def plot_heatmap_age_race_cause(df, total_count_yticks=True,
                                total_count_cols=True, total_count_xticks=True,
                                figsize=(14, 3), 
                                cmap='viridis',
                                annot_fontsize=10,
                                age_interest=np.array(['15-24', '25-34',
                                                       '35-44', '45-54', '55-64']),
                                fontsize=10,
                                title=None,
                                fname=None):

    """
    Create a heatmap of no. of incidents by incident cause (column),
    race (x axis), and age groups (y axis)
    :param pd.DataFrame df: dataset
    :param bool total_count_yticks: if True, show the total counts across all subplots with yticks
    :param bool total_count_cols: if True, show the total counts in a year with title
    :param bool total_count_xticks: if True, show the total counts across all rows with xticks
    :param tuple figsize:
    :param str cmap:
    :param int annot_fontsize:
    :param list or np.array age_interest: subset of age groups that we want to visualize
    :param int fontsize:
    :param str title:
    :param str fname:
    :return: matplotlib figure
    """

    # find the index of the age groups that we are interested in
    age_interest_inds = np.array([np.argwhere(age == age_names) for age in age_interest]).ravel()
    # compute the counts
    gb = df.groupby(['civilian_age_binned', 'civilian_race'])[incident_causes_list].sum()

    fig, axes = plt.subplots(1, len(incident_causes_list), figsize=figsize, sharey=True)
    for i, (ax, incident_cause) in enumerate(zip(axes, incident_causes_list)):
        
        temp = (gb[incident_cause].unstack())[:-1]
        vmax = temp.max().max()

        # filling in the missing race and age groups
        missing_races = set(race_list) - set(temp.columns)
        if len(missing_races) > 0:
            for missing_race in missing_races:
                temp[missing_race] = np.nan
        temp = temp[race_list]
        missing_ages = set(age_interest_inds) - set(temp.index)
        if len(missing_ages) > 0:
            for missing_age in missing_ages:
                temp = temp.T
                temp[missing_age] = np.nan
                temp = temp.T.sort_index()
        temp = temp.loc[age_interest_inds, race_list]
        temp.index = age_interest
        temp = temp.replace(0, np.nan)  # nan (non existing data = 0) is shown as gray

        sns.heatmap(temp, annot=True, annot_kws={"size": annot_fontsize}, cbar=False, fmt='.3g', 
                    cmap=cmap, vmin=0, vmax=vmax, ax=ax)
        ax.set(ylabel='', xlabel='')

        if total_count_cols:
            ax.set_title('{} ({})'.format(incident_causes_list_print[i], int(temp.sum().sum())),
                         fontsize=fontsize)
        else:
            ax.set_title(incident_causes_list_print[i], fontsize=fontsize)
        if total_count_xticks:
            ax.set_xticklabels([s + '\n({})'.format(int(n))
                                for s, n in zip(race_list, temp.sum(axis=0))], rotation=0)
        else:
            ax.set_xticklabels(race_list, rotation=0)
    if total_count_yticks:
        temp = df['civilian_age_binned'].value_counts().sort_index()[:-1].loc[age_interest_inds]
        axes[0].set_yticklabels([s + ' ({})'.format(int(n))
                                 for s, n in zip(age_interest, temp)], rotation=0,
                                fontsize=fontsize)
    
    fig.suptitle(title, x=0.5, y=1.05)
    fig.tight_layout()
    if fname is not None:
        fig.savefig(fname, bbox_inches='tight')        
        
        
def plot_stackedbar_compare_ratio(df_ratio, df_ref_ratio, df_total,
                                  figsize=(12, 6), severity='Shot', legend=True, fname=None):
    
    # plot horizontal stacked bar side by side
    # to compare the general population (df_ref_ratio: ratio) and the data of interest (df: count)
    
    assert np.equal(df_ratio.index.values, df_ref_ratio.index.values).sum() == df_ratio.shape[0]
    
    cols_race = ['#CE2827', '#3167AE', '#4C5151', '#B8BAB9']
    
    df_ratio = df_ratio.copy()
    df_ref_ratio = df_ref_ratio.copy()
    
    # compute the ratio for df (df_ref should be)
    if df_ratio.index.dtype == 'object':
        df_ratio.index = [s[0] + s[1:].lower() for s in df_ratio.index]
        df_ref_ratio.index = [s[0] + s[1:].lower() for s in df_ref_ratio.index]

    # plotting
    fig, axes = plt.subplots(1, df_ratio.shape[0], figsize=figsize, sharey=True)
    for i, (ax, ind) in enumerate(zip(axes, df_ratio.index)):
        
        # ind should be string
        df_temp = pd.concat([df_ref_ratio.loc[ind, :], df_ratio.loc[ind, :]], axis=1).T
        ax = df_temp.plot(kind='bar', stacked=True, ax=ax, legend=False, ylim=(0, 100),
                          width=0.75, color=cols_race)
        ax.set_title((str(ind) + ' ({})'.format(df_total.values[i])).upper(), fontsize=10)
        if severity == 'Deaths':
            ax.set_xticklabels(['County\nDeaths', 'Deaths\nby OIS'], rotation=0, fontsize=10)
        elif severity == 'Shot':
            ax.set_xticklabels(['Population', 'Civilian\n' + severity], rotation=0, fontsize=10)
        
        if legend:
            if i == len(df_ratio.index)-1:
                ax.legend(df_ratio.columns, ncol=1, bbox_to_anchor=(0, 0), loc='lower left',
                          fontsize='medium')

        # text annotation
        for p in ax.patches:
            width, height = p.get_width(), p.get_height()
            x, y = p.get_xy() 
            if height > 0:
                ax.text(x+width/2, y+height/2, '{:.1f}%'.format(height), color='white', fontsize=10,
                        horizontalalignment='center', verticalalignment='center')        
    fig.tight_layout()
    
    if fname is not None:
        fig.savefig(fname)


def annotate(ax, direction='v', unit='num', color='white', fontsize=10, threshold=0):

    """
    Add text to matplotlib bar graphs
    :param matplotlib.axes._subplots.AxesSubplot ax: matplotlib ax
    :param str direction: 'v' for vertical 'h' for horizontal bar plot
    :param str unit: 'num' for absolute counts, 'percent' for percentage
    :param str or np.array color: color of the annotated text
    :param int fontsize:
    :param int threshold: annotation happens when the number is larger than the threshold
    (if it's 0, it shows all positive numbers)
    :return: same matplotlib ax but with annotation
    """
    
    if unit == 'num':
        s = '{:.0f}'
    elif unit == 'percent':
        s = '{:.1f}%'
    else:
        raise ValueError('unit should be "num" or "percent"')
    
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        
        if direction == 'v':
            target = height
        elif direction == 'h':
            target = width
        else:
            raise ValueError('direction should be "v" or "h"')
            
        if target > threshold:
            ax.text(x+width/2, y+height/2, s.format(target), color=color, fontsize=fontsize,
                    horizontalalignment='center', verticalalignment='center')