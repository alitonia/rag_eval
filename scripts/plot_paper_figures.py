#!/usr/bin/env python3
"""Generate publication-grade Okabe-Ito vector figures for RegRAG-VN (IEEE-RIVF 2026)."""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_DIR = Path(__file__).resolve().parent.parent / "paper" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Okabe-Ito colorblind-safe palette
OI_BLUE = "#0072B2"
OI_SKY = "#56B4E9"
OI_ORANGE = "#E69F00"
OI_GREEN = "#009E73"
OI_VERM = "#D55E00"
OI_PURPLE = "#CC79A7"
OI_GRAY = "#7F7F7F"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 8.0,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8.0,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.2,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def make_benchmark_figure() -> None:
    """Fig 2: Benchmark composition (88 questions: 64 answerable + 24 unanswerable probes)."""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(3.52, 1.62), gridspec_kw={"width_ratios": [1.0, 1.35]}
    )
    fig.subplots_adjust(left=0.04, right=0.97, top=0.82, bottom=0.22, wspace=0.82)

    # Panel (a): 88 Questions split
    cats = ["Answer-\nable", "Unansw-\nerable"]
    vals = [64, 24]
    colors = [OI_BLUE, OI_VERM]
    bars = ax1.bar(cats, vals, color=colors, width=0.54, edgecolor="none")
    ax1.set_ylim(0, 88)
    ax1.set_ylabel("Questions")
    ax1.set_title("(a) 88 Gold Questions", pad=5, fontweight="bold")
    ax1.grid(axis="y", alpha=0.22, linewidth=0.5)
    ax1.set_axisbelow(True)
    for b, v in zip(bars, vals):
        ax1.text(
            b.get_x() + b.get_width() / 2,
            v + 2.0,
            f"{v}\n({v/88*100:.0f}%)",
            ha="center",
            va="bottom",
            fontsize=6.8,
            fontweight="bold",
        )

    # Panel (b): Breakdown of 24 unanswerable probes
    probe_types = [
        "CAR / Foreign loan",
        "Parcel-merging",
        "Marital property",
        "Payment-account",
    ]
    probe_counts = [2, 1, 7, 14]
    pcols = [OI_GRAY, OI_PURPLE, OI_ORANGE, OI_SKY]
    y_pos = np.arange(len(probe_types))
    hbars = ax2.barh(y_pos, probe_counts, color=pcols, height=0.58)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(probe_types, fontsize=7.0)
    ax2.set_xlim(0, 18.0)
    ax2.set_xlabel("Probes (n = 24)")
    ax2.set_title("(b) Refusal Probe Taxonomy", pad=5, fontweight="bold")
    ax2.grid(axis="x", alpha=0.22, linewidth=0.5)
    ax2.set_axisbelow(True)
    for b, v in zip(hbars, probe_counts):
        ax2.text(
            v + 0.4,
            b.get_y() + b.get_height() / 2,
            f"{v}",
            va="center",
            ha="left",
            fontsize=7.0,
            fontweight="bold",
        )

    fig.savefig(OUT_DIR / "fig_benchmark.pdf", format="pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT_DIR / "fig_benchmark.png", dpi=200, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_results_figure() -> None:
    """Fig 3: Two-panel visual of Table I (Hallucination) & Tables II-III (Citation Funnel)."""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(7.16, 1.82), gridspec_kw={"width_ratios": [1.15, 1.15]}
    )
    fig.subplots_adjust(left=0.07, right=0.98, top=0.83, bottom=0.18, wspace=0.52)

    # Panel (a): Hallucination Rate across 3 models x 3 modes (Table I)
    models = ["Qwen2.5-7B", "Qwen2.5-3B", "Vistral-7B"]
    closed = [0.438, 0.750, 0.625]
    bm25 = [0.344, 0.469, 0.672]
    dense = [0.313, 0.422, 0.594]

    x = np.arange(len(models))
    w = 0.25
    b1 = ax1.bar(x - w, closed, width=w, color=OI_GRAY, label="Closed-book")
    b2 = ax1.bar(x, bm25, width=w, color=OI_ORANGE, label="RAG-BM25")
    b3 = ax1.bar(x + w, dense, width=w, color=OI_BLUE, label="RAG-Dense")

    ax1.set_xticks(x)
    ax1.set_xticklabels(models)
    ax1.set_ylim(0, 1.02)
    ax1.set_ylabel("Hallucination Rate")
    ax1.set_title("(a) Hallucination Rate (Table I)", pad=7, fontweight="bold")
    ax1.grid(axis="y", alpha=0.22, linewidth=0.5)
    ax1.set_axisbelow(True)
    ax1.legend(frameon=False, loc="upper left", ncol=3, handlelength=1.1, columnspacing=0.9)

    for bars in (b1, b2, b3):
        for b in bars:
            h = b.get_height()
            ax1.text(
                b.get_x() + b.get_width() / 2,
                h + 0.015,
                f"{h:.2f}",
                ha="center",
                va="bottom",
                fontsize=6.3,
            )

    # Panel (b): Retrieval-to-Citation Funnel (Tables II & III)
    stages = [
        "Điều F1 (Closed)",
        "Khoản Acc. (Dense)",
        "Điều F1 (BM25)",
        "Điều F1 (Dense)",
        "Điều@3 (BM25)",
        "Điều@3 (Dense)",
        "Doc@3 (Dense)",
        "Doc@3 (BM25)",
    ]
    rates = [0.5, 31.7, 32.6, 43.4, 49.2, 52.4, 89.1, 90.6]
    scols = [OI_GRAY, OI_VERM, OI_GREEN, OI_GREEN, OI_ORANGE, OI_ORANGE, OI_SKY, OI_SKY]
    y = np.arange(len(stages))
    hbars = ax2.barh(y, rates, color=scols, height=0.62)
    ax2.set_yticks(y)
    ax2.set_yticklabels(stages, fontsize=7.0)
    ax2.set_xlim(0, 106)
    ax2.set_xlabel("Percentage (%)")
    ax2.set_title("(b) Retrieval-to-Citation Funnel (Tables II–III)", pad=6, fontweight="bold")
    ax2.grid(axis="x", alpha=0.22, linewidth=0.5)
    ax2.set_axisbelow(True)
    for b, v in zip(hbars, rates):
        ax2.text(
            v + 1.4,
            b.get_y() + b.get_height() / 2,
            f"{v:.1f}%",
            va="center",
            ha="left",
            fontsize=6.8,
            fontweight="bold",
        )

    fig.savefig(OUT_DIR / "fig_results.pdf", format="pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT_DIR / "fig_results.png", dpi=200, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def make_pipeline_figure() -> None:
    """Fig 1: Clean horizontal architecture & trust-boundary diagram."""
    fig, ax = plt.subplots(figsize=(7.16, 1.38))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 24)
    ax.axis("off")

    def card(x, y, w, h, title, body, edge, fill, header_fill):
        # Main card
        box = mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.35,rounding_size=1.2",
            linewidth=1.0, edgecolor=edge, facecolor=fill
        )
        ax.add_patch(box)
        # Header band
        hdr = mpatches.FancyBboxPatch(
            (x, y + h - 4.3), w, 4.3, boxstyle="round,pad=0.35,rounding_size=1.0",
            linewidth=0, facecolor=header_fill
        )
        ax.add_patch(hdr)
        ax.text(x + w / 2, y + h - 2.1, title, ha="center", va="center",
                fontsize=7.0, fontweight="bold", color="white")
        ax.text(x + w / 2, y + (h - 4.3) / 2, body, ha="center", va="center",
                fontsize=6.7, color="#1F2937", linespacing=1.32)

    # 4 main stages
    card(1.0, 5.8, 20.5, 16.0, "1. Gold Inputs",
         "88 QA questions\n(64 ans. + 24 probes)\n+ SHA-1 manifest\n(trusted only)",
         OI_BLUE, "#EEF6FC", OI_BLUE)

    card(26.0, 5.8, 22.0, 16.0, "2. Ingestion & Gate",
         "22 statutes → 3,703\nTier-2 chunks + Tier-1\nCoverage gate:\nverbatim passage check",
         OI_ORANGE, "#FFF7EB", "#C97A00")

    card(52.5, 5.8, 22.0, 16.0, "3. Retrieval & Gen.",
         "BM25 (pyvi) / BGE-M3\ntop-3 context packing\n3 models × 3 modes\n(4-bit greedy → 792)",
         OI_GREEN, "#EDF9F5", "#007A59")

    card(79.0, 5.8, 20.0, 16.0, "4. Provenance Audit",
         "Lexical groundedness\n+ Điều / Khoản F1\nTagged by (corpus,\nretriever_backend)",
         OI_PURPLE, "#FAF0F6", "#9E4D7C")

    # Forward arrows
    arrow_kw = dict(arrowstyle="-|>,head_width=0.35,head_length=0.55",
                    lw=1.3, color="#374151")
    for x0, x1 in [(21.9, 25.6), (48.4, 52.1), (74.9, 78.6)]:
        ax.annotate("", xy=(x1, 13.8), xytext=(x0, 13.8), arrowprops=arrow_kw)

    # Gate exclusion branch below Stage 2
    ax.annotate("", xy=(37.0, 1.4), xytext=(37.0, 5.4),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.45",
                                lw=1.0, color=OI_VERM, ls="--"))
    ax.text(38.0, 3.2, "Missing passage → Excluded",
            ha="left", va="center", fontsize=6.6, color=OI_VERM, fontweight="bold")

    fig.savefig(OUT_DIR / "fig_pipeline.pdf", format="pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(OUT_DIR / "fig_pipeline.png", dpi=200, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


if __name__ == "__main__":
    make_pipeline_figure()
    make_benchmark_figure()
    make_results_figure()
    print("Generated figures in", OUT_DIR)
