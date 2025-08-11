import os

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from flask import Flask, render_template


QDRANT_HOST = os.environ['QDRANT_HOST']

client = QdrantClient(url=QDRANT_HOST)

app = Flask(__name__)

@app.route('/init')
def init_db():
    """
    Init the QDrant DB with a simple collection. 
    """

    # Create a collection
    client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=4, distance=Distance.DOT),
    )
    
    # Add a vector
    operation_info = client.upsert(
        collection_name="test_collection",
        wait=True,
        points=[
            PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
            PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
            PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
            PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
            PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
            PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
        ],
    )
    
    print(operation_info)

@app.route('/')
def index():
    """
    This route performs a Qdrant query and displays the results on an HTML page.
    """
    try:
        # Perform the Qdrant search
        # Ensure 'test_collection' exists and has data
        search_result = client.query_points(
            collection_name="test_collection",
            query=[0.2, 0.1, 0.9, 0.7],
            with_payload=True, # Set to True if you want to display payload data
            with_vectors=True, # return the vectors
            limit=3
        ).points

        print(search_result)

        # Extract the IDs, vectors, and city from payload for display
        points_data = []
        for point in search_result:
            city_name = point.payload.get("city", "N/A") if point.payload else "N/A" # Safely get city
            points_data.append({
                "id": point.id,
                "vector_preview": str(point.vector)[:50] + "..." if point.vector else "N/A",
                "city": city_name # Pass the city data
            })

        # Render the HTML template, passing the results
        return render_template('index.html', points=points_data)

    except Exception as e:
        # Basic error handling for display
        error_message = f"An error occurred: {e}"
        print(f"Error: {e}") # Log the full error to console
        return render_template('index.html', error=error_message)
    

if __name__ == '__main__':
    # Run the Flask app on localhost:3000
    app.run(host='0.0.0.0', port=3000, debug=True)
