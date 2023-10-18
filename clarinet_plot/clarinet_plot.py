import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
from scipy import stats
from matplotlib.patches import PathPatch
sns.set_context('talk', font_scale=0.8)

def clarinet_plot(
    df,
    lw        = 2,
    ec        = '0.2',
    h_pad     = 0.1,
    pad       = 0.05,
    cmap      = None,
    ax        = None,
    ascending = True,
    vertical  = True,
    show_tail = True,
    half      = False,
    duet      = False,
    cmap_kde  = None,
    ax_kde    = None,
    swap_duet = False,
    use_rank  = False,
    heatmap   = False,
    stripe    = False,
    n_stripe  = 10,
    lw_stripe = 1,
    ec_stripe = '0.2'
  ):
  '''
  Draw clarinet plots.
  '''
  # restriction
  if duet:
    half = False

  # get stats
  n_col = df.shape[1]
  max_val = df.abs().max().max()
  n_max = df.count().max()

  # center positions
  if half:
    x_arr = (1 + h_pad) * np.arange(n_col)
  else:
    x_arr = (1 + h_pad) * 2 * np.arange(n_col)
  if not vertical:
    x_arr = x_arr[::-1]

  # color
  if cmap == None:
    if heatmap:
      cmap = 'magma'
    else:
      cmap = 'husl'
  if cmap == 'husl':
    c_arr = sns.husl_palette(n_col)
  else:
    c_arr = plt.get_cmap(cmap)(np.arange(n_col))

  # color for kde
  if cmap_kde == None:
    if not heatmap:
      cmap_kde = cmap
    else:
      cmap_kde = 'husl'
  if cmap_kde == 'husl':
    c2_arr = sns.husl_palette(n_col)
  else:
    c2_arr = plt.get_cmap(cmap_kde)(np.arange(n_col))

  # main loop
  for i, (col, sr_in) in enumerate(df.iteritems()):
    x  = x_arr[i]
    c  = c_arr[i]
    c2 = c2_arr[i]

    # right x-coordinate
    sr = sr_in.dropna() / max_val
    sr = sr.sort_values(ascending=ascending)
    x1_arr = x + sr.values

    # y-coordinate
    if use_rank:
      if ascending:
        y_arr = np.arange(n_max)[-sr.size:]
      else:
        y_arr = np.arange(n_max)[:sr.size]
    else:
      y_arr = np.linspace(0,1,sr.size)

    # tail
    if not show_tail:
      x1_arr = x1_arr[sr!=0]
      y_arr = y_arr[sr!=0]
      sr = sr[sr!=0]

    # left x-coordinate
    if half or duet:
      x2_arr = x * np.ones_like(x1_arr)
    else:
      x2_arr = x - sr.values

    # kde coordinates
    if duet:
      if ax_kde == None:
        ax_kde = ax.twinx() if vertical else ax.twiny()
      sr2 = sr_in.dropna()
      yy_arr = np.linspace(sr2.min(), sr2.max())
      xx_arr = stats.gaussian_kde(sr2[sr2!=0])(yy_arr)
      xx_arr = x - xx_arr / xx_arr.max()
      if vertical == swap_duet:
        x1_arr = -x1_arr + 2 * x
        xx_arr = -xx_arr + 2 * x

    # draw clarinet
    def draw_func(x1_arr, x2_arr, y_arr, ax, **kws):
      if vertical:
        return ax.fill_betweenx(y_arr, x2_arr, x1_arr, **kws)
      else:
        return ax.fill_between(y_arr, x2_arr, x1_arr, **kws)

    if not heatmap:
      draw_func(x1_arr, x2_arr, y_arr, ax, fc=c, ec=ec, lw=lw)
    else:
      # heatmap
      g = draw_func(x1_arr, x2_arr, y_arr, ax, fc='none', ec=ec, lw=lw)
      xr_min = np.min([x1_arr.min(), x2_arr.min()])
      xr_max = np.max([x1_arr.max(), x2_arr.max()])
      if vertical:
        rect = [xr_min, xr_max, y_arr.min(), y_arr.max()]
        img = ax.imshow(sr.values[::-1].reshape(-1,1), extent=rect,
                        cmap=cmap, aspect='auto')
      else:
        rect = [y_arr.min(), y_arr.max(), xr_min, xr_max]
        img = ax.imshow(sr.values.reshape(1,-1), extent=rect,
                        cmap=cmap, aspect='auto')
      clip = PathPatch(g.get_paths()[0], transform=ax.transData)
      img.set_clip_path(clip)

    # draw kde
    if duet:
      draw_func(xx_arr, x, yy_arr, ax_kde, fc=c2, ec=ec, lw=lw)

    # stripe
    if stripe:
      for v in np.linspace(0, 1, n_stripe):
        if ascending:
          i = sr.gt(v).argmax()
        else:
          i = sr.lt(v).argmax()
        if i != 0:
          if vertical:
            ax.plot([x2_arr[i], x1_arr[i]], [y_arr[i], y_arr[i]],
                    c=ec_stripe, lw=lw_stripe)
          else:
            ax.plot([y_arr[i], y_arr[i]], [x2_arr[i], x1_arr[i]],
                    c=ec_stripe, lw=lw_stripe)

  # ticks
  if vertical:
    ax.set_xticks(x_arr)
    ax.set_xticklabels(df.columns)
  else:
    ax.set_yticks(x_arr)
    ax.set_yticklabels(df.columns)

  # lim
  x_min = 0 if half else -1
  x_max = x_arr.max() + 1
  y_min = 0
  y_max = n_max if use_rank else 1
  dx    = pad * (x_max - x_min)
  dy    = pad * (y_max - y_min)
  xlim  = (x_min - dx, x_max + dx)
  ylim  = (y_min - dy, y_max + dy)
  if vertical:
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
  else:
    ax.set_xlim(ylim)
    ax.set_ylim(xlim)
