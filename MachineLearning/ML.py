import os
import pandas as pd


class ML:

    def __init__(self, fileName):
        os.chdir('../DataAquisition/JsonFiles')
        f = open(fileName, 'r')
        str = f.read()
        os.chdir('../../MachineLearning')
        self.pand = pd.read_json(str, orient='index')
        return

    def calculateLaggedInstance(self, lag, targetFeature='liquid_acc_period'):
        # lag = autoregressive lag
        """
        for each day (row) and for a given feature (column) add value for that feature N days
        prior
        For each value of N (1-3 in our case) a new column is added for that feature representing
        the Nth prior day's measurement.
        @pararms:           targetFeature          'precip_acc_period'
        """
        features = self.pand.columns
        for feature in features:
            if feature != 'date':
                for N in range(1, lag + 1):
                    self.deriveNthDayFeature(N, feature)
        # fill any textual values with nans
        self.pand = self.pand.apply(pd.to_numeric, errors='coerce')
        # iterate over the all columns and replace nones by 0
        for feature in features:
            missingVals = pd.isnull(self.pand[feature])
            self.pand[feature][missingVals] = 0
        # drop nans
        self.pand = self.pand.dropna()
        return self.pand

    def deriveNthDayFeature(self, N, feature):
        # total number of rows
        rows = self.pand.shape[0]
        # None values to maintain the constistent rows length for each N
        nth_prior_measurements = [None]*N + [self.pand[feature][i-N] for i in range(N, rows)]
        col_name = "{}_{}".format(feature, N)
        self.pand[col_name] = nth_prior_measurements
        return

    def getPearsonCorrelation(self, targetFeature='liquid_acc_period'):
        print("Remember the following Pearson interpretation:\n0.8 - 1.0: Very Strong\n0.6 - 0." +
              "8: Strong\n0.4 - 0.6: Moderate\n0.2 - 0.4: Weak\n0.0 - 0.2: Very Weak")
        corr = self.pand.corr()[[targetFeature]].sort_values(targetFeature)
        print(corr)
        return


# MLobject = ML('[49, 8]onlyRain.json')
# MLobject.calculateLaggedInstance(3)
# MLobject.getPearsonCorrelation()
