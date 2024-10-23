import pandas as pd
import matplotlib.pyplot as plt

from metric_comp import compare_summary_stats


import pandas as pd
import matplotlib.pyplot as plt


def format_values(df):
    # Format the values to 2 decimal places, convert to int if .00
    df['modis'] = df['modis'].apply(lambda x: f"{round(x, 2):.2f}".rstrip(
        '0').rstrip('.') if x % 1 != 0 else f"{int(x)}")
    df['viirs'] = df['viirs'].apply(lambda x: f"{round(x, 2):.2f}".rstrip(
        '0').rstrip('.') if x % 1 != 0 else f"{int(x)}")
    return df


def save_dataframe_as_png(df, filename, title="DataFrame"):
    # Format the DataFrame values
    df = format_values(df)

    # Create a new figure
    plt.figure()

    # Hide axes
    plt.axis('off')

    # Create a table
    table = plt.table(cellText=df.values, colLabels=df.columns,
                      cellLoc='center', loc='center')

    # Set font size and scale the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)  # Scale the table size

    # Add title if provided
    if title:
        plt.title(title, fontsize=16, loc='center')

    # Save the figure as PNG
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()


for i in range(12, 13):
    df = compare_summary_stats(i, 2015, clip=True, nozeros=True)
    save_dataframe_as_png(
        df, f'band_{i}_2015_stats_plot.png', f'MODIS/VIIRS 2015 Band {i}')
# save_dataframe_as_png(df, 'dataframe_image.png', title='Summary Statistics')
