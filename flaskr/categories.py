import os
import logging
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)



bp = Blueprint('categories', __name__)

@bp.route('/')
def index():
    os.chdir(bp.root_path+"/SERP_Collection")
    categories = os.listdir()
    for category in categories:
        if category.startswith('.'):
            categories.remove(category)
    logging.warning(categories)
    return render_template('categories/index.html', title='Home', categories=categories)
