
from __future__ import absolute_import as _

from tcod.tcod import _CDataWrapper
from tcod.libtcod import ffi, lib


class Image(_CDataWrapper):
    """
    .. versionadded:: 2.0

    Args:
        width (int): Width of the new Image.
        height (int): Height of the new Image.

    Attributes:
        width (int): Read only width of this Image.
        height (int): Read only height of this Image.
    """
    def __init__(self, *args, **kargs):
        super(Image, self).__init__(*args, **kargs)
        if not self.cdata:
            self._init(*args, **kargs)
        self.width, self.height = self._get_size()

    def _init(self, width, height):
        self.cdata = ffi.gc(lib.TCOD_image_new(width, height),
                            lib.TCOD_image_delete)

    def clear(self, color):
        """Fill this entire Image with color.

        Args:
            color (Union[Tuple[int, int, int], Sequence[int]]):
                An (r, g, b) sequence or Color instance.
        """
        lib.TCOD_image_clear(self.cdata, color)

    def invert(self):
        """Invert all colors in this Image."""
        lib.TCOD_image_invert(self.cdata)

    def hflip(self):
        """Horizontally flip this Image."""
        lib.TCOD_image_hflip(self.cdata)

    def rotate90(self, rotations=1):
        """Rotate this Image clockwise in 90 degree steps.

        Args:
            rotations (int): Number of 90 degree clockwise rotations.
        """
        lib.TCOD_image_rotate90(self.cdata, rotations)

    def vflip(self):
        """Vertically flip this Image."""
        lib.TCOD_image_vflip(self.cdata)

    def scale(self, width, height):
        """Scale this Image to the new width and height.

        Args:
            width (int): The new width of the Image after scaling.
            height (int): The new height of the Image after scaling.
        """
        lib.TCOD_image_scale(self.cdata, width, height)
        self.width, self.height = width, height

    def set_key_color(self, color):
        """Set a color to be transparent during blitting functions.

        Args:
            color (Union[Tuple[int, int, int], Sequence[int]]):
                An (r, g, b) sequence or Color instance.
        """
        lib.TCOD_image_set_key_color(self.cdata, color)

    def get_alpha(self, x, y):
        """Get the Image alpha of the pixel at x, y.

        Args:
            x (int): X pixel of the image.  Starting from the left at 0.
            y (int): Y pixel of the image.  Starting from the top at 0.

        Returns:
            int: The alpha value of the pixel.
            With 0 being fully transparent and 255 being fully opaque.
        """
        return lib.TCOD_image_get_alpha(self.cdata, x, y)

    def refresh_console(self, console):
        """Update an Image created with :any:`tcod.image_from_console`.

        The console used with this function should have the same width and
        height as the Console given to :any:`tcod.image_from_console`.
        The font width and height must also be the same as when
        :any:`tcod.image_from_console` was called.

        Args:
            console (Console): A Console with a pixel width and height
                               matching this Image.
        """
        lib.TCOD_image_refresh_console(self.cdata, _cdata(console))

    def _get_size(self):
        """Return the (width, height) for this Image.

        Returns:
            Tuple[int, int]: The (width, height) of this Image
        """
        w = ffi.new('int *')
        h = ffi.new('int *')
        lib.TCOD_image_get_size(self.cdata, w, h)
        return w[0], h[0]

    def get_pixel(self, x, y):
        """Get the color of a pixel in this Image.

        Args:
            x (int): X pixel of the Image.  Starting from the left at 0.
            y (int): Y pixel of the Image.  Starting from the top at 0.

        Returns:
            Tuple[int, int, int]:
                An (r, g, b) tuple containing the pixels color value.
                Values are in a 0 to 255 range.
        """
        return lib.TCOD_image_get_pixel(self.cdata, x, y)

    def get_mipmap_pixel(self, left, top, right, bottom):
        """Get the average color of a rectangle in this Image.

        Parameters should stay within the following limits:
        * 0 <= left < right < Image.width
        * 0 <= top < bottom < Image.height

        Args:
            left (int): Left corner of the region.
            top (int): Top corner of the region.
            right (int): Right corner of the region.
            bottom (int): Bottom corner of the region.

        Returns:
            Tuple[int, int, int]:
                An (r, g, b) tuple containing the averaged color value.
                Values are in a 0 to 255 range.
        """
        color = lib.TCOD_image_get_mipmap_pixel(self.cdata,
                                                left, top, right, bottom)
        return (color.r, color.g, color.b)

    def put_pixel(self, x, y, color):
        """Change a pixel on this Image.

        Args:
            x (int): X pixel of the Image.  Starting from the left at 0.
            y (int): Y pixel of the Image.  Starting from the top at 0.
            color (Union[Tuple[int, int, int], Sequence[int]]):
                An (r, g, b) sequence or Color instance.
        """
        lib.TCOD_image_put_pixel(self.cdata, x, y, color)

    def blit(self, console, x, y, bg_blend, scale_x, scale_y, angle):
        """Blit onto a Console using scaling and rotation.

        Args:
            console (Console): Blit destination Console.
            x (int): Console X position for the center of the Image blit.
            y (int): Console Y position for the center of the Image blit.
                     The Image blit is centered on this position.
            bg_blend (int): Background blending mode to use.
            scale_x (float): Scaling along Image x axis.
                             Set to 1 for no scaling.  Must be over 0.
            scale_y (float): Scaling along Image y axis.
                             Set to 1 for no scaling.  Must be over 0.
            angle (float): Rotation angle in radians. (Clockwise?)
        """
        lib.TCOD_image_blit(self.cdata, _cdata(console), x, y, bg_blend,
                            scale_x, scale_y, angle)

    def blit_rect(self, console, x, y, width, height, bg_blend):
        """Blit onto a Console without scaling or rotation.

        Args:
            console (Console): Blit destination Console.
            x (int): Console tile X position starting from the left at 0.
            y (int): Console tile Y position starting from the top at 0.
            width (int): Use -1 for Image width.
            height (int): Use -1 for Image height.
            bg_blend (int): Background blending mode to use.
        """
        lib.TCOD_image_blit_rect(self.cdata, _cdata(console),
                                 x, y, width, height, bg_blend)

    def blit_2x(self, console, dest_x, dest_y,
                img_x=0, img_y=0, img_width=-1, img_height=-1):
        """Blit onto a Console with double resolution.

        Args:
            console (Console): Blit destination Console.
            dest_x (int): Console tile X position starting from the left at 0.
            dest_y (int): Console tile Y position starting from the top at 0.
            img_x (int): Left corner pixel of the Image to blit
            img_y (int): Top corner pixel of the Image to blit
            img_width (int): Width of the Image to blit.
                             Use -1 for the full Image width.
            img_height (int): Height of the Image to blit.
                              Use -1 for the full Image height.
        """
        lib.TCOD_image_blit_2x(self.cdata, _cdata(console), dest_x, dest_y,
                               img_x, img_y, img_width, img_height)

    def save_as(self, filename):
        """Save the Image to a 32-bit .bmp or .png file.

        Args:
            filename (AnyStr): File path to same this Image.
        """
        lib.TCOD_image_save(self.cdata, _bytes(filename))
