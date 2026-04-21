import sys
import traceback

with open("error_output.txt", "w", encoding="utf-8") as f:
    try:
        from app.main import app
        f.write("Backend imports OK\n")
        print("OK")
    except Exception as e:
        tb = traceback.format_exc()
        f.write(tb)
        print("FAILED - see error_output.txt")
