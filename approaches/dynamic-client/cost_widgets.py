import numpy as np
import panel as pn


def calculate_level_size(*, level, pixels_per_tile, extra_dimension_length, data_dtype):
    """
    Calculate the uncompressed size for a given zoom level in GB.
    """
    data_size = (
        (pixels_per_tile * 2**level) ** 2
        * extra_dimension_length
        * data_dtype.itemsize
        * 1e-9
    )
    spatial_coords_size = (
        (pixels_per_tile * 2**level * 2) * data_dtype.itemsize * 1e-9
    )
    extra_coords_size = extra_dimension_length * data_dtype.itemsize * 1e-9
    return data_size + spatial_coords_size + extra_coords_size


def calculate_pyramid_cost(
    *,
    number_of_zoom_levels,
    pixels_per_tile,
    extra_dimension_length,
    data_dtype,
    data_compression_ratio,
    price_per_GB,
):
    """
    Calculated the uncompressed size for pyramids with a given number of zoom levels
    in GB.
    """
    data_dtype = np.dtype(data_dtype)
    pyramid_size = 0
    for level in range(number_of_zoom_levels):
        pyramid_level_size = calculate_level_size(
            level=level,
            pixels_per_tile=pixels_per_tile,
            extra_dimension_length=extra_dimension_length,
            data_dtype=data_dtype,
        )
        pyramid_size += pyramid_level_size
    pyramid_cost = pyramid_size / data_compression_ratio * price_per_GB
    return f"Pyramid cost: ${pyramid_cost:.2f}/month"


# Define widgets for panel app
extra_dim_widget = pn.widgets.IntSlider(
    name="Time dimension length", start=365, end=3650, step=365, value=730
)
pixels_widget = pn.widgets.DiscreteSlider(
    name="Pixels per tile", options=[128, 256, 512], value=128
)
zoom_level_widget = pn.widgets.IntSlider(
    name="Number of zoom levels", start=1, end=8, step=1, value=4
)
compression_widget = pn.widgets.IntSlider(
    name="Data compression ratio", start=5, end=9, step=2, value=7
)
dtype_widget = pn.widgets.Select(
    name="Data type", options=["float16", "float32", "float64"], value="float32"
)
price_widget = pn.widgets.FloatSlider(
    name="Storage pricing ($ per GB per month)",
    start=0.02,
    end=0.03,
    step=0.02,
    value=0.005,
)
