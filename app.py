from flask import Flask, jsonify, request, send_from_directory
import threading
import subprocess
import pymongo
import json
import os

app = Flask(__name__)

@app.route('/')
def serve_streamlit():
    return send_from_directory('static', 'index.html')

@app.route('/addTask', methods=['POST'])
def addATask():
    try:
        if request.method == 'POST':
            data = request.json  # Parse JSON data from request body
            task_name = data.get('task_name')
            task_details = data.get('task_details')
            due_date = data.get('due_date')
            status = data.get('status')

            
            if task_name is None or task_details is None or due_date is None:
                return jsonify({'error': 'Missing form fields'}), 400
                
            # Here you can add code to process the task data
            # For example, save it to a database or perform other actions
            # Connect to MongoDB
            client = pymongo.MongoClient("mongodb+srv://taskmanager:QZdYRbZwA45j7bUv@cluster0.uuvuidq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            # Select database
            db = client["task_manager"]

            # Select collection
            collection = db["task_list"]

            # Insert data into collection
            insert_result = collection.insert_one({
                "task_name": task_name,
                "task_details": task_details,
                "due_date": due_date,
                "status" : status
            })

            # Print inserted document ID
            print("Inserted document ID:", insert_result.inserted_id)


            return jsonify({
                'task_name': task_name,
                'task_details': task_details,
                'due_date': due_date
            })
        else:
            return jsonify({"error": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/getTask', methods=['GET'])
def getATask():
    try:
        if request.method == 'GET':
        
            client = pymongo.MongoClient("mongodb+srv://taskmanager:QZdYRbZwA45j7bUv@cluster0.uuvuidq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            # Select database
            db = client["task_manager"]

            # Select collection
            collection = db["task_list"]
            # Fetch all documents from collection
            all_documents = list(collection.find())  # Convert cursor to list
            
            # Convert documents to JSON format
            json_docs = []
            for doc in all_documents:
                # Convert ObjectId to string
                doc['_id'] = str(doc['_id'])
                json_docs.append(doc)
            
            return jsonify(json_docs)  # Return JSON response
        else:
            return jsonify({"error": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def run_streamlit():
    # Start Streamlit app
    streamlit_script = 'src/ui/manage.py'
    command = f"streamlit run {streamlit_script} --server.port 8505"
    process = subprocess.Popen(command, shell=True)
    process.communicate()

if __name__ == '__main__':
    # Run Streamlit in a separate thread
    thread = threading.Thread(target=run_streamlit)
    thread.start()

    # Run Flask app
    app.run(port=5000, debug=True)
