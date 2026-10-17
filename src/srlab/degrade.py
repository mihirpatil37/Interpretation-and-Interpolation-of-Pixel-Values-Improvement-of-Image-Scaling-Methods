"""Create low-resolution (LR) images from high-resolution (HR) ones."""

from PIL import Image



def modcrop(img: Image.Image, scale: int) -> Image.Image:
    """Crop the image so width and height are divisible by `scale`.

    Pixels are removed from the right and bottom edges.
    Example: a 2041x1357 image with scale=4 becomes 2040x1356.
    """
    width, height = img.size                                                                        # TODO 1
    new_width = width - width % scale                                                               # TODO 2
    new_height = height - height % scale
    return img.crop((0, 0, new_width, new_height))                                                  # TODO 3





def bicubic_downscale(img: Image.Image, scale: int) -> Image.Image:
    """Return the low-resolution version of `img`, shrunk by `scale` with bicubic.
    The image is modcropped first, so the result is exactly 1/scale the size.
    """
    
    img = modcrop(img, scale)                                                                       # TODO 4: modcrop the image (call your function above)
    width, height = img.size                                                                        # TODO 5: compute the LR size
    new_width = width // scale             
    new_height = height // scale
    new_img = img.resize((new_width, new_height), Image.Resampling.BICUBIC)                         # TODO 6: resize with bicubic and return it
    return new_img


