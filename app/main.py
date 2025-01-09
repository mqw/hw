from flask import Flask
import srv

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return "OK", 200

app.add_url_rule('/reverse', view_func=srv.reverse)
app.add_url_rule('/restore', view_func=srv.restore)

if __name__ == '__main__':
    app.run(debug=True)
