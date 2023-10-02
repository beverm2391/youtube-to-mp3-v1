import argparse
import os
import requests
import string

def download_mp3_from_server(url: str):
    def _sanitize_filename(filename: str):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in filename if c in valid_chars)
    
    endpoint = "http://127.0.0.1:8000"

    try:
        test = requests.get(endpoint)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the FastAPI server. Make sure its running - use `uvicorn main:app --reload`")
        return

    
    response = requests.get(f"{endpoint}/convert", params={"url": url})

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return

    output_dir = "mp3s"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the mp3 filename from the Content-Disposition header
    content_disposition = response.headers.get("Content-Disposition")
    if not content_disposition:
        print("Error: Could not get the filename from the response.")
        return

    filename = content_disposition.split("filename=")[1].strip('"')

    output_path = os.path.join(output_dir, _sanitize_filename(filename))

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Saved {filename} to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download mp3 from FastAPI server")
    parser.add_argument("url", type=str, help="The URL of the YouTube video")
    args = parser.parse_args()

    download_mp3_from_server(args.url)