""" Admin Blueprint """

from flask import Blueprint, current_app

from ..config import Config

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

from .importer import * # NOQA
