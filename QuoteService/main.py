from flask import Flask, jsonify
from pymongo import MongoClient, errors as mongo_errors
import redis

def get_db():
        client = MongoClient(host='my-mongo-container',
                             port=27017,
                             username='jayesh',
                             password='jayesh',
                             authSource="admin")
        db = client["quote_db"]
        return db
    
def get_redis():
        r = redis.Redis(host='my-redis-server', port=6379)
        return r
    
class Quote(object):
    def __init__(self, quote, by):
        self.quote = quote
        self.by = by

app = Flask(__name__)

@app.route("/api/quote")
def quote():
    db=""
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

        
        pipe2 = [{'$sample': {'size': 1}}]
        result = db.quote_tb.aggregate(pipeline=pipe2).try_next()

        
        app.logger.info(type(result))
        app.logger.info(result)

        if result:
            return jsonify({"quote": result['quote'], "by": result['author'], "count": count})
        else:
            return jsonify({"quote": "No quotes found", "by": "Unknown", "count": count})

    except:
        pass
    finally:
        if type(db)==MongoClient:
             db.close()


@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"404 Error: {e}")
    return jsonify({"message": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  
