import numpy as np
import matplotlib.pyplot as plt

def load_plotting_config():
    from cycler import cycler
    colors=['#fe9f6d', '#de4968', '#8c2981', '#3b0f70', '#000004']
    default_cycler = cycler(color=['#fe9f6d', '#de4968', '#8c2981', '#3b0f70', '#000004'])

    params = {'figure.figsize': (7, 3),
            'axes.prop_cycle': default_cycler,
            'axes.titlesize': 14,
            'legend.fontsize': 12,
            'axes.labelsize': 14,
            'axes.titlesize': 14,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12}
    plt.rcParams.update(params)

def plot_pulse_cal_data(tt, zz, vv, figsize=(10, 8), n_plots=5, colors=['#feb078', '#f1605d'],
                        xlabel=None, ylabel=None, ylabel_twin=None, title=None):
    # Assume time is recorded in second
    fig, axes = plt.subplots(n_plots, 1, figsize=figsize)

    sec_per_plot = np.round(tt.max() / n_plots)
    for i, ax in enumerate(axes):
        idx = np.logical_and(tt > i*sec_per_plot, tt < (i+1)*sec_per_plot)
        ax.plot(tt[idx], zz[idx], colors[0])

        # ax.set_ylim(-2e-3, 2e-3)
        
        # ax.plot(tt, lp_bp)
        # ax.set_ylim(-2e-16, 2e-16)
        
        # Recorded drive signal is 20x smaller than the actual
        ax_twin = ax.twinx()
        ax_twin.plot(tt[idx], vv[idx]*20, colors[1], alpha=0.6)

        if i == int(n_plots / 2):
            if ylabel is not None:
                ax.set_ylabel(ylabel, fontsize=14)
            if ylabel_twin is not None:
                ax_twin.set_ylabel(ylabel_twin, fontsize=14)
        
    if title is not None:
        axes[0].set_title(title, fontsize=14)
    if xlabel is not None:
        axes[-1].set_xlabel(xlabel, fontsize=14)
    fig.tight_layout()\
    
    return fig, axes