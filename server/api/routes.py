"""
Collection of Flask API route functions
https://realpython.com/flask-blueprint/
"""
import functools
import logging
import os
from datetime import datetime

from flask import Blueprint

from ..core.mock_request import get_points

endpoints = Blueprint("endpoints", __name__)


@endpoints.get("/")
def test_route():
    return ("hello", 200)


@endpoints.get("/points")
def test_param():
    return get_points()
