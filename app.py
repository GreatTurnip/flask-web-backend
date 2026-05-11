from flask import Flask,jsonify,request
import sqlite3
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    
    """)
    conn.commit()
    conn.close()
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"
@app.route("/status",methods=['GET'])
def status():
    return jsonify(
        {
            "total_posts": len(posts),
            "server":"Flask_API",
            "status":"active"
        }
    )
@app.route("/posts",methods=["POST"])
def create_post():
    data = request.get_json()
    if not data.get("title") or not data.get("content"):
        return jsonify({"error":"Title and Content are missing"})
    new_post={
        "id": len(posts)+1,
        "title": data["title"],
        "content": data["content"]
    }
    posts.append(new_post)
    return jsonify(new_post),201
@app.route("/posts", methods=["GET"])
def get_posts():
    limit = request.args.get("limit")
    #here i will create a connection to db and fetch data from the db
    conn = get_db() #open connection
    cursor = conn.execute("SELECT * FROM posts") #runs and sql command
    rows = cursor.fetchall() #fetches all the output
    conn.close() #close the connection and the result is stored in rows

    posts = [dict(row) for row in rows]
    if limit:
        limit = int(limit)
        return jsonify(posts[:limit])
    return jsonify(posts)
@app.route("/posts/<int:id>",methods=["PUT"])
def update_post(id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error":"Invalid Json"}),400
    if not data.get("title") or not data.get("content"):
        return jsonify({"error": "Title and content required"}), 400
    for post in posts:
        if post["id"]== id:
            post["title"]= data["title"]
            post["content"]= data["content"]
            return jsonify(post),200
    return jsonify({"error":"Post not found"}), 404
@app.route("/posts/<int:id>",methods=["DELETE"])
def delete_post(id):
    for post in posts:
        if post["id"]==id:
            posts.remove(post)
            return jsonify({"message":"Post deleted"}),200
    return jsonify({"error":"Post not found"}), 404
if __name__ == "__main__":
    init_db()
    app.run()