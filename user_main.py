#!/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import Literal, Any, Dict
from flask import Flask, jsonify, request, session, Response, current_app as ca
from flask_session import Session
from db import MYQL
import uuid, json, base64, hashlib, ipaddress

from flask_cors import CORS, cross_origin
from flask import jsonify
from datetime import date

app = Flask("Grid Eye Central")
app.url_map.strict_slashes = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_THRESHOLD"] = 50
app.config['JSON_SORT_KEYS'] = False
Session(app)
cors = CORS(app, resources={r"*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}}, supports_credentials=True)

MTEL_STORE ="/opt/log/mtel"
STEL_STORE ="/opt/log/stel"
CONF_STORE ="/opt/etc"
VERSION = "/opt/version.ini"

from new_user_audit import user_audit

@app.after_request
def log_activity(response):
    # print('session_id', session.get('_permanent'))
    # request_object = user_audit(request, session, ca, response)
    user_audit(request, session, ca, response)
    # logger.info(request_object)
    return response

## Below backends code for web ##