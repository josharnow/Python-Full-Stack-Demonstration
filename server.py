from flask_app import app
from flask_app.controllers import login, companies
# from waitress import serve

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    # serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)    # Run the app in debug mode.
    # app.run(debug=True) should be the very last statement! 