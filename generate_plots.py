from pathlib import Path
import os, sys
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.colors import SymLogNorm
from sklearn.metrics import r2_score

project_path = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(project_path)
from config import Config
from metric_comps import MetricDataset, resample_raster, create_summary_stats
config = Config()
    
def main(year, stats_output_dir):
    """
    Creates a multi-page PDF with comparison plots between MODIS and VIIRS snow metrics for a given year.
    Resamples VIIRS metrics to MODIS grid for comparison in all plots.
    Args:
        year (int): The year to process.
        stats_output_dir (Path): Directory to save the output PDF.
    Returns:
        None
    """
    
    pdf_path = Path(stats_output_dir) / f"{year}_modis_viirs_metrics_plots.pdf"
    with PdfPages(pdf_path) as pdf:


        compare_metrics_dict = {}
        for i in range(0, len(config.modis_metric_names)):
            compare_metrics_dict[f"{year} Band {i + 1}"] = {}
        compare_metrics_dict

        for i in range(0, len(config.modis_metric_names)):
            if config.viirs_metric_names[i] is None:
                continue
            print(f"Loading MODIS metric {i + 1}: {config.modis_metric_names[i]}")
            mds = MetricDataset(config.modis_metric_path, i+1, year, 'modis', 'v6', config.modis_metric_names)
            mds_array, mds_transform = mds.load_tiff()
            compare_metrics_dict[f"{year} Band {i + 1}"]["modis"] = mds_array


            if i == 11:
                band = 10
            else:
                band = i + 1
            print(f"Loading VIIRS metric {band}: {config.viirs_metric_names[i]}")
            vds = MetricDataset(config.viirs_metric_path, band, year, 'viirs', 'v001', config.viirs_metric_names)
            vds_array, vds_transform = resample_raster(mds, vds) #Use resample_raster to warp viirs metrics to modis grid
            compare_metrics_dict[f"{year} Band {i + 1}"]["viirs"] = vds_array

        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8.5, 11))
        axes = axes.flatten()

        index = 0
        for i, (key, values) in enumerate(compare_metrics_dict.items()):
            try:
                viirs_metric = values['viirs']
            except:
                continue
            modis_metric = values['modis']

            viirs_z_mask = np.nonzero(viirs_metric)
            viirs_metric = viirs_metric[viirs_z_mask]
            modis_z_mask = np.nonzero(modis_metric)
            modis_metric = modis_metric[modis_z_mask]

            _, viirs_bins = np.histogram(viirs_metric, bins=40)
            _, modis_bins = np.histogram(modis_metric, bins=40)

            ax = axes[index]
            ax.hist(viirs_metric.flatten(), bins=viirs_bins, alpha=0.8, label='viirs')
            ax.hist(modis_metric.flatten(), bins=modis_bins, alpha=0.6, label='modis')
            ax.set_title(config.modis_metric_names[i])

            ax.legend()

            index += 1

        plt.suptitle(f'{year}: MODIS VIIRS Histograms', fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        pdf.savefig(fig, dpi=300)

        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8.5, 11))
        axes = axes.flatten()
        index = 0
        for i in range(0, len(config.modis_metric_names)):
            d = compare_metrics_dict[f'{year} Band {i+1}']

            if 'viirs' in d.keys():
                d['modis'] = np.where(d['modis']==0, np.nan, d['modis'])
                d['viirs'] = np.where(d['viirs']==0, np.nan, d['viirs'])
                d['dif'] = d['modis'] - d['viirs']
                d['dif'] = np.ma.masked_where(np.isnan(d['dif']), d['dif'])
                dif = d['dif']
                print(config.modis_metric_names[i])
                print("Min:", dif.min(), "Mean:", dif.mean(), "Median:", np.ma.median(dif), "Max:", dif.max())
                print()

                ax = axes[index]
                cmap = plt.get_cmap('RdBu')
                cmap.set_bad(color='gray')

                divnorm = TwoSlopeNorm(vmin=dif.min(), vcenter=0, vmax=dif.max())

                im = ax.imshow(dif, cmap=cmap, norm=divnorm, interpolation='nearest')
                ax.set_title(f'{config.modis_metric_names[i]}')
                ax.axis('off')

                fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.03)
                index += 1

        plt.suptitle(f'{year}: Difference MODIS - VIIRS Metrics', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.97])  # Try 0.97 or even 0.98
        pdf.savefig(fig, dpi=300)
        plt.close('all')

        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8.5, 11))
        axes = axes.flatten()
        index = 0
        for i in range(0, len(config.modis_metric_names)):
            d = compare_metrics_dict[f'{year} Band {i+1}']
            if 'viirs' in d.keys():
                dif = d['dif']
                print(config.modis_metric_names[i])
                print("Min:", dif.min(), "Mean:", dif.mean(), "Median:", np.ma.median(dif), "Max:", dif.max())
                print()

                ax = axes[index]
                cmap = plt.get_cmap('RdBu')
                cmap.set_bad(color='gray')

                symlog_norm = SymLogNorm(linthresh=1, vmin=dif.min(), vmax=dif.max(), base=10)

                im = ax.imshow(dif, cmap=cmap, norm=symlog_norm, interpolation='nearest')
                ax.set_title(f'{config.modis_metric_names[i]}')
                ax.axis('off')

                fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.03)
                index += 1

        plt.suptitle(f'{year}: Difference MODIS - VIIRS - log scale', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        pdf.savefig(fig, dpi=300)
        plt.close('all')
        
        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8.5, 11))
        axes = axes.flatten()
        index = 0
        for i in range(0, len(config.modis_metric_names)):
            d = compare_metrics_dict[f'{year} Band {i+1}']
            if 'viirs' in d.keys():

                modis_array = d['modis']
                viirs_array = d['viirs']
                
                modis_flat = modis_array.flatten()
                viirs_flat = viirs_array.flatten()

                valid_mask = ~np.isnan(modis_flat) & ~np.isnan(viirs_flat)
                modis_valid = modis_flat[valid_mask]
                viirs_valid = viirs_flat[valid_mask]

                sample_size = min(50000, len(modis_valid))
                indices = np.random.choice(len(modis_valid), size=sample_size, replace=False)
                modis_sample = modis_valid[indices]
                viirs_sample = viirs_valid[indices]
                
                ax = axes[index]
                ax.scatter(modis_sample, viirs_sample, alpha=0.2, edgecolor='k', s=10)
                ax.set_xlabel('MODIS', fontsize=8)
                ax.set_ylabel('VIIRS', fontsize=8)
                ax.set_title(config.modis_metric_names[i], fontsize=10)
                ax.grid(True)

                r2 = r2_score(viirs_sample, modis_sample)
                ax.text(0.05, 0.95, f'$R^2$ = {r2:.4f}', transform=ax.transAxes,
                        fontsize=8, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.7))
                
                index += 1

        plt.suptitle(f'{year}: MODIS - VIIRS Metrics (sample of {sample_size} pixels)', fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        scatter_path = Path(stats_output_dir) / f"{year}_modis_viirs_scatter.png"
        plt.savefig(scatter_path, dpi=300, bbox_inches="tight")
        plt.close('all')
        
        fig, ax = plt.subplots(figsize=(8.5, 11))
        img = plt.imread(scatter_path)
        ax.imshow(img)
        ax.axis('off')
        pdf.savefig(fig, dpi=300)
        plt.close(fig)

        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8.5, 11))
        axes = axes.flatten()
        index = 0
        for i in range(0, len(config.modis_metric_names)):
            d = compare_metrics_dict[f'{year} Band {i+1}']
            if 'viirs' in d.keys():
                viirs_array = d['viirs']

                print(config.modis_metric_names[i])
                print("Min:", viirs_array.min(), "Mean:", viirs_array.mean(), "Median:", np.ma.median(viirs_array), "Max:", viirs_array.max())
                print()

                ax = axes[index]

                im = ax.imshow(viirs_array, interpolation='nearest')
                ax.set_title(f'{config.viirs_metric_names[i]}')
                ax.axis('off')

                fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.03)
                index += 1

        plt.suptitle(f'{year}: VIIRS Metrics', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        pdf.savefig(fig, dpi=300)
        plt.close('all')


        fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(8.5, 11))
        axes = axes.flatten()
        index = 0
        for i in range(0, len(config.modis_metric_names)):
            d = compare_metrics_dict[f'{year} Band {i+1}']
            if 'viirs' in d.keys():
                modis_array = d['modis']


                print(config.modis_metric_names[i])
                print("Min:", modis_array.min(), "Mean:", modis_array.mean(), "Median:", np.ma.median(modis_array), "Max:", modis_array.max())
                print()

                ax = axes[index]

                im = ax.imshow(modis_array, interpolation='nearest')
                ax.set_title(f'{config.modis_metric_names[i]}')
                ax.axis('off')

                fig.colorbar(im, ax=ax, orientation='vertical', fraction=0.03)
                index += 1

        plt.suptitle(f'{year}: MODIS Metrics', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        pdf.savefig(fig, dpi=300)
        plt.close('all')
        
if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate MODIS/VIIRS metric comparison plots.")
    parser.add_argument("year", type=int, nargs="?", default=2019, help="Year to process (default: 2019)")
    parser.add_argument("--output_dir", "-o", type=Path, default=".", help="Directory to save output plots (default: current directory)")
    args = parser.parse_args()

    stats_output_dir = args.output_dir

    main(args.year, stats_output_dir)