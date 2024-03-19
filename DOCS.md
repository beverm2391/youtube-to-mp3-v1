> [!WARNING]  
> These docs are not updated (yet)... sorry I've been busy

### Initial Setup
1. **Create a Virtual Environment:**  
    Run `python3 -m venv venv`. This step is needed only once to set up a virtual environment.

2. **Activate the Virtual Environment:**  
    Use `source venv/bin/activate` to activate the virtual environment. You'll need to do this each time you start a new terminal session.
    - **Note:** Ensure you're using the Python interpreter from this virtual environment. If you're using VSCode, You can switch interpreters by clicking on the Python version displayed in the bottom right corner of the window.

3. **Install Dependencies:**  
    Run `pip install -r requirements.txt` to install the required Python packages. This also needs to be done only once.

#### Running the Converter

4. **Run Tests:**  
    Before starting the server, execute `pytest` from the root directory of the project to confirm that everything is set up correctly.

5. **Start the Server:**  
    Use `uvicorn main:app --reload` to start the FastAPI server.

6. **Download MP3:**  
    Execute `python3 get_mp3.py "YOUR_URL_HERE"` to download the MP3 file from the given YouTube URL. Make sure to put it in quotes so that special characters like `?` don't mess up the shell.

To stop the server, use `Ctrl+C`.

#### Notes
- Conversion may take some time, especially for longer videos.
- You can monitor the conversion progress in the terminal window where you ran `uvicorn main:app --reload`.