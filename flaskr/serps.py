import os
import sys
import json
import logging
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


bp = Blueprint('serps', __name__)

# Get components for each query to add class in html
def getClasses(path, date):
    result_classes = {}
    files = os.listdir(path)
    for f in files:
        if not f.startswith('.') and f.startswith(date):
            with open(f'{path}/{f}', 'r') as inFile:
                data = json.load(inFile)
            query = f.split('_')[1].split('.')[0]
            classes = set()
            for d in data:
                if d['type'] not in ['organic', 'unknown']:
                    classes.add(d['type'].replace(' ', ''))
            result_classes[query] = list(classes)
    return result_classes

@bp.route('/<category>/<date>')
def serps(category, date):
    os.chdir(bp.root_path+f"/SERP-database/")
    # serpFiles = os.listdir()
    # logging.warning(serpFiles)
    logging.warning(os.getcwd())
    
    # Get components for each query to add class in html
    result_classes = getClasses('for_comparing_serps', date)
    os.chdir("../")
    if not os.path.isdir("SERP-Components"):
        os.mkdir('SERP-Components')
    
    path1 = f"SERP-Components/components_{date}.json"
    with open(path1, "w") as outfile:
        json.dump(result_classes, outfile)

    with open(path1, "r") as inFile:
        day_components = json.load(inFile)
        #logging.warning(day_components)
    
    os.chdir("static/SERP_Collection")
    categories = os.listdir()
    #logging.warning(categories)
    querylist = []
    for c in categories:
        if c==category and not c.startswith('.'):
            alldates = os.listdir(c)
            for d in alldates:
                if d==date and not d.startswith('.'):
                    logging.warning(d)
                    queries_in_category_on_date = os.listdir(f"{c}/{d}")
                    logging.warning(queries_in_category_on_date)
                    for query_with_html in queries_in_category_on_date:
                        querylist.append(query_with_html.replace(".html",""))
                        

    
    
    logging.warning(querylist)
    name="test.html"

    return render_template('serps/serps-and-filters.html', title='Home', category=category, date=date, components=day_components, querylist = querylist)
        
    #logging.warning(categories)
