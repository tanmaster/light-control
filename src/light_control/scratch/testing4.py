import colorsys

from light_control.main import send_static


def smooth_rgb_spectrum(steps=100):
    """
    Generates 'steps' number of smooth hex colors
    across the full RGB rainbow spectrum.
    """
    for i in range(steps):
        # Vary Hue from 0.0 to 1.0; keep Saturation and Value at max (1.0)
        hue = i / steps
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        # Convert 0.0-1.0 float values to 0-255 integers
        r, g, b = [int(x * 255) for x in rgb]

        # Format as a 6-digit hex string
        yield r, g, b


# Usage
for color in smooth_rgb_spectrum(1000):
    # sleep(0.01)
    send_static(color)
