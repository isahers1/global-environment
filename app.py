from flask import Flask, render_template, request
import subprocess



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/proof', methods=['POST'])
def proof():
    proof_name = request.form['proof_name']
    group_name = request.form['group_name']
    group_operation = request.form['group_operation']
    goal = request.form['goal']
    assumption = request.form['assumption']
    return render_template('proof.html', proof_name=proof_name, group_name=group_name, group_operation=group_operation, goal=goal, assumption=assumption)

@app.route("/run_code", methods=["POST"])
def run_code():
    code = request.form["code"]
    try:
        result = subprocess.run(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stderr:
            return result.stderr
        else:
            return result.stdout
    except Exception as e:
        return str(e)
   

if __name__ == "__main__":
    app.run()