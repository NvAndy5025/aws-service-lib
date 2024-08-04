from flask import Flask, request, jsonify
from flask_cors import CORS
import awsservice

app = Flask(__name__)
CORS(app)

@app.route('/api/deploy-ec2', methods=['POST'])
def deploy_ec2():
    roleArn = request.args.get("roleArn")
    sessionName = request.args.get("sessionName")
    region = request.args.get("region")
    
    try:
        result = awsservice.deploy_ec2(roleArn, sessionName, region)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)