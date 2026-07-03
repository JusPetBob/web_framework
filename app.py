import core, os, json
from flask import Flask,current_app,Response,render_template,send_file

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()

app = Flask(__name__)
print("Creating EventHandler in PID", os.getpid())
#app.eventhandler = core.EventHandler("recv")


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/api/storage/", defaults={"path": ""})
@app.route("/api/storage/<path:path>")
def storage(path:str):
    if path == "":
        return [i.removesuffix(":\\") for i in os.listdrives()]
    
    path = path.removesuffix("/")
    p = path.split("/")
    p[0] += ":"
    
    root_path = "\\".join(p).removesuffix("\\")
    
    if os.path.isfile(root_path):        
        return send_file(root_path, "text")
    
    else:
        root_path += "\\"
            
        l = [{"name":i, "path":"/api/storage/"+path+"/"+i, "type":"file" if os.path.isfile(root_path+i) else "folder"} for i in os.listdir(root_path)]
        
        return l


@app.route("/api/events")
def event_handler():
    def stream():
        for x in current_app.eventhandler.itterate_events():
            print(x)
            yield f"data: {x.get("data")}\n\n"
    
    return Response(stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    
    try:
        app.run(port=8000,debug=True,use_reloader=True)
    finally:
        if "eventhandler" in dir(app):
            app.eventhandler.close()