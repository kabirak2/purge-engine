import subprocess
import time
import webview
import psutil
import os
import sys

STREAMLIT_PORT = 8501
STREAMLIT_URL = f"http://localhost:{STREAMLIT_PORT}"


def start_streamlit():
    """
    Starts the Streamlit app as a background process.
    """
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "ui/app.py",
            "--server.port",
            str(STREAMLIT_PORT),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
    )


def wait_for_streamlit():
    """
    Wait until Streamlit server is reachable.
    """
    import socket

    for _ in range(50):
        try:
            with socket.create_connection(("localhost", STREAMLIT_PORT), timeout=0.5):
                return
        except OSError:
            time.sleep(0.2)

    raise RuntimeError("Streamlit did not start in time")


def stop_process_tree(pid):
    """
    Ensure Streamlit shuts down cleanly.
    """
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass


def main():
    streamlit_process = start_streamlit()
    wait_for_streamlit()

    # Window created ONLY after server is ready
    window = webview.create_window(
        title="PURGE AI Console",
        url=STREAMLIT_URL,
        fullscreen=True,
        resizable=False,
    )

    webview.start(debug=False)
    stop_process_tree(streamlit_process.pid)



if __name__ == "__main__":
    main()
