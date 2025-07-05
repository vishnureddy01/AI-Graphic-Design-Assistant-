import os
from flask import Flask, send_from_directory, request, jsonify, send_file
from PIL import Image, ImageDraw
import random
import io
import base64
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'static/uploads'
try:
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        logger.info(f"Created directory: {UPLOAD_FOLDER}")
    if not os.access(UPLOAD_FOLDER, os.W_OK):
        logger.error(f"Directory {UPLOAD_FOLDER} is not writable")
        raise PermissionError(f"Directory {UPLOAD_FOLDER} is not writable")
except Exception as e:
    logger.error(f"Failed to set up upload directory: {e}")
    raise

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Existing design endpoints (Abstract Classic, Spiral, Wave, Fractal, Grid)
@app.route('/api/abstract_classic')
def abstract_classic():
    elements = [
        {"type": "background", "color": [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]},
        {"type": "circle", "x": random.randint(100, 500), "y": random.randint(100, 300), "size": random.randint(50, 150), "color": [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], "alpha": random.uniform(0.5, 1)},
        {"type": "rect", "x": random.randint(100, 500), "y": random.randint(100, 300), "size": random.randint(50, 150), "color": [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], "alpha": random.uniform(0.5, 1), "rotation": random.randint(0, 360)}
    ]
    return jsonify({"elements": elements})

@app.route('/api/abstract_spiral')
def abstract_spiral():
    elements = [
        {"type": "background", "color": [random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)]},
        {"type": "circle", "x": 300, "y": 200, "size": 50, "gradient": [[255, 0, 0], [0, 0, 255]], "alpha": 0.8},
        {"type": "circle", "x": 300, "y": 200, "size": 100, "gradient": [[0, 255, 0], [255, 0, 255]], "alpha": 0.6, "rotation": 45}
    ]
    return jsonify({"elements": elements})

@app.route('/api/abstract_wave')
def abstract_wave():
    elements = [
        {"type": "background", "color": [200, 220, 255]},
        {"type": "line", "x1": 0, "y1": 100, "x2": 600, "y2": 100, "color": [0, 100, 255], "weight": 10},
        {"type": "line", "x1": 0, "y1": 200, "x2": 600, "y2": 200, "color": [0, 100, 255], "weight": 10}
    ]
    return jsonify({"elements": elements})

@app.route('/api/abstract_fractal')
def abstract_fractal():
    elements = [
        {"type": "background", "color": [0, 0, 0]},
        {"type": "triangle", "x": 300, "y": 200, "size": 100, "color": [255, 255, 0], "alpha": 0.7, "rotation": 0},
        {"type": "triangle", "x": 300, "y": 200, "size": 50, "color": [255, 0, 0], "alpha": 0.7, "rotation": 120}
    ]
    return jsonify({"elements": elements})

@app.route('/api/abstract_grid')
def abstract_grid():
    elements = [
        {"type": "background", "color": [255, 255, 255]},
        {"type": "rect", "x": 100, "y": 100, "size": 50, "color": [200, 200, 200], "alpha": 1},
        {"type": "rect", "x": 200, "y": 200, "size": 50, "color": [200, 200, 200], "alpha": 1}
    ]
    return jsonify({"elements": elements})

# Generate image based on text input
@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    subject = data.get('subject', '').lower()
    animals = ['bird', 'dog', 'fish', 'cat', 'horse', 'rabbit', 'tiger', 'lion', 'elephant', 'bear', 'fox', 'wolf', 'deer', 'snake', 'turtle']
    
    if subject not in animals:
        return jsonify({"error": f"Subject must be one of: {', '.join(animals)}"}), 400
    
    elements = [
        {"type": "background", "color": [random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)]},
        {"type": "ellipse", "x": 300, "y": 200, "width": 100, "height": 150, "color": [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], "alpha": 0.8}
    ]
    return jsonify({"elements": elements})

# Export design
@app.route('/api/export', methods=['POST'])
def export_design():
    data = request.get_json()
    format = data.get('format')
    
    if format in ['png', 'jpg']:
        img_data = data.get('image').split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img = Image.open(io.BytesIO(img_bytes))
        output = io.BytesIO()
        img.save(output, format=format.upper())
        output.seek(0)
        return send_file(output, mimetype=f'image/{format}')
    elif format == 'svg':
        elements = data.get('elements')
        svg_content = '<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">'
        for el in elements:
            if el['type'] == 'background':
                svg_content += f'<rect width="600" height="400" fill="rgb({el["color"][0]},{el["color"][1]},{el["color"][2]})"/>'
            elif el['type'] == 'text':
                svg_content += f'<text x="{el["x"]}" y="{el["y"]}" font-size="{el["size"]}" fill="rgb({el["color"][0]},{el["color"][1]},{el["color"][2]})" text-anchor="middle" dominant-baseline="middle">{el["content"]}</text>'
        svg_content += '</svg>'
        return send_file(io.BytesIO(svg_content.encode()), mimetype='image/svg+xml')
    
    return jsonify({"error": "Invalid format"}), 400

# Reference images
@app.route('/api/references')
def references():
    refs = [
        {"style": "Bird", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/bird-8019604_1280.jpg"},
        {"style": "Dog", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/dog-8019605_1280.jpg"},
        {"style": "Fish", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/fish-8019606_1280.jpg"},
        {"style": "Cat", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/cat-8019607_1280.jpg"},
        {"style": "Horse", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/horse-8019608_1280.jpg"},
        {"style": "Rabbit", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/rabbit-8019609_1280.jpg"},
        {"style": "Tiger", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/tiger-8019610_1280.jpg"},
        {"style": "Lion", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/lion-8019611_1280.jpg"},
        {"style": "Elephant", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/elephant-8019612_1280.jpg"},
        {"style": "Bear", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/bear-8019613_1280.jpg"},
        {"style": "Fox", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/fox-8019614_1280.jpg"},
        {"style": "Wolf", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/wolf-8019615_1280.jpg"},
        {"style": "Deer", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/deer-8019616_1280.jpg"},
        {"style": "Snake", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/snake-8019617_1280.jpg"},
        {"style": "Turtle", "url": "https://cdn.pixabay.com/photo/2023/05/26/12/40/turtle-8019618_1280.jpg"}
    ]
    return jsonify({"references": refs})

# Image upload endpoint
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    logger.debug("Received upload request")
    if 'file' not in request.files:
        logger.error("No file provided in request")
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        logger.error("No file selected")
        return jsonify({"error": "No file selected"}), 400
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            filename = f"upload_{random.randint(1000, 9999)}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logger.info(f"Saved file to {filepath}")
            # Verify file exists
            if not os.path.exists(filepath):
                logger.error(f"File {filepath} was not saved")
                return jsonify({"error": "Failed to save file"}), 500
            return jsonify({"image_url": f"/{filepath}"})
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return jsonify({"error": f"Server error: {str(e)}"}), 500
    logger.error(f"Invalid file format: {file.filename}")
    return jsonify({"error": "Invalid file format, use PNG or JPG"}), 400

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)