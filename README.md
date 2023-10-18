# About this repository
This repository provides a Python implementation of clarinet plots. Clarinet plots are plots similar to violin plots, and they are suitable for displaying zero-inflated distribution of scRNA-seq data. A clarinet plot shows the shape of quantile function raher than probability density function.

The original paper is in preparation.

# Open notebook
- [Open notebook in Colab](https://colab.research.google.com/github/okumakito/clarinet_plot/blob/main/clarinet_plot.ipynb) (executable)
- [Open notebook in GitHub](https://github.com/okumakito/clarinet_plot/blob/main/clarinet_plot.ipynb) (not executable)

# Required packages
numpy, scipy, pandas, matplotlib, seaborn

# Install
```
git clone https://github.com/okumakito/clarinet_plot.git
```

# Basic usage

* Import
  ```
  import clarinet_plot as cla
  ```
* Convert your data to a pandas DataFrame object with rows represent observations and columns represent variables such as genes, cell types, time points, experimental conditions, etc. If each column has different number of observations, set the number of rows to the maximum number of observations, and use `None` for missing values. **If your data is count data, it is recommended to convert them to log expression data (ex. `df2=df.apply(np.log1p)`).** You can load a test data by the following command:
  ```
  df = cla.load_test_data()
  ```
* Draw clarinet plots:
  ```
  cla.clarinet_plot(df)
  ```

# Options

* Change line width (ex. `lw=1`, default is 2)
* Change Edge color (ex. `ec='gray'`, default is '0.2')
* Change color map (ex. `cmap='tab10'`, default is 'husl')
  Change padding from axes (ex. `pad=0.2`, default is 0.05)
* Change padding between clarinets (ex. `pad_between=1`, default is 0.1)
* Reverse (`asceinding=False`)
* Horizontal (`vertical=False`)
* Tailless (`show_tail=False`)
* Use rank instead of quantile (`use_rank=True`)
* Half (`half=True`)
* Duet with violin (`duet=True`)
* Swap duet positions (`swap_duet=True`)
* Set color map for kernel density estimation (ex. `cmap_kde='tab10'`)
* Heatmap (`heatmap=True`)
* Stripe (`stripe=True`)
* Change stripe number (ex. `n_stripe=20`, default is10)
* Change stripe line width (ex. `lw_stripe=2`, default is 1)
* Change stripe edge color (ex. `ec_stripe='blue'`, default is '0.2')

NOTE: `half` cannot be used with `duet`.

# Advanced options

* If you would like to modify styles more in details, prepare an 'ax' object of matplotlib and pass it to clarinet_plot function as an argument.
  ```
  import matplotlib.pyplot as plt
  fig, ax = plt.subplots()
  cla.clarinet_plot(df, ax=ax)
  ax.set_title('clarinet plot')
  fig.show()
  ```
* Similarly, the second y-axis for duet mode can be modified by using another 'ax' object.
  ```
  import matplotlib.pyplot as plt
  fig, ax = plt.subplots()
  ax2 = ax.twinx()
  cla.clarinet_plot(df, duet-ax=ax, ax_kde=ax2)
  ax.set_ylabel('Left side label')
  ax2.set_ylabel('Right side label')
  fig.show()
  ```
