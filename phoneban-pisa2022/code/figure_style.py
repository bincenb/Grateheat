"""House figure style. Import with: from figure_style import apply_figure_style, panel_letter, PALETTE, direct_label"""
import matplotlib as mpl
import matplotlib.pyplot as plt

PALETTE = {
    "primary":   "#2E5A87",  # slate blue: the main result
    "secondary": "#8FB3D3",  # pale blue: a related second series
    "control":   "#9A9A9A",  # grey: controls, references, 'everything else'
    "accent":    "#B8412C",  # brick red: use at most once per figure
    "shade":     "#EFE3C8",  # sand: background bands (windows, periods)
    "ink":       "#222222",  # text and axes
}
# Colour-blind-safe set (Okabe-Ito) for 4+ categories
CATEGORICAL = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000"]

def apply_figure_style(sizes=(9, 8, 7), context="paper"):
    """sizes = (axis labels, tick labels, annotations) in points at final print size.
    context='poster' scales everything up for a science-fair board."""
    if context == "poster":
        sizes = tuple(round(s * 2.2) for s in sizes)
    label, tick, small = sizes
    lw = 0.8 if context == "paper" else 1.6
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
        "font.size": tick,
        "axes.labelsize": label,
        "axes.titlesize": label,
        "axes.titleweight": "normal",
        "axes.titlelocation": "left",
        "xtick.labelsize": tick,
        "ytick.labelsize": tick,
        "legend.fontsize": small,
        "legend.frameon": False,
        "axes.edgecolor": PALETTE["ink"],
        "axes.labelcolor": PALETTE["ink"],
        "xtick.color": PALETTE["ink"],
        "ytick.color": PALETTE["ink"],
        "text.color": PALETTE["ink"],
        "axes.linewidth": lw,
        "xtick.major.width": lw, "ytick.major.width": lw,
        "xtick.major.size": 3, "ytick.major.size": 3,
        "xtick.direction": "out", "ytick.direction": "out",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False,
        "axes.prop_cycle": mpl.cycler(color=[PALETTE["primary"], PALETTE["control"], PALETTE["secondary"], PALETTE["accent"]]),
        "lines.linewidth": 1.4 if context == "paper" else 2.8,
        "lines.markersize": 4 if context == "paper" else 8,
        "errorbar.capsize": 0,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "figure.constrained_layout.use": True,
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.fonttype": "none",
    })
    return sizes

def panel_letter(ax, letter, dx=-0.02, dy=1.02):
    """Bold lowercase panel letter just above the top-left corner of the axes area."""
    fs = mpl.rcParams["axes.labelsize"]
    fs = fs + 1 if isinstance(fs, (int, float)) else 10
    ax.text(dx, dy, letter, transform=ax.transAxes, fontsize=fs, fontweight="bold",
            ha="right", va="bottom", color=PALETTE["ink"])

def direct_label(ax, line_or_xy, text, color=None, dx=4, dy=0, **kw):
    """Label a series at its last point instead of using a legend.
    Pass a Line2D, or an (x, y) tuple in data coordinates. Offset is in points."""
    if hasattr(line_or_xy, "get_xdata"):
        x, y = line_or_xy.get_xdata()[-1], line_or_xy.get_ydata()[-1]
        color = color or line_or_xy.get_color()
    else:
        x, y = line_or_xy
    fs = mpl.rcParams["legend.fontsize"]
    ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                va="center", ha="left", color=color or PALETTE["ink"], fontsize=fs, **kw)
