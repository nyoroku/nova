import subprocess
import os

def export_utf8():
    # Use the local virtualenv python
    python_exe = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = "python" # fallback
        
    cmd = [
        python_exe, "manage.py", "dumpdata", 
        "--natural-foreign", "--natural-primary",
        "-e", "contenttypes", "-e", "auth.permission",
        "--indent", "2"
    ]
    
    try:
        # Run the command and capture output as bytes
        result = subprocess.run(cmd, capture_line_output=False, capture_output=True, check=True)
        
        # Write the bytes directly to file to avoid Windows encoding interference
        # Or decode as utf-8 and write with utf-8 encoding explicitly
        with open("sample_data.json", "w", encoding="utf-8", newline='') as f:
            # We assume dumpdata sends utf-8 or it can be decoded
            f.write(result.stdout.decode('utf-8'))
            
        print("Successfully exported sample_data.json in UTF-8 (No BOM)")
    except subprocess.CalledProcessError as e:
        print(f"Error during dumpdata: {e.stderr.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    export_utf8()
