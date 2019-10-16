#!/usr/bin/env python3.7
import sys
import os 
from students2.__init__ import create_app

if __name__=='__main__':
    try:
        os.environ['FLASK_APP'] = 'students2'
        os.environ['FLASK_ENV'] = 'dev'
        port=sys.argv[1]
    except Exception:
        print("Usage: python3.7 wsgi.py <port number>")
        print("Usage: ./ wsgi.py <port number>")
        sys.exit(0)
    app=create_app()
    app.run(port=port)
