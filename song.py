from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import os
import io

app = Flask(__name__)

# Font settings
font_path = r"C:\Windows\Fonts\times.ttf"
title_font = ImageFont.truetype(font_path, 40)
subtitle_font = ImageFont.truetype(font_path, 25)
note_font = ImageFont.truetype(font_path, 20)

# Note mappings
sharp_notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
flat_notes = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"]
open_string_indices = [7, 0, 5, 10, 2, 7]  # E, A, D, G, B, E

class CreateDiagram:
    def __init__(self, title, frets, mode="sharp"):
        self.title = title
        self.w = 550
        self.h = (frets * 100) + 150
        self.image = Image.new("RGB", (self.w, self.h), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.frets = frets
        self.mode = mode

    def create_base(self):
        self.draw.text((self.w // 2, 10), self.title, font=title_font, fill="black", anchor='mt')
        for i, j in zip(range(30, 540, 100), ['E', 'A', "D", "G", 'B', 'E']):
            self.draw.text((i, 70), j, font=subtitle_font, fill="black", anchor='mt')
        for x in range(30, 540, 100):
            self.draw.line([(x, 100), (x, self.h - 50)], fill="black", width=2)
        for i in range(self.frets + 1):
            if i != 0:
                self.draw.text((5, (i * 100) + 50), str(i), font=subtitle_font, fill="black", anchor='lt')
            self.draw.line([(30, (i * 100) + 100), (530, (i * 100) + 100)], fill="black", width=2)

    def add_points(self, mapping):
        scales = sharp_notes if self.mode == "sharp" else flat_notes
        for x, string_key in enumerate(mapping):
            for y in mapping[string_key]:
                note_index = (open_string_indices[x] + y) % 12
                note_name = scales[note_index]
                self.draw.ellipse(((100*x)+15, (y*100)+35, (100*x)+45, (y*100)+65), fill="black", outline="black")
                self.draw.text(((100*x)+30, (y*100)+50), note_name, font=note_font, fill="white", anchor='mm')

    def get_image(self):
        img_io = io.BytesIO()
        self.image.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    title = data.get('title', 'Guitar Fretboard')
    frets = int(data.get('frets', 12))
    mode = data.get('mode', 'sharp')
    mapping = data.get('mapping', {"E": [], "A": [], "D": [], "G": [], "B": [], "e": []})
    
    diag = CreateDiagram(title, frets, mode)
    diag.create_base()
    diag.add_points(mapping)
    return send_file(diag.get_image(), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)