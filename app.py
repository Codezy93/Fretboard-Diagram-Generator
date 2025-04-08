from PIL import ImageDraw, Image, ImageFont
import argparse
import pickle
import os

font_path = r"C:\Windows\Fonts\times.ttf"
title_font = ImageFont.truetype(font_path, 40)
subtitle_font = ImageFont.truetype(font_path, 25)
note_font = ImageFont.truetype(font_path, 20)

class CreateDiagram:
    def __init__(self, title, frets):
        self.title = title
        self.w = 550
        self.h = (frets*100) + 150
        self.image = Image.new("RGB", (self.w, self.h), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.frets = frets

    def create_base(self):

        # Add Title to the image
        self.draw.text((self.w//2, 10), self.title, font=title_font, fill="black", anchor='mt')

        # Add the String Names
        for i, j in zip([x for x in range(30, 540, 100)], ['E', 'A', "D", "G", 'B', 'E']):
            self.draw.text((i, 70), j, font=subtitle_font, fill="black", anchor='mt')

        # Add the String Lines
        for x in range(30, 540, 100):
            self.draw.line([(x, 100), (x, (self.h)-50)], fill="black", width=2)

        # Add Fret Lines
        for i in range(0, self.frets+1):
            if i != 0:
                self.draw.text((5, (i*100)+50), str(i), font=subtitle_font, fill="black", anchor='lt')
            self.draw.line([(30, (i*100)+100), (530, (i*100)+100)], fill="black", width=2)

    def add_points(self, mapping):
        """
        This dict must match the order of the x-axis: 
        E=0, B=1, G=2, D=3, A=4, E=5
        """
        # Chromatic scale array, starting from A=0
        scales = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

        # Open strings (E, B, G, D, A, E) in terms of the above scales array:
        # A=0, A#=1, B=2, C=3, C#=4, D=5, D#=6, E=7, F=8, F#=9, G=10, G#=11
        open_string_indices = [7, 0, 5, 10, 2, 7]  
        # => E=7, B=2, G=10, D=5, A=0, E=7

        # Place each note and annotate it
        for x, string_key in enumerate(mapping):
            for y in mapping[string_key]:
                # Draw the marker
                if y == 0:
                    self.draw.ellipse(((100*x)+15, (y*100)+85, (100*x)+45, (y*100)+115), fill=(0, 0, 0), outline=(0, 0, 0))
                    note_index = (open_string_indices[x] + y) % 12
                    note_name = scales[note_index]
                    self.draw.text(((100*x)+30, (y*100)+100), note_name, font=note_font, fill="white", anchor='mm')
                else:
                    self.draw.ellipse(((100*x)+15, (y*100)+35, (100*x)+45, (y*100)+65), fill=(0, 0, 0), outline=(0, 0, 0))
                    note_index = (open_string_indices[x] + y) % 12
                    note_name = scales[note_index]
                    self.draw.text(((100*x)+30, (y*100)+50), note_name, font=note_font, fill="white", anchor='mm')

    def show(self):
        self.image.show()

    def save(self):
        save_path = f"saves/{self.title}.jpg"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.image.save(save_path, format='JPEG')


    def serialize(self, mapping):
        if not os.path.exists('serialized/'):
            os.makedirs('serialized/')
        with open(f"serialized/{self.title}.sav", "wb") as f:
            pickle.dump(mapping, f)
    
    def get_from_save(self, title):
        pass

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    diag = CreateDiagram('Major and Sharp Notes', 24)
    diag.create_base()
    mapping = {
        "E":[],
        "A":[],
        "D":[],
        "G":[],
        "B":[],
        "el":[],
    }
    diag.add_points(mapping)
    diag.serialize(mapping)
    # diag.show()
    diag.save()