import os
import tempfile
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_handler():
    data = request.json

    if 'urls' not in data:
        return jsonify({'error': 'Missing "urls" parameter in the request'}), 400

    urls = data['urls']

    # Set up temporary directory to store scraped data
    temp_dir = tempfile.mkdtemp()

    # Run the Scrapy script in a separate process
    try:
        subprocess.check_output(['python', 'script.py', '--urls', ','.join(urls), '--output', f'{temp_dir}/output.json'])
        
        # Read the scraped data from the output file
        with open(f'{temp_dir}/output.json', 'r') as file:
            result = file.read()

    except subprocess.CalledProcessError as e:
        print(f"Error executing Scrapy script: {e}")
        return jsonify({'error': f"Error executing Scrapy script: {e}"}), 500

    finally:
        # Clean up temporary directory
        subprocess.run(['rm', '-r', temp_dir], check=False)

    return jsonify({'data': result})

if __name__ == '__main__':
    app.run(debug=True)
