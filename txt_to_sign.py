from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation




# Define the path to your sign language alphabet images folder
images_folder = r'/home/keithmartin/Desktop/khe_hackathon/sign_images/'


# Create a figure and axis for the animation
fig, ax = plt.subplots()



# Define a mapping from text to image filenames
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
    ' ': 'space.jpg',  # Define a blank image for spaces
}



#image_paths = []

# Function to translate text to sign language images
def text_to_sign_language(text):
    # Create a list to store the sign language images
    sign_language_images = []

    for letter in text.upper():
        if letter in sign_language_dict:
            image_path = images_folder + sign_language_dict[letter]


            #image_paths.append(image_path)


            try:
                img = Image.open(image_path)
                sign_language_images.append(img)
            except FileNotFoundError:
                print(f"Image not found for letter: {letter}")

    return sign_language_images





#def load_image(filename):
#    for image_path in image_paths: 
#        try:
#            return Image.open(image_path)
#        except FileNotFoundError:
#            print(f"Image not found: {filename}")
#        return None





# Translate text to sign language images
text_to_translate = input("Enter text: ")
translated_images = text_to_sign_language(text_to_translate)


# Function to update the animation frame
def update(frame):
    im.set_data(translated_images[frame])
    return [im]


# Initialize the animation with the first image
im = ax.imshow(translated_images[0])


# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(translated_images), interval=250, blit=True)

# Display the animation
plt.axis("off")
plt.show()






# Concatenate and display the translated images using matplotlib
#if translated_images:
#    plt.figure(figsize=(12, 4))
#    total_width = sum(img.width for img in translated_images)
#    max_height = max(img.height for img in translated_images)
#    combined_image = Image.new('RGB', (total_width, max_height))
#
#    x_offset = 0
#    for img in translated_images:
#        combined_image.paste(img, (x_offset, 0))
#        x_offset += img.width
#
#    plt.imshow(combined_image)
#    plt.axis('off')  # Turn off axis labels and ticks
#    plt.show()