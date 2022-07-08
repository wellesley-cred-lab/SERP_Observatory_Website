import os
import logging
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
#from flaskr.db import get_db
from flask.cli import with_appcontext

bp = Blueprint('categories', __name__)


@bp.route('/')
def index():
    with current_app.app_context():
        os.chdir(bp.root_path+"/static/SERP_Collection")
        categories = os.listdir()
        for category in categories:
            if category.startswith('.'):
                categories.remove(category)
        logging.warning(categories)
        

    
    
    
    
    

    # # execute the command to fetch all the data from the table emp
    # crsr.execute("SELECT * FROM organic")
    
    # # store all the fetched data in the ans variable
    # ans = crsr.fetchall()
    # logging.warning(ans)

    return render_template('categories/index.html', title='Home', categories=categories)

