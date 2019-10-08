import sys
from students2.__init__ import create_app

if __name__=='__main__':
    try:
        port=sys.argv[1]
    except:
        print("Usage: python3.7 wsgi.py <port number>")
    app=create_app()
    app.run(port=port)
