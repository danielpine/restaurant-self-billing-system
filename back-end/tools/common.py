import os
import sys
sys.path.append("..")
sys.path.append(".")


def getPythonDataBase():
    profile = os.getenv('PY_DB_TP')
    if profile:
        return profile
    else:
        return 'dev'
