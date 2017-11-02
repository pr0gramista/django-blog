from pilkit.processors import ResizeToFit, Anchor


class UpscaleToFit(object):
    """Only upscales image to the given dimensions"""

    def __init__(self, width=None, height=None, anchor=Anchor.CENTER):
        """
        :param width: The maximum width of the desired image.
        :param height: The maximum height of the desired image.
        """
        self.width = width
        self.height = height
        self.anchor = anchor
        self.processor = ResizeToFit(width=width, height=height, anchor=anchor)

    def process(self, img):
        img_width, img_height = img.size

        if img_width < self.width and img_height < self.height:
            return self.processor.process(img)
        else:
            return img
