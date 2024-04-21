from flask import Flask, jsonify, request
import base64
import json
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://vision-durranis-projects.vercel.app", "methods": ["POST"]}})

openai.api_key = 'YOUR-OPENAI-KEY'

@app.route("/api/openAIVision", methods=['POST'])  
def openai_vision():
        
        data = request.json
        imageData = data.get('imageData')
        print(imageData)
        base64_image = imageData['imageData']
        include_color = imageData['include_colour']
        include_surrounding=imageData['include_surrounding']
        include_emotion=imageData['include_emotion']
        include_text=imageData['include_text']
        print(base64_image)
        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(base64_image)

        # Assuming 'readerURL' is expecting a URL, you can convert the bytes to a data URL
        data_url = f"data:image/jpeg;base64,{base64_image}"

        # Now you can use this data URL as the image URL
        image_url = data_url

        prompt_text = "What object is it? Just give the object name, don't give extra details. If it is a human, also tell the emotion of the human."
        if include_color:
            prompt_text += " If there is a color, please specify but don't give other details. Write in sentence form."
        if include_surrounding:
            prompt_text += " Also tell me the objects in the surrounding of the central object in sentence format"
        if include_emotion:
                prompt_text += " Also tell me the emotion of the central object in sentence format. if there is no human, ignore this part"
        if include_text:
                prompt_text += " Also tell me the text visible in the image "

        openai_response = openai.ChatCompletion.create(
            max_tokens=1000,
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "low"
                            },
                        },
                    ],
                },
            ],
        )

        vision_response_text = openai_response['choices'][0]['message']['content']

        return jsonify({
            'vision_response': vision_response_text,
        })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4040)
