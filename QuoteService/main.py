from flask import Flask, jsonify
from pymongo import MongoClient
import redis

def get_db():
    """
    Connects to the MongoDB database and returns the database object.
    """
    client = MongoClient(host='my-mongo-container',
                         port=27017,
                         username='jayesh',
                         password='jayesh',
                         authSource="admin")
    db = client["quote_db"]
    return db

def get_redis():
    """
    Connects to the Redis server and returns the Redis client object.
    """
    r = redis.Redis(host='my-redis-server', port=6379)
    return r

class Quote:
    """
    Represents a Quote object.
    """
    def __init__(self, quote, by):
        self.quote = quote
        self.by = by

app = Flask(__name__)

@app.route("/api/quote")
def quote():
    """
    Retrieves a random quote from MongoDB and returns it in a JSON response.
    Also tracks the number of requests using Redis.
    """
    db = ""
    try:
        db = get_db()
        r = get_redis()

        count = r.get("count")
        if count is None:
            r.set("count", 1)
            count = 0
        else:
            count = int(count) + 1
            r.set("count", count)

        # Aggregation pipeline to fetch a random quote
        pipe2 = [{'$sample': {'size': 1}}]
        result = db.quote_tb.aggregate(pipeline=pipe2).try_next()

        app.logger.info(f"Result type: {type(result)}")
        app.logger.info(f"Result: {result}")

        if result:
            return jsonify({"quote": result['quote'], "by": result['author'], "count": count})
        else:
            return jsonify({"quote": "No quotes found", "by": "Unknown", "count": count})

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if isinstance(db, MongoClient):
            db.close()

@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 errors (resource not found).
    """
    app.logger.error(f"404 Error: {e}")
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
