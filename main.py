from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)

client = Client("https://reach-vb-musicgen-prompt-upsampling.hf.space/--replicas/5u05c/")

@app.route('/')
def index():
    return 'Server is running'


@app.route('/prompt', methods=['GET'])
def generate_audio():
    try:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided."}), 400

        result = client.predict(prompt, api_name="/generate_audio")
        response_path, response_text = result
        url_with_path = "https://reach-vb-musicgen-prompt-upsampling.hf.space/--replicas/5u05c/file=" + response_path
        return jsonify({
            "audio_url": url_with_path,
            "generated_text": response_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)