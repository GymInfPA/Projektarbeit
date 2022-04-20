"""
Beinhaltet alle Funktionalitäten in Bezug auf die zu verarbeitenden Daten.

Attribute:
    df: pandas.DataFrame
"""

import pandas as pd
import numpy as np


class DataContainer():
    """Main datastucture is a pandas.DataFrame."""
    
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(filename, sep=None, engine='python')    # pandas DataFrame
        self.__labels = self.df.columns.tolist()

    def get_dimension(self):
        """Return dimension of pandas.DataFrame as a tuple. Index column (i.e. the very first column) does not count."""
        nrows, ncols = self.df.shape
        if ncols > 0:
            ncols -= 1      # Index nicht zählen
        return (nrows, ncols)

    def column_labels(self):
        """Return names of all columns except index column."""
        return self.__labels[1:]

    def index_label(self):
        """Return name of index column."""
        return self.__labels[0]

    def get_row(self, index=0):
        """Return a tuple of all values in a row."""
        return self.df.iloc[index].tolist()

    def get_all_rows(self):
        """Return a list of all tuples of values."""
        return self.df.values.tolist()

    def cormat(self):
        """Return pandas.DataFrame.corr correlation matrix."""
        return self.df.corr()

    def corr_coef(self,x_idx=0, y_idx=1):
        """Return correlation coefficent of y-values given x-values."""
        x_serie = self.df.iloc[:,x_idx+1]
        y_serie = self.df.iloc[:,y_idx+1]
        return x_serie.corr(y_serie)

    def scatter_matrix(self,ax):
        """Plot a scatter_matrix to a given axis."""
        return pd.plotting.scatter_matrix(self.df,ax=ax)

    def descriptions(self):
        """Return a list of pandas.DataFrame description."""
        d = []
        for i in self.df.columns[1:]:
            description = self.df[i].describe(include=[np.number])
            d.append(description.to_list())
        d.insert(0,list(description.keys()))
        df2=pd.DataFrame(d)
        df2=df2.dropna(axis='columns')
        return df2.T.values.tolist()


    def _description(self, col):
        return self.df[col].describe()

    def normalize_col(self, col=0, scale=False, group_by=None):
        """Normalize a given column and add it as new column."""
        if type(col) is int:
            col = self.__labels[col]
        if type(group_by) is int:
            group_by = self.__labels[group_by]

        if scale:
            new_col_label = col + '_ns'
        else:
            new_col_label = col + '_n'

        if group_by is not None:
            grouped = self.df[[group_by,col]].groupby(group_by)
            grouped_means_dict = grouped[col].mean().to_dict()
            grouped_stddev_dict = grouped[col].std(ddof=0).to_dict()
            self.df[new_col_label] = self.df[col]-self.df[group_by].apply(lambda g: grouped_means_dict[g])
            self.df[new_col_label] = self.df[new_col_label]/self.df[group_by].apply(lambda g: grouped_stddev_dict[g])
        else:
            mean = self.df[col].mean()
            if scale:
                stddev = self.df[col].std(ddof=0)
            else:
                stddev = 1
            self.df[new_col_label]= (self.df[col]-mean)/stddev

        self.__labels = self.df.columns.tolist()

        
        

if __name__ == '__main__':
    filename = r'C:\Users\marce\OneDrive - Kantonsschule Olten\Informatik\GymInf\GymInfProjekt\opendata.swiss\envidat_nathaz_fat_wsl_1946-19.csv'
    filename = r'C:\Users\marce\OneDrive - Kantonsschule Olten\Informatik\GymInf\GymInfProjekt\Prototypen\data\COVID19Cases_vs_FullyVaccPersons_202139.csv'
    data = DataContainer(filename)
    rows, cols = data.get_dimension()
    print(f'{rows} rows x {cols} columns')
    print('Index: {}'.format(data.index_label()))
    print(data.column_labels())
    print(data._description(data.column_labels()[0]))
    print(data.descriptions())
