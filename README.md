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
  df = cla.load_testdata()
  ```
* Draw clarinet plots:
  ```
  cla.clarinet_plot(df)
  ```

# Options

* Reverse (`asceinding=False`)
* Horizontal (`vertical=False`)
* Tailless (`show_tail=False`)
* Use rank instead of quantile (`use_rank=True`)
* Half (`half=True`)
* Duet with violin (`duet=True`)
* Heatmap (`heatmap=True`)
* Stripe (`stripe=True`)

NOTE: `half` cannot be used with `duet`.
