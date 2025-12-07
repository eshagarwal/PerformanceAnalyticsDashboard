from app import app

if __name__ == "__main__":
    app.run(port=8080, dev_tools_ui=False, debug=False, host="127.0.0.1")