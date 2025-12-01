# -*- coding: utf-8 -*-

"""
------------------------------------------------

describe: 
    App manual entry
        dev: python app.py
        prod: supervisor>uvicorn startup(PROD)

base_info:
    __author__ = PyGo
    __time__ = 2025/11/25 21:39
    __version__ = v.1.0.0
    __mail__ = gaoming971366@163.com
    __blog__ = www.pygo2.top
    __project__ = fastslot-api
    __file_name__ = app.py

usage:
    
design:

reference urls:

python version:
    python3


Enjoy the good life every day！！!
Life is short, I use python.

------------------------------------------------
"""
import uvicorn


"""========================================================================================="""
# manual startup(DEV)
if __name__ == "__main__":
    config = uvicorn.Config("deploy:app",
                            host="127.0.0.1",
                            port=22222,
                            log_level="debug",
                            reload=True
                            )
    server = uvicorn.Server(config)
    server.run()
"""========================================================================================="""
