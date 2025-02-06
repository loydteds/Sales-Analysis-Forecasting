import pandas as pd
import statsmodels.api as sm
import plotly.graph_objs as go

class SalesPerformanceEvaluator:
    def __init__(self, file_path, sub_categories):
        self.file_path = file_path
        self.sub_categories = sub_categories
        self.data = self.load_data()

    def load_data(self):
        """Loads the sales dataset and processes the 'Order Date' column."""
        data = pd.read_excel(self.file_path)
        data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y', errors='coerce')
        data.set_index('Order Date', inplace=True)
        return data

    def resample_sales(self, sub_category_data):
        """Resamples sales data to monthly sales."""
        return sub_category_data['Sales'].resample('ME').sum()

    def perform_seasonal_decomposition(self, monthly_sales):
        """Performs seasonal decomposition on the resampled sales data."""
        return sm.tsa.seasonal_decompose(monthly_sales, model='additive', period=12)

    def process_seasonal_and_residual(self, seasonal, residual):
        """Categorizes seasonal values and processes them."""
        expected_increases, expected_drops = [], []
        recorded_values = {}

        for date, seasonal_value, residual_value in zip(seasonal.index, seasonal, residual):
            if pd.notna(residual_value):
                recorded_values[date.date()] = residual_value
            if seasonal_value < 0:
                expected_drops.append((date.date(), seasonal_value))
            elif seasonal_value > 0:
                expected_increases.append((date.date(), seasonal_value))

        return expected_increases, expected_drops, recorded_values

    def evaluate_performance(self, expected_increases, expected_drops, recorded_values):
        """Evaluates performance based on seasonal expectations."""
        results = {
            "failed_increases": 0,
            "exceeded_increases": 0,
            "failed_drops": 0,
            "exceeded_drops": 0,
        }

        for date, expected_value in expected_increases:
            recorded_value = recorded_values.get(date)
            if recorded_value is not None:
                if expected_value > 0 and recorded_value < expected_value:
                    results["failed_increases"] += abs(expected_value - recorded_value)
                elif expected_value > 0 and recorded_value > expected_value:
                    results["exceeded_increases"] += abs(recorded_value - expected_value)

        for date, expected_value in expected_drops:
            recorded_value = recorded_values.get(date)
            if recorded_value is not None:
                if recorded_value < expected_value:
                    results["failed_drops"] += abs(expected_value - recorded_value)
                elif recorded_value > expected_value:
                    results["exceeded_drops"] += abs(recorded_value - expected_value)

        return results

    def create_performance_plot(self, seasonal, residual, sub_category):
        """Creates a performance plot with seasonal and residual components."""
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=seasonal.index,
            y=seasonal,
            mode='lines',
            name='Seasonal Component',
            line=dict(width=2)
        ))

        fig.add_trace(go.Scatter(
            x=residual.index,
            y=residual,
            mode='lines',
            name='Residual Component',
            line=dict(width=2, dash='dash', color='orange')
        ))

        fig.update_layout(
            title=f'Seasonal and Residual Components for {sub_category}',
            xaxis_title='Date',
            yaxis_title='Value',
            legend_title='Components',
            template='plotly_dark'
        )

        fig.show()

    def evaluate_sub_category(self, sub_category):
        """Evaluates and processes the sales performance for a sub-category."""
        sub_category_data = self.data[self.data['Sub-Category'] == sub_category]
        monthly_sales = self.resample_sales(sub_category_data)
        decomposition = self.perform_seasonal_decomposition(monthly_sales)
        seasonal, residual = decomposition.seasonal, decomposition.resid

        expected_increases, expected_drops, recorded_values = self.process_seasonal_and_residual(seasonal, residual)
        performance_results = self.evaluate_performance(expected_increases, expected_drops, recorded_values)

        # Print evaluation results
        self.print_evaluation_results(sub_category, performance_results)

        # Create plot for seasonal and residual components
        self.create_performance_plot(seasonal, residual, sub_category)

    def print_evaluation_results(self, sub_category, performance_results):
        """Prints the evaluation results for a given sub-category."""
        print(f"\nSales Performance Evaluation for {sub_category}:")
        print(f"Expected Increase but Failed Total: {performance_results['failed_increases']:.2f}")
        print(f"Expected Increase and Exceeded Total: {performance_results['exceeded_increases']:.2f}")
        print(f"Below Expected Drop Total: {performance_results['failed_drops']:.2f}")
        print(f"Expected Drop but Exceeded Total: {performance_results['exceeded_drops']:.2f}")

    def evaluate_all_sub_categories(self):
        """Evaluates performance for all sub-categories."""
        for sub_category in self.sub_categories:
            self.evaluate_sub_category(sub_category)

# Define the sub-categories of interest
sub_categories = ['Bookcases', 'Chairs', 'Labels', 'Tables', 'Storage', 'Furnishings', 
                  'Art', 'Phones', 'Binders', 'Appliances', 'Paper', 'Accessories', 
                  'Envelopes', 'Fasteners', 'Supplies', 'Machines', 'Copiers']

# Define file path
file_path = 'C:\\Users\\loydt\\Downloads\\Projects\\Superstore Sales Dataset.xlsx'

# Initialize evaluator and evaluate all sub-categories
evaluator = SalesPerformanceEvaluator(file_path, sub_categories)
evaluator.evaluate_all_sub_categories()


"""
Sales Performance Evaluation for Bookcases:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 4141.00 | -3528.45 | 7669.45
2015-11-30 | 4388.03 | 971.00 | 3417.03
2016-06-30 | 103.59 | -2760.47 | 2864.05
2016-09-30 | 4141.00 | 3436.51 | 704.49
2016-11-30 | 4388.03 | 269.23 | 4118.81
2017-09-30 | 4141.00 | 379.52 | 3761.48
2017-11-30 | 4388.03 | -952.65 | 5340.68

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2017-06-30 | 103.59 | 259.69 | 156.10
2018-06-30 | 103.59 | 2788.35 | 2684.77

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-07-31 | -117.20 | -163.59 | 46.39
2016-12-31 | -195.33 | -197.36 | 2.03
2017-05-31 | -872.52 | -1482.43 | 609.91
2017-08-31 | -698.70 | -803.82 | 105.12
2017-12-31 | -195.33 | -818.41 | 623.08

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -117.20 | -97.97 | 19.23
2015-08-31 | -698.70 | -254.81 | 443.88
2015-10-31 | -1075.10 | -135.78 | 939.32
2015-12-31 | -195.33 | 1303.34 | 1498.67
2016-01-31 | -1255.13 | 1067.98 | 2323.11
2016-02-29 | -2151.00 | 260.28 | 2411.29
2016-03-31 | -959.48 | 555.90 | 1515.38
2016-04-30 | -1308.15 | -871.99 | 436.17
2016-05-31 | -872.52 | -349.31 | 523.21
2016-07-31 | -117.20 | -163.59 | 46.39
2016-08-31 | -698.70 | 1346.20 | 2044.90
2016-10-31 | -1075.10 | 160.66 | 1235.76
2016-12-31 | -195.33 | -197.36 | 2.03
2017-01-31 | -1255.13 | 375.01 | 1630.14
2017-02-28 | -2151.00 | -580.24 | 1570.77
2017-03-31 | -959.48 | -616.93 | 342.55
2017-04-30 | -1308.15 | 398.72 | 1706.87
2017-05-31 | -872.52 | -1482.43 | 609.91
2017-07-31 | -117.20 | 549.13 | 666.33
2017-08-31 | -698.70 | -803.82 | 105.12
2017-10-31 | -1075.10 | 262.69 | 1337.79
2017-12-31 | -195.33 | -818.41 | 623.08
2018-01-31 | -1255.13 | -1155.42 | 99.72
2018-02-28 | -2151.00 | 607.53 | 2758.53
2018-03-31 | -959.48 | 348.61 | 1308.08
2018-04-30 | -1308.15 | 760.84 | 2068.99
2018-05-31 | -872.52 | 2119.31 | 2991.83

Total for Bookcases:
Expected Increase but Failed Total: 27875.99
Expected Increase and Exceeded Total: 2840.86
Below Expected Drop Total: 1386.53
Expected Drop but Exceeded Total: 31259.05
Sales Performance Evaluation for Chairs:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 4755.73 | 2658.79 | 2096.94
2015-11-30 | 4624.72 | -3881.03 | 8505.75
2015-12-31 | 7635.22 | 3082.19 | 4553.03
2016-05-31 | 633.58 | -1191.84 | 1825.42
2016-09-30 | 4755.73 | -1730.55 | 6486.28
2016-11-30 | 4624.72 | 1821.76 | 2802.96
2016-12-31 | 7635.22 | -3672.19 | 11307.40
2017-05-31 | 633.58 | 345.75 | 287.83
2017-09-30 | 4755.73 | -977.37 | 5733.10
2017-11-30 | 4624.72 | 2010.14 | 2614.58
2017-12-31 | 7635.22 | 540.86 | 7094.36

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2018-05-31 | 633.58 | 796.95 | 163.37

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2017-07-31 | -120.99 | -1768.92 | 1647.93
2017-10-31 | -1.49 | -838.69 | 837.19
2018-04-30 | -1591.50 | -4009.88 | 2418.38

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -120.99 | 104.60 | 225.59
2015-08-31 | -3637.60 | -389.61 | 3248.00
2015-10-31 | -1.49 | 77.05 | 78.55
2016-01-31 | -4115.38 | 910.01 | 5025.39
2016-02-29 | -4075.26 | -261.71 | 3813.55
2016-03-31 | -1645.26 | -471.24 | 1174.02
2016-04-30 | -1591.50 | -138.93 | 1452.57
2016-06-30 | -2461.75 | 221.83 | 2683.59
2016-07-31 | -120.99 | 1615.19 | 1736.18
2016-08-31 | -3637.60 | -658.00 | 2979.60
2016-10-31 | -1.49 | 712.49 | 713.99
2017-01-31 | -4115.38 | -444.17 | 3671.21
2017-02-28 | -4075.26 | -383.15 | 3692.11
2017-03-31 | -1645.26 | 750.22 | 2395.48
2017-04-30 | -1591.50 | 4099.68 | 5691.18
2017-06-30 | -2461.75 | -1536.28 | 925.47
2017-07-31 | -120.99 | -1768.92 | 1647.93
2017-08-31 | -3637.60 | 998.47 | 4636.07
2017-10-31 | -1.49 | -838.69 | 837.19
2018-01-31 | -4115.38 | -514.98 | 3600.41
2018-02-28 | -4075.26 | 595.72 | 4670.98
2018-03-31 | -1645.26 | -328.12 | 1317.14
2018-04-30 | -1591.50 | -4009.88 | 2418.38
2018-06-30 | -2461.75 | 1265.31 | 3727.06

Total for Chairs:
Expected Increase but Failed Total: 53307.65
Expected Increase and Exceeded Total: 163.37
Below Expected Drop Total: 4903.51
Expected Drop but Exceeded Total: 62361.63
Sales Performance Evaluation for Labels:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-07-31 | 15.85 | -56.66 | 72.51
2015-09-30 | 79.77 | 37.38 | 42.39
2015-10-31 | 52.18 | -234.16 | 286.35
2015-11-30 | 318.59 | 1.73 | 316.85
2015-12-31 | 138.08 | 104.63 | 33.45
2016-09-30 | 79.77 | -70.61 | 150.38
2016-11-30 | 318.59 | -374.46 | 693.05
2016-12-31 | 138.08 | 14.32 | 123.76
2017-07-31 | 15.85 | -57.84 | 73.69
2017-09-30 | 79.77 | -13.95 | 93.73
2017-10-31 | 52.18 | -157.79 | 209.97
2017-12-31 | 138.08 | -166.13 | 304.22

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2016-07-31 | 15.85 | 67.31 | 51.46
2016-10-31 | 52.18 | 344.77 | 292.58
2017-11-30 | 318.59 | 325.54 | 6.95

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-08-31 | -60.59 | -140.62 | 80.04
2016-05-31 | -2.88 | -63.06 | 60.18
2016-06-30 | -55.31 | -139.64 | 84.33
2017-03-31 | -0.36 | -197.71 | 197.36
2017-05-31 | -2.88 | -26.89 | 24.00
2018-03-31 | -0.36 | -119.85 | 119.49
2018-06-30 | -55.31 | -83.17 | 27.85

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-08-31 | -60.59 | -140.62 | 80.04
2016-01-31 | -178.96 | -28.92 | 150.04
2016-02-29 | -160.96 | 96.92 | 257.88
2016-03-31 | -0.36 | 270.38 | 270.74
2016-04-30 | -145.43 | -9.05 | 136.37
2016-05-31 | -2.88 | -63.06 | 60.18
2016-06-30 | -55.31 | -139.64 | 84.33
2016-08-31 | -60.59 | -42.31 | 18.28
2017-01-31 | -178.96 | 73.68 | 252.64
2017-02-28 | -160.96 | -5.43 | 155.53
2017-03-31 | -0.36 | -197.71 | 197.36
2017-04-30 | -145.43 | -11.75 | 133.68
2017-05-31 | -2.88 | -26.89 | 24.00
2017-06-30 | -55.31 | 175.63 | 230.94
2017-08-31 | -60.59 | 135.75 | 196.34
2018-01-31 | -178.96 | -91.93 | 87.03
2018-02-28 | -160.96 | -138.67 | 22.30
2018-03-31 | -0.36 | -119.85 | 119.49
2018-04-30 | -145.43 | -26.38 | 119.05
2018-05-31 | -2.88 | 42.77 | 45.65
2018-06-30 | -55.31 | -83.17 | 27.85

Total for Labels:
Expected Increase but Failed Total: 2400.36
Expected Increase and Exceeded Total: 351.00
Below Expected Drop Total: 593.25
Expected Drop but Exceeded Total: 2669.70
Sales Performance Evaluation for Tables:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-08-31 | 394.07 | -1662.63 | 2056.70
2015-09-30 | 876.97 | -217.11 | 1094.08
2015-11-30 | 2781.89 | -1816.98 | 4598.87
2015-12-31 | 6356.49 | -1383.32 | 7739.81
2016-09-30 | 876.97 | 30.59 | 846.38
2016-11-30 | 2781.89 | 301.58 | 2480.32
2016-12-31 | 6356.49 | -2550.50 | 8906.99
2017-09-30 | 876.97 | -253.02 | 1129.99
2017-11-30 | 2781.89 | 1075.86 | 1706.03
2017-12-31 | 6356.49 | 3494.29 | 2862.20

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2016-08-31 | 394.07 | 451.72 | 57.65
2017-08-31 | 394.07 | 771.37 | 377.30

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-06-30 | -617.84 | -1574.12 | 956.28
2017-01-31 | -153.16 | -957.38 | 804.22
2017-10-31 | -796.88 | -2107.76 | 1310.87
2018-01-31 | -153.16 | -1946.87 | 1793.71
2018-06-30 | -617.84 | -951.44 | 333.60

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -1358.41 | -600.81 | 757.60
2015-10-31 | -796.88 | 1694.14 | 2491.02
2016-01-31 | -153.16 | 2464.71 | 2617.87
2016-02-29 | -2732.02 | 128.48 | 2860.51
2016-03-31 | -1466.46 | -699.83 | 766.63
2016-04-30 | -1698.17 | 1044.06 | 2742.23
2016-05-31 | -1586.48 | -1126.69 | 459.80
2016-06-30 | -617.84 | -1574.12 | 956.28
2016-07-31 | -1358.41 | 563.66 | 1922.07
2016-10-31 | -796.88 | -25.93 | 770.95
2017-01-31 | -153.16 | -957.38 | 804.22
2017-02-28 | -2732.02 | -146.30 | 2585.72
2017-03-31 | -1466.46 | 701.37 | 2167.83
2017-04-30 | -1698.17 | -730.06 | 968.11
2017-05-31 | -1586.48 | 2107.00 | 3693.48
2017-06-30 | -617.84 | 2086.02 | 2703.85
2017-07-31 | -1358.41 | -402.39 | 956.02
2017-10-31 | -796.88 | -2107.76 | 1310.87
2018-01-31 | -153.16 | -1946.87 | 1793.71
2018-02-28 | -2732.02 | -421.72 | 2310.30
2018-03-31 | -1466.46 | -441.08 | 1025.38
2018-04-30 | -1698.17 | -753.54 | 944.63
2018-05-31 | -1586.48 | -1419.85 | 166.64
2018-06-30 | -617.84 | -951.44 | 333.60

Total for Tables:
Expected Increase but Failed Total: 33421.37
Expected Increase and Exceeded Total: 434.95
Below Expected Drop Total: 5198.69
Expected Drop but Exceeded Total: 38109.33
Sales Performance Evaluation for Storage:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 3873.13 | 1060.60 | 2812.52
2015-11-30 | 3974.64 | 3595.54 | 379.10
2015-12-31 | 1976.34 | -924.67 | 2901.01
2016-05-31 | 13.06 | -779.08 | 792.14
2016-09-30 | 3873.13 | 1242.50 | 2630.62
2016-11-30 | 3974.64 | -1553.34 | 5527.98
2016-12-31 | 1976.34 | -2465.58 | 4441.92
2017-09-30 | 3873.13 | -2096.96 | 5970.09
2017-11-30 | 3974.64 | -1836.06 | 5810.70
2018-05-31 | 13.06 | -831.29 | 844.35

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2017-05-31 | 13.06 | 1816.51 | 1803.45
2017-12-31 | 1976.34 | 3596.39 | 1620.05

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-08-31 | -559.37 | -1042.52 | 483.15
2016-04-30 | -869.33 | -1080.70 | 211.37
2016-06-30 | -17.82 | -816.18 | 798.35
2017-06-30 | -17.82 | -877.90 | 860.08
2017-08-31 | -559.37 | -1876.13 | 1316.76

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -1073.29 | -470.51 | 602.78
2015-08-31 | -559.37 | -1042.52 | 483.15
2015-10-31 | -608.16 | 614.99 | 1223.15
2016-01-31 | -2534.58 | -678.83 | 1855.74
2016-02-29 | -2631.72 | -379.99 | 2251.73
2016-03-31 | -1542.90 | -84.99 | 1457.91
2016-04-30 | -869.33 | -1080.70 | 211.37
2016-06-30 | -17.82 | -816.18 | 798.35
2016-07-31 | -1073.29 | -860.75 | 212.54
2016-08-31 | -559.37 | 3124.80 | 3684.17
2016-10-31 | -608.16 | -130.37 | 477.78
2017-01-31 | -2534.58 | 298.40 | 2832.98
2017-02-28 | -2631.72 | 1458.44 | 4090.16
2017-03-31 | -1542.90 | 155.11 | 1698.00
2017-04-30 | -869.33 | 466.39 | 1335.72
2017-06-30 | -17.82 | -877.90 | 860.08
2017-07-31 | -1073.29 | 1537.41 | 2610.70
2017-08-31 | -559.37 | -1876.13 | 1316.76
2017-10-31 | -608.16 | -278.48 | 329.68
2018-01-31 | -2534.58 | 586.57 | 3121.15
2018-02-28 | -2631.72 | -872.31 | 1759.41
2018-03-31 | -1542.90 | 136.03 | 1678.93
2018-04-30 | -869.33 | 820.45 | 1689.77
2018-06-30 | -17.82 | 1900.22 | 1918.04

Total for Storage:
Expected Increase but Failed Total: 32110.42
Expected Increase and Exceeded Total: 3423.50
Below Expected Drop Total: 3669.72
Expected Drop but Exceeded Total: 38500.07
Sales Performance Evaluation for Furnishings:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 1101.30 | 650.35 | 450.95
2015-11-30 | 1554.49 | -612.45 | 2166.95
2015-12-31 | 1560.05 | -1051.77 | 2611.82
2016-09-30 | 1101.30 | -1068.03 | 2169.33
2016-11-30 | 1554.49 | 308.05 | 1246.44
2016-12-31 | 1560.05 | -706.34 | 2266.39
2017-04-30 | 290.57 | -1278.98 | 1569.55
2017-09-30 | 1101.30 | 374.71 | 726.59
2017-11-30 | 1554.49 | 261.44 | 1293.05
2018-04-30 | 290.57 | 108.91 | 181.66

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2016-04-30 | 290.57 | 1127.11 | 836.55
2017-12-31 | 1560.05 | 1715.15 | 155.10

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-05-31 | -7.57 | -83.86 | 76.29
2016-10-31 | -512.45 | -600.66 | 88.20
2017-06-30 | -484.56 | -641.39 | 156.83
2018-03-31 | -326.06 | -1062.58 | 736.52
2018-05-31 | -7.57 | -612.08 | 604.51
2018-06-30 | -484.56 | -518.65 | 34.09

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -308.35 | 50.24 | 358.59
2015-08-31 | -821.94 | 642.43 | 1464.37
2015-10-31 | -512.45 | -198.58 | 313.88
2016-01-31 | -768.84 | 374.18 | 1143.02
2016-02-29 | -1276.64 | -196.64 | 1080.00
2016-03-31 | -326.06 | 138.58 | 464.64
2016-05-31 | -7.57 | -83.86 | 76.29
2016-06-30 | -484.56 | 1117.08 | 1601.65
2016-07-31 | -308.35 | 57.13 | 365.48
2016-08-31 | -821.94 | -98.19 | 723.75
2016-10-31 | -512.45 | -600.66 | 88.20
2017-01-31 | -768.84 | 200.73 | 969.57
2017-02-28 | -1276.64 | 480.18 | 1756.82
2017-03-31 | -326.06 | 881.04 | 1207.10
2017-05-31 | -7.57 | 652.98 | 660.55
2017-06-30 | -484.56 | -641.39 | 156.83
2017-07-31 | -308.35 | -150.34 | 158.02
2017-08-31 | -821.94 | -587.20 | 234.73
2017-10-31 | -512.45 | 756.27 | 1268.72
2018-01-31 | -768.84 | -617.88 | 150.96
2018-02-28 | -1276.64 | -326.50 | 950.14
2018-03-31 | -326.06 | -1062.58 | 736.52
2018-05-31 | -7.57 | -612.08 | 604.51
2018-06-30 | -484.56 | -518.65 | 34.09

Total for Furnishings:
Expected Increase but Failed Total: 14682.74
Expected Increase and Exceeded Total: 991.65
Below Expected Drop Total: 1696.44
Expected Drop but Exceeded Total: 16568.44
Sales Performance Evaluation for Art:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 393.84 | -139.95 | 533.79
2015-11-30 | 295.39 | -309.78 | 605.17
2016-04-30 | 52.12 | -95.80 | 147.92
2016-09-30 | 393.84 | 214.08 | 179.75
2016-11-30 | 295.39 | 193.02 | 102.37
2016-12-31 | 396.54 | -13.52 | 410.06
2017-05-31 | 73.32 | -8.99 | 82.31
2017-09-30 | 393.84 | -98.44 | 492.28
2017-11-30 | 295.39 | 92.45 | 202.94
2017-12-31 | 396.54 | -573.32 | 969.86
2018-04-30 | 52.12 | -80.07 | 132.19
2018-05-31 | 73.32 | -106.84 | 180.16

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-12-31 | 396.54 | 562.54 | 166.00
2016-05-31 | 73.32 | 91.52 | 18.20
2017-04-30 | 52.12 | 151.56 | 99.44

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-07-31 | -92.43 | -141.84 | 49.41
2016-06-30 | -116.14 | -165.42 | 49.29
2016-07-31 | -92.43 | -181.28 | 88.84
2016-10-31 | -75.39 | -182.25 | 106.85
2017-06-30 | -116.14 | -279.32 | 163.18

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -92.43 | -141.84 | 49.41
2015-08-31 | -179.03 | -120.62 | 58.41
2015-10-31 | -75.39 | 136.56 | 211.95
2016-01-31 | -285.29 | -52.27 | 233.02
2016-02-29 | -198.97 | 117.96 | 316.93
2016-03-31 | -263.94 | -116.03 | 147.92
2016-06-30 | -116.14 | -165.42 | 49.29
2016-07-31 | -92.43 | -181.28 | 88.84
2016-08-31 | -179.03 | 74.41 | 253.44
2016-10-31 | -75.39 | -182.25 | 106.85
2017-01-31 | -285.29 | -104.36 | 180.93
2017-02-28 | -198.97 | 21.20 | 220.17
2017-03-31 | -263.94 | 27.25 | 291.20
2017-06-30 | -116.14 | -279.32 | 163.18
2017-07-31 | -92.43 | 298.80 | 391.24
2017-08-31 | -179.03 | 21.89 | 200.92
2017-10-31 | -75.39 | 21.38 | 96.77
2018-01-31 | -285.29 | 132.33 | 417.62
2018-02-28 | -198.97 | -163.46 | 35.51
2018-03-31 | -263.94 | 64.46 | 328.41
2018-06-30 | -116.14 | 420.43 | 536.57

Total for Art:
Expected Increase but Failed Total: 4038.79
Expected Increase and Exceeded Total: 283.65
Below Expected Drop Total: 457.57
Expected Drop but Exceeded Total: 4378.57
Sales Performance Evaluation for Phones:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 1194.17 | -3721.95 | 4916.12
2015-12-31 | 3557.15 | -3489.53 | 7046.68
2016-03-31 | 753.58 | -2418.59 | 3172.18
2016-11-30 | 6772.79 | -4898.92 | 11671.70
2016-12-31 | 3557.15 | -255.07 | 3812.21
2017-09-30 | 1194.17 | -13.87 | 1208.05
2017-11-30 | 6772.79 | -4244.84 | 11017.63
2017-12-31 | 3557.15 | 3185.39 | 371.75
2018-03-31 | 753.58 | -1003.96 | 1757.54

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-11-30 | 6772.79 | 8584.55 | 1811.77
2016-09-30 | 1194.17 | 3176.61 | 1982.44
2017-03-31 | 753.58 | 2863.35 | 2109.76

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-08-31 | -315.47 | -544.09 | 228.62
2016-05-31 | -597.22 | -1021.22 | 424.00
2016-06-30 | -319.27 | -1395.44 | 1076.17
2017-08-31 | -315.47 | -1957.13 | 1641.66
2017-10-31 | -304.71 | -2771.53 | 2466.82
2018-05-31 | -597.22 | -2028.22 | 1431.01

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -1369.89 | -1036.52 | 333.37
2015-08-31 | -315.47 | -544.09 | 228.62
2015-10-31 | -304.71 | 2087.49 | 2392.20
2016-01-31 | -2615.46 | -2339.11 | 276.35
2016-02-29 | -3663.73 | -317.45 | 3346.28
2016-04-30 | -3091.95 | 1943.41 | 5035.36
2016-05-31 | -597.22 | -1021.22 | 424.00
2016-06-30 | -319.27 | -1395.44 | 1076.17
2016-07-31 | -1369.89 | 387.25 | 1757.14
2016-08-31 | -315.47 | 1942.01 | 2257.47
2016-10-31 | -304.71 | 124.83 | 429.54
2017-01-31 | -2615.46 | -1516.93 | 1098.53
2017-02-28 | -3663.73 | 135.48 | 3799.20
2017-04-30 | -3091.95 | -177.74 | 2914.21
2017-05-31 | -597.22 | 2490.24 | 3087.45
2017-06-30 | -319.27 | 1073.31 | 1392.58
2017-07-31 | -1369.89 | 90.07 | 1459.97
2017-08-31 | -315.47 | -1957.13 | 1641.66
2017-10-31 | -304.71 | -2771.53 | 2466.82
2018-01-31 | -2615.46 | 3296.84 | 5912.30
2018-02-28 | -3663.73 | -377.23 | 3286.49
2018-04-30 | -3091.95 | -2324.88 | 767.07
2018-05-31 | -597.22 | -2028.22 | 1431.01
2018-06-30 | -319.27 | -237.07 | 82.19

Total for Phones:
Expected Increase but Failed Total: 44973.86
Expected Increase and Exceeded Total: 5903.97
Below Expected Drop Total: 7268.28
Expected Drop but Exceeded Total: 46896.00
Sales Performance Evaluation for Binders:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 4683.01 | 4073.07 | 609.94
2015-12-31 | 4873.90 | -4749.31 | 9623.21
2016-01-31 | 67.72 | -4144.98 | 4212.70
2016-09-30 | 4683.01 | -4552.11 | 9235.12
2016-11-30 | 934.95 | -153.73 | 1088.68
2016-12-31 | 4873.90 | -2267.81 | 7141.71
2017-01-31 | 67.72 | -256.16 | 323.87
2017-04-30 | 42.32 | 14.57 | 27.75
2017-09-30 | 4683.01 | 104.19 | 4578.82
2017-11-30 | 934.95 | -1203.34 | 2138.29
2018-04-30 | 42.32 | -1831.33 | 1873.65

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-11-30 | 934.95 | 982.22 | 47.27
2016-04-30 | 42.32 | 1441.90 | 1399.58
2017-12-31 | 4873.90 | 6642.26 | 1768.36
2018-01-31 | 67.72 | 4026.28 | 3958.56

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-10-31 | -1146.97 | -2759.58 | 1612.60
2017-03-31 | -222.90 | -775.56 | 552.66
2017-06-30 | -1311.21 | -1490.85 | 179.64
2017-08-31 | -1189.83 | -2466.05 | 1276.22
2018-02-28 | -2547.32 | -2682.06 | 134.74
2018-03-31 | -222.90 | -3440.82 | 3217.92
2018-06-30 | -1311.21 | -2871.00 | 1559.79

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -1531.42 | 885.97 | 2417.40
2015-08-31 | -1189.83 | 1711.19 | 2901.02
2015-10-31 | -1146.97 | -2759.58 | 1612.60
2016-02-29 | -2547.32 | 1086.02 | 3633.33
2016-03-31 | -222.90 | 3841.52 | 4064.42
2016-05-31 | -2652.24 | 231.11 | 2883.35
2016-06-30 | -1311.21 | 3987.00 | 5298.21
2016-07-31 | -1531.42 | -345.33 | 1186.10
2016-08-31 | -1189.83 | 380.01 | 1569.84
2016-10-31 | -1146.97 | -461.50 | 685.47
2017-02-28 | -2547.32 | 1221.19 | 3768.51
2017-03-31 | -222.90 | -775.56 | 552.66
2017-05-31 | -2652.24 | 722.77 | 3375.01
2017-06-30 | -1311.21 | -1490.85 | 179.64
2017-07-31 | -1531.42 | -915.50 | 615.92
2017-08-31 | -1189.83 | -2466.05 | 1276.22
2017-10-31 | -1146.97 | 2846.23 | 3993.20
2018-02-28 | -2547.32 | -2682.06 | 134.74
2018-03-31 | -222.90 | -3440.82 | 3217.92
2018-05-31 | -2652.24 | -1328.73 | 1323.51
2018-06-30 | -1311.21 | -2871.00 | 1559.79

Total for Binders:
Expected Increase but Failed Total: 40853.73
Expected Increase and Exceeded Total: 7173.78
Below Expected Drop Total: 8533.58
Expected Drop but Exceeded Total: 46248.87
Sales Performance Evaluation for Appliances:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-10-31 | 22.06 | -1114.06 | 1136.12
2015-11-30 | 2136.76 | -1234.74 | 3371.50
2015-12-31 | 1372.20 | -39.53 | 1411.74
2016-08-31 | 122.05 | -1044.44 | 1166.48
2016-09-30 | 480.78 | -299.34 | 780.12
2016-12-31 | 1372.20 | -990.47 | 2362.68
2017-09-30 | 480.78 | -560.76 | 1041.54
2017-11-30 | 2136.76 | -1797.38 | 3934.14
2017-12-31 | 1372.20 | 771.59 | 600.61

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-08-31 | 122.05 | 543.62 | 421.57
2015-09-30 | 480.78 | 601.68 | 120.91
2016-10-31 | 22.06 | 535.44 | 513.38
2016-11-30 | 2136.76 | 2773.69 | 636.93
2017-08-31 | 122.05 | 242.40 | 120.35
2017-10-31 | 22.06 | 320.20 | 298.13

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-02-29 | -403.96 | -598.20 | 194.24
2016-03-31 | -26.24 | -207.25 | 181.01
2016-07-31 | -863.06 | -914.52 | 51.46
2017-02-28 | -403.96 | -945.61 | 541.66
2017-04-30 | -322.64 | -1434.40 | 1111.76
2018-03-31 | -26.24 | -338.86 | 312.62
2018-04-30 | -322.64 | -1908.29 | 1585.64
2018-05-31 | -123.93 | -590.41 | 466.48

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -863.06 | -316.02 | 547.04
2016-01-31 | -976.40 | -379.51 | 596.89
2016-02-29 | -403.96 | -598.20 | 194.24
2016-03-31 | -26.24 | -207.25 | 181.01
2016-04-30 | -322.64 | 3084.27 | 3406.91
2016-05-31 | -123.93 | 392.90 | 516.83
2016-06-30 | -1417.61 | -411.48 | 1006.14
2016-07-31 | -863.06 | -914.52 | 51.46
2017-01-31 | -976.40 | -891.59 | 84.81
2017-02-28 | -403.96 | -945.61 | 541.66
2017-03-31 | -26.24 | 287.69 | 313.93
2017-04-30 | -322.64 | -1434.40 | 1111.76
2017-05-31 | -123.93 | -60.91 | 63.02
2017-06-30 | -1417.61 | 1259.40 | 2677.01
2017-07-31 | -863.06 | 972.12 | 1835.18
2018-01-31 | -976.40 | 1012.68 | 1989.08
2018-02-28 | -403.96 | 1285.39 | 1689.35
2018-03-31 | -26.24 | -338.86 | 312.62
2018-04-30 | -322.64 | -1908.29 | 1585.64
2018-05-31 | -123.93 | -590.41 | 466.48
2018-06-30 | -1417.61 | -1106.34 | 311.28

Total for Appliances:
Expected Increase but Failed Total: 15804.93
Expected Increase and Exceeded Total: 2111.28
Below Expected Drop Total: 4444.86
Expected Drop but Exceeded Total: 19482.34
Sales Performance Evaluation for Paper:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 506.81 | -298.34 | 805.14
2015-11-30 | 1281.39 | 855.43 | 425.96
2015-12-31 | 904.65 | -113.24 | 1017.89
2016-05-31 | 190.54 | -148.27 | 338.81
2016-06-30 | 80.77 | -801.08 | 881.85
2016-08-31 | 73.37 | 60.83 | 12.54
2016-09-30 | 506.81 | 173.32 | 333.49
2016-11-30 | 1281.39 | 181.16 | 1100.24
2016-12-31 | 904.65 | 508.14 | 396.51
2017-03-31 | 55.29 | -833.68 | 888.97
2017-08-31 | 73.37 | -674.99 | 748.35
2017-09-30 | 506.81 | 142.51 | 364.30
2017-11-30 | 1281.39 | -1019.10 | 2300.49
2017-12-31 | 904.65 | -377.41 | 1282.06
2018-05-31 | 190.54 | -521.98 | 712.52
2018-06-30 | 80.77 | -126.52 | 207.29

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-08-31 | 73.37 | 631.65 | 558.28
2016-03-31 | 55.29 | 270.13 | 214.84
2017-05-31 | 190.54 | 687.75 | 497.21
2017-06-30 | 80.77 | 945.09 | 864.32
2018-03-31 | 55.29 | 581.03 | 525.74

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -488.60 | 79.92 | 568.52
2015-10-31 | -422.71 | 170.12 | 592.83
2016-01-31 | -929.17 | 190.14 | 1119.31
2016-02-29 | -691.88 | -277.55 | 414.33
2016-04-30 | -560.45 | -191.81 | 368.64
2016-07-31 | -488.60 | -300.87 | 187.72
2016-10-31 | -422.71 | -216.23 | 206.48
2017-01-31 | -929.17 | -159.71 | 769.46
2017-02-28 | -691.88 | 170.94 | 862.82
2017-04-30 | -560.45 | 75.12 | 635.57
2017-07-31 | -488.60 | 238.44 | 727.04
2017-10-31 | -422.71 | 63.60 | 486.32
2018-01-31 | -929.17 | -12.94 | 916.23
2018-02-28 | -691.88 | 124.11 | 815.99
2018-04-30 | -560.45 | 134.19 | 694.64

Total for Paper:
Expected Increase but Failed Total: 11816.40
Expected Increase and Exceeded Total: 2660.39
Below Expected Drop Total: 0.00
Expected Drop but Exceeded Total: 9365.91
Sales Performance Evaluation for Accessories:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 2016.48 | -1701.39 | 3717.86
2015-11-30 | 2758.62 | -1623.63 | 4382.25
2015-12-31 | 4415.53 | -1420.99 | 5836.52
2016-09-30 | 2016.48 | 98.81 | 1917.67
2016-11-30 | 2758.62 | -130.22 | 2888.84
2016-12-31 | 4415.53 | 3764.53 | 651.00
2017-07-31 | 253.72 | -2648.96 | 2902.68
2017-09-30 | 2016.48 | 1379.09 | 637.38
2017-11-30 | 2758.62 | 1530.37 | 1228.25
2017-12-31 | 4415.53 | -2567.02 | 6982.55

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-07-31 | 253.72 | 1088.17 | 834.45
2016-07-31 | 253.72 | 1337.31 | 1083.59

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-08-31 | -564.04 | -1595.74 | 1031.70
2016-10-31 | -385.25 | -504.45 | 119.19

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-08-31 | -564.04 | 262.37 | 826.41
2015-10-31 | -385.25 | 180.16 | 565.42
2016-01-31 | -1773.43 | 123.32 | 1896.75
2016-02-29 | -1955.26 | 1200.89 | 3156.15
2016-03-31 | -954.96 | -168.98 | 785.98
2016-04-30 | -1841.34 | 991.18 | 2832.52
2016-05-31 | -849.30 | -617.06 | 232.24
2016-06-30 | -1120.76 | -207.21 | 913.55
2016-08-31 | -564.04 | -1595.74 | 1031.70
2016-10-31 | -385.25 | -504.45 | 119.19
2017-01-31 | -1773.43 | 229.60 | 2003.03
2017-02-28 | -1955.26 | -1206.05 | 749.21
2017-03-31 | -954.96 | -243.91 | 711.05
2017-04-30 | -1841.34 | -345.35 | 1495.99
2017-05-31 | -849.30 | 902.26 | 1751.56
2017-06-30 | -1120.76 | -976.78 | 143.98
2017-08-31 | -564.04 | 1109.88 | 1673.91
2017-10-31 | -385.25 | 100.80 | 486.05
2018-01-31 | -1773.43 | -576.40 | 1197.03
2018-02-28 | -1955.26 | -218.32 | 1736.94
2018-03-31 | -954.96 | 189.40 | 1144.36
2018-04-30 | -1841.34 | -869.31 | 972.04
2018-05-31 | -849.30 | -508.68 | 340.62
2018-06-30 | -1120.76 | 960.51 | 2081.26

Total for Accessories:
Expected Increase but Failed Total: 31144.98
Expected Increase and Exceeded Total: 1918.04
Below Expected Drop Total: 1150.89
Expected Drop but Exceeded Total: 28846.95
Sales Performance Evaluation for Envelopes:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-07-31 | 21.48 | -197.63 | 219.11
2015-09-30 | 162.23 | -111.01 | 273.24
2015-11-30 | 435.24 | 312.81 | 122.43
2015-12-31 | 282.12 | -145.45 | 427.58
2016-03-31 | 68.06 | -256.17 | 324.23
2016-09-30 | 162.23 | 72.72 | 89.50
2016-11-30 | 435.24 | -315.87 | 751.11
2016-12-31 | 282.12 | 254.13 | 27.99
2017-09-30 | 162.23 | 48.32 | 113.91
2017-11-30 | 435.24 | 13.10 | 422.14
2017-12-31 | 282.12 | -98.65 | 380.77

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2016-07-31 | 21.48 | 109.82 | 88.34
2017-03-31 | 68.06 | 120.16 | 52.10
2017-07-31 | 21.48 | 97.84 | 76.36
2018-03-31 | 68.06 | 146.05 | 77.99

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-08-31 | -172.51 | -210.13 | 37.62
2017-05-31 | -59.55 | -205.71 | 146.15
2017-10-31 | -38.08 | -136.06 | 97.98
2018-02-28 | -136.28 | -172.55 | 36.27

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-08-31 | -172.51 | 54.13 | 226.64
2015-10-31 | -38.08 | 64.18 | 102.27
2016-01-31 | -176.00 | -155.85 | 20.15
2016-02-29 | -136.28 | 165.53 | 301.81
2016-04-30 | -180.85 | 9.64 | 190.49
2016-05-31 | -59.55 | 121.77 | 181.33
2016-06-30 | -205.85 | 75.70 | 281.55
2016-08-31 | -172.51 | -210.13 | 37.62
2016-10-31 | -38.08 | 81.91 | 120.00
2017-01-31 | -176.00 | 16.57 | 192.57
2017-02-28 | -136.28 | 17.05 | 153.33
2017-04-30 | -180.85 | -31.67 | 149.17
2017-05-31 | -59.55 | -205.71 | 146.15
2017-06-30 | -205.85 | -65.86 | 140.00
2017-08-31 | -172.51 | 166.03 | 338.54
2017-10-31 | -38.08 | -136.06 | 97.98
2018-01-31 | -176.00 | 149.32 | 325.32
2018-02-28 | -136.28 | -172.55 | 36.27
2018-04-30 | -180.85 | 32.07 | 212.92
2018-05-31 | -59.55 | 93.97 | 153.52
2018-06-30 | -205.85 | 0.19 | 206.04

Total for Envelopes:
Expected Increase but Failed Total: 3152.00
Expected Increase and Exceeded Total: 294.80
Below Expected Drop Total: 318.02
Expected Drop but Exceeded Total: 3613.65
Sales Performance Evaluation for Fasteners:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-09-30 | 22.25 | 20.91 | 1.35
2015-10-31 | 25.75 | -23.95 | 49.70
2015-11-30 | 79.14 | -58.54 | 137.68
2015-12-31 | 26.45 | 4.05 | 22.41
2016-09-30 | 22.25 | -8.78 | 31.03
2016-10-31 | 25.75 | -57.74 | 83.50
2016-11-30 | 79.14 | 19.80 | 59.34
2016-12-31 | 26.45 | 15.31 | 11.15
2017-09-30 | 22.25 | -15.34 | 37.59
2017-11-30 | 79.14 | 35.53 | 43.61
2017-12-31 | 26.45 | -22.57 | 49.02

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2017-10-31 | 25.75 | 78.48 | 52.73

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-07-31 | -2.79 | -26.18 | 23.39
2016-02-29 | -8.56 | -31.12 | 22.56
2016-08-31 | -1.09 | -25.06 | 23.97
2017-03-31 | -24.37 | -28.72 | 4.34
2017-05-31 | -28.34 | -28.69 | 0.35
2017-08-31 | -1.09 | -13.37 | 12.27
2018-03-31 | -24.37 | -25.81 | 1.44
2018-04-30 | -7.09 | -38.24 | 31.15

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-07-31 | -2.79 | -26.18 | 23.39
2015-08-31 | -1.09 | 35.21 | 36.31
2016-01-31 | -41.92 | -5.08 | 36.83
2016-02-29 | -8.56 | -31.12 | 22.56
2016-03-31 | -24.37 | 51.32 | 75.69
2016-04-30 | -7.09 | -1.30 | 5.79
2016-05-31 | -28.34 | 19.28 | 47.62
2016-06-30 | -39.43 | 5.06 | 44.48
2016-07-31 | -2.79 | 8.21 | 11.00
2016-08-31 | -1.09 | -25.06 | 23.97
2017-01-31 | -41.92 | -5.40 | 36.52
2017-02-28 | -8.56 | 22.40 | 30.96
2017-03-31 | -24.37 | -28.72 | 4.34
2017-04-30 | -7.09 | 36.33 | 43.42
2017-05-31 | -28.34 | -28.69 | 0.35
2017-06-30 | -39.43 | -8.40 | 31.02
2017-07-31 | -2.79 | 14.75 | 17.55
2017-08-31 | -1.09 | -13.37 | 12.27
2018-01-31 | -41.92 | 7.27 | 49.19
2018-02-28 | -8.56 | 5.51 | 14.07
2018-03-31 | -24.37 | -25.81 | 1.44
2018-04-30 | -7.09 | -38.24 | 31.15
2018-05-31 | -28.34 | 6.20 | 34.54
2018-06-30 | -39.43 | 0.13 | 39.56

Total for Fasteners:
Expected Increase but Failed Total: 526.38
Expected Increase and Exceeded Total: 52.73
Below Expected Drop Total: 119.47
Expected Drop but Exceeded Total: 674.04
Sales Performance Evaluation for Supplies:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2016-01-31 | 809.18 | -1245.07 | 2054.25
2016-03-31 | 2926.68 | -3093.10 | 6019.78
2016-04-30 | 11.08 | -196.63 | 207.71
2017-01-31 | 809.18 | -1869.68 | 2678.86
2018-03-31 | 2926.68 | -2260.47 | 5187.14
2018-04-30 | 11.08 | -365.20 | 376.28

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2017-03-31 | 2926.68 | 4881.10 | 1954.43
2017-04-30 | 11.08 | 89.36 | 78.28
2018-01-31 | 809.18 | 2642.29 | 1833.11

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2015-09-30 | -356.37 | -433.82 | 77.45
2015-12-31 | -187.21 | -644.12 | 456.91
2016-12-31 | -187.21 | -786.79 | 599.58
2017-05-31 | -324.08 | -525.28 | 201.20
2017-07-31 | -456.04 | -669.77 | 213.73
2017-09-30 | -356.37 | -788.52 | 432.14
2018-05-31 | -324.08 | -555.54 | 231.46
2018-06-30 | -285.61 | -895.88 | 610.26

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-08-31 | -590.03 | -445.11 | 144.92
2015-09-30 | -356.37 | -433.82 | 77.45
2015-10-31 | -549.73 | 64.11 | 613.85
2015-11-30 | -465.94 | 55.27 | 521.21
2015-12-31 | -187.21 | -644.12 | 456.91
2016-02-29 | -531.93 | 351.12 | 883.05
2016-05-31 | -324.08 | 608.35 | 932.42
2016-06-30 | -285.61 | 127.89 | 413.50
2016-07-31 | -456.04 | 354.79 | 810.83
2016-08-31 | -590.03 | 529.98 | 1120.00
2016-09-30 | -356.37 | 749.87 | 1106.24
2016-10-31 | -549.73 | -274.20 | 275.53
2016-11-30 | -465.94 | -411.12 | 54.82
2016-12-31 | -187.21 | -786.79 | 599.58
2017-02-28 | -531.93 | -523.53 | 8.40
2017-05-31 | -324.08 | -525.28 | 201.20
2017-06-30 | -285.61 | 295.52 | 581.13
2017-07-31 | -456.04 | -669.77 | 213.73
2017-08-31 | -590.03 | -557.33 | 32.70
2017-09-30 | -356.37 | -788.52 | 432.14
2017-10-31 | -549.73 | -262.38 | 287.35
2017-11-30 | -465.94 | -116.62 | 349.31
2017-12-31 | -187.21 | 958.45 | 1145.66
2018-02-28 | -531.93 | -300.05 | 231.88
2018-05-31 | -324.08 | -555.54 | 231.46
2018-06-30 | -285.61 | -895.88 | 610.26

Total for Supplies:
Expected Increase but Failed Total: 16524.02
Expected Increase and Exceeded Total: 3865.81
Below Expected Drop Total: 2822.74
Expected Drop but Exceeded Total: 12335.53
Sales Performance Evaluation for Machines:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-11-30 | 3457.21 | -1573.99 | 5031.20
2016-04-30 | 2330.74 | -3104.81 | 5435.54
2016-06-30 | 0.69 | -2391.69 | 2392.38
2016-09-30 | 4237.92 | -6766.57 | 11004.50
2016-11-30 | 3457.21 | 48.47 | 3408.73
2016-12-31 | 713.29 | 361.63 | 351.66
2017-04-30 | 2330.74 | 1735.21 | 595.53
2017-09-30 | 4237.92 | -6427.16 | 10665.09
2017-11-30 | 3457.21 | 2141.31 | 1315.90
2017-12-31 | 713.29 | -3133.17 | 3846.45
2018-04-30 | 2330.74 | 1985.39 | 345.35

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2015-09-30 | 4237.92 | 13809.52 | 9571.60
2015-12-31 | 713.29 | 3387.32 | 2674.04
2017-06-30 | 0.69 | 2727.62 | 2726.93
2018-06-30 | 0.69 | 279.85 | 279.16

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-02-29 | -1090.93 | -2747.89 | 1656.96
2016-03-31 | -572.33 | -2520.16 | 1947.83
2017-01-31 | -1621.14 | -3538.87 | 1917.73
2017-08-31 | -1327.38 | -2376.01 | 1048.63
2018-02-28 | -1090.93 | -1433.56 | 342.63
2018-03-31 | -572.33 | -1462.54 | 890.21
2018-05-31 | -76.38 | -3003.33 | 2926.95

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-10-31 | -2875.55 | -389.01 | 2486.55
2016-01-31 | -1621.14 | 1071.27 | 2692.41
2016-02-29 | -1090.93 | -2747.89 | 1656.96
2016-03-31 | -572.33 | -2520.16 | 1947.83
2016-05-31 | -76.38 | 1081.38 | 1157.76
2016-07-31 | -3176.12 | 1456.95 | 4633.08
2016-08-31 | -1327.38 | 2786.54 | 4113.92
2016-10-31 | -2875.55 | 119.33 | 2994.88
2017-01-31 | -1621.14 | -3538.87 | 1917.73
2017-02-28 | -1090.93 | 4797.24 | 5888.17
2017-03-31 | -572.33 | 4598.49 | 5170.82
2017-05-31 | -76.38 | 2537.74 | 2614.12
2017-07-31 | -3176.12 | -1046.43 | 2129.70
2017-08-31 | -1327.38 | -2376.01 | 1048.63
2017-10-31 | -2875.55 | 885.47 | 3761.02
2018-01-31 | -1621.14 | 3083.39 | 4704.53
2018-02-28 | -1090.93 | -1433.56 | 342.63
2018-03-31 | -572.33 | -1462.54 | 890.21
2018-05-31 | -76.38 | -3003.33 | 2926.95

Total for Machines:
Expected Increase but Failed Total: 44392.33
Expected Increase and Exceeded Total: 15251.72
Below Expected Drop Total: 10730.92
Expected Drop but Exceeded Total: 53077.86
Sales Performance Evaluation for Copiers:

For Expected Increase but Failed:
Date | Expected Increase | Recorded Value | Failed Expectations
2015-12-31 | 939.05 | -703.22 | 1642.28
2016-03-31 | 5384.33 | -2718.54 | 8102.87
2016-05-31 | 1581.03 | -383.14 | 1964.17
2016-10-31 | 8009.47 | -8933.63 | 16943.10
2017-03-31 | 5384.33 | -7885.12 | 13269.44
2017-12-31 | 939.05 | -3675.72 | 4614.77
2018-05-31 | 1581.03 | -2647.70 | 4228.74

For Expected Increase and Exceeded:
Date | Expected Increase | Recorded Value | Exceeded Expectations
2016-12-31 | 939.05 | 4679.17 | 3740.11
2017-05-31 | 1581.03 | 3331.07 | 1750.03
2017-10-31 | 8009.47 | 9133.78 | 1124.31
2018-03-31 | 5384.33 | 10903.89 | 5519.56

Below Expected Drop:
Date | Expected Drop | Recorded Value | Failed Expectations
2016-07-31 | -313.42 | -1908.20 | 1594.78
2017-08-31 | -1845.88 | -2184.07 | 338.19
2017-09-30 | -1141.14 | -1177.24 | 36.10
2018-04-30 | -1959.51 | -2489.61 | 530.09

For Expected Drop but Exceeded:
Date | Expected Drop | Recorded Value | Exceeded Expectations
2015-11-30 | -2165.88 | 690.92 | 2856.80
2016-01-31 | -1821.45 | 303.15 | 2124.60
2016-02-29 | -3174.06 | 1635.34 | 4809.40
2016-04-30 | -1959.51 | 3058.63 | 5018.14
2016-06-30 | -3492.54 | 2467.55 | 5960.09
2016-07-31 | -313.42 | -1908.20 | 1594.78
2016-08-31 | -1845.88 | 2384.22 | 4230.10
2016-09-30 | -1141.14 | 1377.39 | 2518.53
2016-11-30 | -2165.88 | 1705.06 | 3870.94
2017-01-31 | -1821.45 | 298.12 | 2119.57
2017-02-28 | -3174.06 | 568.27 | 3742.32
2017-04-30 | -1959.51 | -268.80 | 1690.71
2017-06-30 | -3492.54 | -593.25 | 2899.29
2017-07-31 | -313.42 | 2108.35 | 2421.77
2017-08-31 | -1845.88 | -2184.07 | 338.19
2017-09-30 | -1141.14 | -1177.24 | 36.10
2017-11-30 | -2165.88 | -2095.75 | 70.14
2018-01-31 | -1821.45 | -301.04 | 1520.40
2018-02-28 | -3174.06 | -1903.38 | 1270.68
2018-04-30 | -1959.51 | -2489.61 | 530.09
2018-06-30 | -3492.54 | -1574.08 | 1918.46

Total for Copiers:
Expected Increase but Failed Total: 50765.37
Expected Increase and Exceeded Total: 12134.01
Below Expected Drop Total: 2499.17
Expected Drop but Exceeded Total: 51541.11
"""
