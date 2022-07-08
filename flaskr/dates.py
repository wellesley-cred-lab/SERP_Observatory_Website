import os
import logging
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


bp = Blueprint('dates', __name__)

@bp.route('/<category>')
def date(category):
    os.chdir(bp.root_path+f"/SERP_Collection/{category}")
    dateFolders = os.listdir()
    datesList = []
    # Place the date folders in order (Most recent on top)
    for date in dateFolders:
        if not date.startswith('.'):
            dateComponents = date.split("-")
            datesList.append({'month':int(dateComponents[0]), 'day':int(dateComponents[1]), 'year':int(dateComponents[2])})
        datesList = sorted(datesList, key=lambda x: (x['year'], x['month'], x['day']),reverse=True)
        sortedDates = []
        for d in datesList:
            sortedDates.append(str(d['month'])+'-'+str(d['day'])+'-'+str(d['year']))
        dateFolders = sortedDates 
    for date in dateFolders:
        if not date.startswith('.'):
            logging.warning(date)
    logging.warning(category)
    logging.warning(dateFolders)
    return render_template('dates/dateList.html', title='Home', category=category, dateFolders=dateFolders)   
        
    #logging.warning(categories)
    