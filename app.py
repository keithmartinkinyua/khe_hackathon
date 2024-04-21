from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import io
from pydub import AudioSegment
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from io import BytesIO
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        audio_data = request.files['audio'].read()
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
        audio_data = audio_segment.export(format="wav").read()

        audio_file = io.BytesIO(audio_data)

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)
            return jsonify({"transcript": text})
        except sr.UnknownValueError:
            return jsonify({"error": "Speech recognition could not understand the audio."})
        except sr.RequestError as e:
            return jsonify({"error": f"Could not request results from the speech recognition service: {e}"})


def text_to_sign_language_animation(text):
    # ...
    images_folder = r'/home/keithmartin/Desktop/khe_hackathon/sign_images/'
    
    sign_language_dict = {
        'A': 'a.jpg',
        'B': 'b.jpg',
        'C': 'c.jpg',
        'D': 'd.jpg',
        'E': 'e.jpg',
        'F': 'f.jpg',
        'G': 'g.jpg',
        'H': 'h.jpg',
        'I': 'i.jpg',
        'J': 'j.jpg',
        'K': 'k.jpg',
        'L': 'l.jpg',
        'M': 'm.jpg',
        'N': 'n.jpg',
        'O': 'o.jpg',
        'P': 'p.jpg',
        'Q': 'q.jpg',
        'R': 'r.jpg',
        'S': 's.jpg',
        'T': 't.jpg',
        'U': 'u.jpg',
        'V': 'v.jpg',
        'W': 'w.jpg',
        'X': 'x.jpg',
        'Y': 'y.jpg',
        'Z': 'z.jpg',
        ' ': 'space.jpg',
    }
    
    
    def text_to_sign_language(text):
        # ...
        
        sign_language_images = []
        
        
        for letter in text.upper():
            if letter in sign_language_dict:
                image_filename = sign_language_dict[letter]
                image_path = os.path.join(images_folder, image_filename)
                try:
                    img = Image.open(image_path)
                    sign_language_images.append(img)
                except FileNotFoundError:
                    print(f"Image not found for letter: {letter}")
                    
        return sign_language_images
    	
    	
    
    
        # Translate text to sign language images
    translated_images = text_to_sign_language(text)

    # Create a figure and axis for the animation
    fig, ax = plt.subplots()




    # Function to update the animation frame
    def update(frame):
        im.set_data(translated_images[frame])
        return [im]
    


    # Initialize the animation with the first image
    im = ax.imshow(translated_images[0])

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(translated_images), interval=250, blit=True)

    # Save the animation as HTML
    buffer = BytesIO()
    ani.save(buffer, writer='html', fps=4)
    buffer.seek(0)
    html_animation = buffer.read().decode('utf-8')

    return html_animation





@app.route('/text_to_sign_language', methods=['POST'])
def text_to_sign_languagee():
    if request.method == 'POST':
        text = request.form['text']
        animation_html = text_to_sign_language_animation(text)
        return jsonify({"animation": animation_html})

if __name__ == '__main__':
    app.run(debug=True)
                    