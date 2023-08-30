from flask import Flask, Response
import subprocess
import re
app = Flask(__name__)
@app.route('/metrics')
def metrics():
    result = subprocess.run(["C:\lmutil.exe", "lmstat", "-a", "-c", "C:\license.dat"], capture_output=True, text=True)
    output = result.stdout
    metrics = {}
    for line in output.split("\n"):
        match = re.match(r'Users of ([\w]*):  \(Total of ([\d]*) license issued;  Total of ([\d]*) licenses in use\)', line)
        if match:
            feature, total, used = match.groups()
            metrics[f'flexlm_{feature}_total'] = total
            metrics[f'flexlm_{feature}_used'] = used
    prom_output = "\n".join(f"{k} {v}" for k, v in metrics.items())
    # return Response("prom_output", mimetype='text/plain')
    return Response (prom_output)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)