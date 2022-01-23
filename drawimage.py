from PIL import Image, ImageDraw, ImageFont


class GenerateMapMarker:

    def __init__(self, generate_limit: int, circle_color: str, width: int, height: int, font_size: int, font_color: str):
        self.generate_limit: int = generate_limit
        self.circle_color: str = circle_color
        self.width: int = width
        self.height: int = height
        self.font_size: int = font_size
        self.font_color: str = font_color

    def draw_ellipse_mask(self, image, width, antialias):
        """
        :param image:
        :param width:
        :param antialias:
        :return:
        """

        mask = Image.new(mode='L', size=(image.size[0] * antialias, image.size[1] * antialias))
        draw = ImageDraw.Draw(mask)
        offset, fill = (width / -2.0, 'white')
        bounds = (1, 1, self.width - 1, self.height - 1)
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse(xy=[left, top, right - 1, bottom], fill=fill)
        mask = mask.resize(image.size, Image.LANCZOS)
        image.paste(self.circle_color, mask=mask)

    def map_img_marker_generator(self, image_text: str):
        """
        :param image_text:
        :return:
        """
        image = Image.new('RGBA', size=(self.width, self.height))
        # drawing a circle on the created image
        self.draw_ellipse_mask(image=image, width=1, antialias=4)
        draw = ImageDraw.Draw(im=image)

        # Adding the desired text on the created image
        font = ImageFont.truetype(font='arial.ttf', size=self.font_size)
        weight_text, height_text = draw.textsize(text=image_text, font=font)
        draw.text(xy=((self.width - weight_text) / 2, (self.height - height_text - 3) / 2), text=image_text, font=font, fill=self.font_color, align='center')

        # save image
        image.save(f'image/{image_text}.png')

    def run(self):
        for i in range(self.generate_limit):
            self.map_img_marker_generator(image_text=str(i + 1))


generate_image = GenerateMapMarker(generate_limit=100, circle_color='#c0392b', width=48, height=48, font_size=28, font_color='#fff')
generate_image.run()
