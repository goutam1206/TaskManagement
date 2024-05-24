from flask import Flask, jsonify, request, send_from_directory
import threading
import subprocess
import pymongo
import json
from bson import ObjectId
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
            # Connect to MongoDB
            client = pymongo.MongoClient("mongodb+srv://taskmanager:QZdYRbZwA45j7bUv@cluster0.uuvuidq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            # Select database
            db = client["task_manager"]

            # Select collection
            collection = db["task_list"]
            # Fetch all documents from collectionclear
            all_documents = list(collection.find())
            # Convert ObjectId to string in each document
            for doc in all_documents:
                doc['_id'] = str(doc['_id'])

            # Convert documents to JSON format
            json_docs = all_documents  # bson.json_util.dumps handles ObjectId serialization
            
            return json_docs, 200  # Return as JSON response with HTTP status code 200
        else:
            return jsonify({"error": "Method not allowed"}), 405
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update operation
@app.route('/update_task', methods=['POST'])
def update_task():
    task_id = request.json.get('task_id')
    updated_task_details = request.json.get('updated_task_details')
    client = pymongo.MongoClient("mongodb+srv://taskmanager:QZdYRbZwA45j7bUv@cluster0.uuvuidq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    # Select database
    db = client["task_manager"]

    # Select collection
    collection = db["task_list"]

    if task_id and updated_task_details:
        # Update the task in the database
        result = collection.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task_details})
        if result.modified_count == 1:
            return jsonify({'message': 'Task updated successfully'})
        else:
            return jsonify({'error': 'Failed to update task'}), 500
    else:
        return jsonify({'error': 'Missing task ID or updated task details'}), 400

# Delete operation
@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.json.get('task_id')
    client = pymongo.MongoClient("mongodb+srv://taskmanager:QZdYRbZwA45j7bUv@cluster0.uuvuidq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    # Select database
    db = client["task_manager"]

    # Select collection
    collection = db["task_list"]
    if task_id:
        # Delete the task from the database
        result = collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete task'}), 500
    else:
        return jsonify({'error': 'Missing task ID'}), 400



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
