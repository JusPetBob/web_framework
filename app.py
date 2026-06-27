import core, os
from flask import Flask,current_app,Response

app = Flask(__name__)
print("Creating EventHandler in PID", os.getpid())
app.eventhandler = core.EventHandler("recv")

@app.route("/")
def event_handler():
    def stream():
        for x in current_app.eventhandler.itterate_events():
            print(x)
            yield f"data: {x.get("data")}\n\n"
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    try:
        app.run(port=8000,debug=True,use_reloader=True)
    finally:
        app.eventhandler.close()