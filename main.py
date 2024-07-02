import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

def get_all_colormaps():
    cmap_categories = {
        'Perceptually Uniform Sequential': ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
        'Sequential': ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                       'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                       'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'],
        'Sequential (2)': ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                           'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                           'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'],
        'Diverging': ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
        'Cyclic': ['twilight', 'twilight_shifted', 'hsv'],
        'Qualitative': ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                        'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                        'tab20c'],
        'Miscellaneous': ['flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                          'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                          'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                          'turbo', 'nipy_spectral', 'gist_ncar']
    }
    all_colormaps = [cmap for category in cmap_categories.values() for cmap in category]
    return all_colormaps, cmap_categories

def apply_colormap(image, colormap):
    gray_image = np.array(image.convert('L'))
    cmap = plt.get_cmap(colormap)
    colored_image = cmap(gray_image)
    colored_image = Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8))
    info = colormap_info(colormap)
    return colored_image, info

def colormap_info(colormap):
    cmap = plt.get_cmap(colormap)
    category = next((cat for cat, cmaps in cmap_categories.items() if colormap in cmaps), "Unknown")
    info = f"Colormap: {colormap}\nCategory: {category}\nIs perceptually uniform: {'Yes' if category == 'Perceptually Uniform Sequential' else 'No'}\nReversible: {'Yes' if hasattr(cmap, '_resample') else 'No'}\nRecommended use: "
    if category in ['Sequential', 'Sequential (2)']:
        info += "Representing ordered data that progresses from low to high"
    elif category == 'Diverging':
        info += "Representing data with a critical middle value"
    elif category == 'Cyclic':
        info += "Representing data that wraps around at the endpoints"
    elif category == 'Qualitative':
        info += "Representing categorical data"
    else:
        info += "Varies depending on the specific colormap"
    return info

all_colormaps, cmap_categories = get_all_colormaps()

css = """
.gradio-container {max-width: 1200px; margin: auto;}
.output-image img {
    max-height: 600px !important;
    width: 100% !important;
    object-fit: contain !important;
}
"""

iface = gr.Interface(
    fn=apply_colormap,
    inputs=[gr.Image(type="pil", label="Input Image"), gr.Dropdown(choices=all_colormaps, label="Colormap", info="Select a colormap to apply")],
    outputs=[gr.Image(type="pil", label="Colormap Applied", elem_id="output-image"), gr.Textbox(label="Colormap Information")],
    title="Apply Colormap to Image",
    description="Upload an image and select a colormap to apply. The image will be converted to grayscale before applying the colormap.",
    examples=[["path/to/example/image.jpg", "viridis"], ["path/to/another/example/image.jpg", "jet"]],
    article="""
    <p>This tool allows you to apply various colormaps to your images. Here are some tips:</p>
    <ul>
        <li>Perceptually Uniform Sequential colormaps like 'viridis' are great for most use cases.</li>
        <li>For diverging data, consider using a Diverging colormap like 'coolwarm'.</li>
        <li>Qualitative colormaps are best for categorical data.</li>
        <li>Be cautious with 'jet' and similar colormaps, as they can be misleading in some contexts.</li>
    </ul>
    """,
    css=css
)

iface.launch()
