"""
This script provides a Flask-based web service that fetches random quotes from a MongoDB database
and the number of requests using Redis. It includes routes for serving quotes and error handling.
"""

from flask import Flask, jsonify
from pymongo import MongoClient
import redis
import pymongo.errors
from redis import exceptions as redis_exceptions

def get_db():
    """
    Connects to the MongoDB database and returns the database object.
    """
    client = MongoClient(
        host='my-mongo-container',
        port=27017,
        username='jayesh',
        password='jayesh',
        authSource="admin"
    )
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

    def display_quote(self):
        """
        Returns the formatted quote as a string.
        """
        return f'"{self.quote}" - {self.by}'

    def is_valid(self):
        """
        Checks if the quote is valid (non-empty).
        """
        return bool(self.quote) and bool(self.by)

app = Flask(__name__)

@app.route("/api/quote")
def get_quote():
    """
    Retrieves a random quote from MongoDB and returns it in a JSON response.
    Also tracks the number of requests using Redis.
    """
    db = ""
    try:
        db = get_db()
        r = get_redis()

        # Fetching and incrementing the request count in Redis
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

        app.logger.info("Result type: %s", type(result))
        app.logger.info("Result: %s", result)

        if result:
            return jsonify({"quote": result['quote'], "by": result['author'], "count": count})

        return jsonify({"quote": "No quotes found", "by": "Unknown", "count": count})

    except (pymongo.errors.PyMongoError, redis_exceptions.RedisError) as e:
        app.logger.error("Error occurred: %s", e)
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if isinstance(db, MongoClient):
            db.close()

@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 errors (resource not found).
    """
    app.logger.error("404 Error: %s", e)
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
