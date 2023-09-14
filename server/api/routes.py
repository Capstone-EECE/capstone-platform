"""
Collection of Flask API route functions
https://realpython.com/flask-blueprint/
"""
import functools
import logging
import os
from datetime import datetime

from flask import Blueprint

endpoints = Blueprint("endpoints", __name__)


@endpoints.get("/")
def test_route():
    return ("hello", 200)


@endpoints.get("/<id>")
def test_param(id: str):
    return (id, 200)
