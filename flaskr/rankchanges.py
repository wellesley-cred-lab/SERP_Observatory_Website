import os
import json
import logging
import sqlite3
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from flaskr import *
from flaskr.db import get_db
from flask.cli import with_appcontext


bp = Blueprint('rankchanges', __name__)

# Load the json file containing changes for a specific query term between the specified previous and current date
# changes is a dictionary with key being organic and other components, value being a dictionary. 
#   For non-organic components, the key is change type and the value are appear or disappear. For organic components, the key is domain name and the value is another dictionary whose keys are title, pos1, pos2, change (amount), change_type.
def getChanges(filename):
    with open(bp.root_path+f"/SERP-database/changes/{filename}") as inFile:  #'filename is query_changebetween_date1_and_date2.json (e.g. Ace_changebetween_6-8-22_and_6-9-22.json')
        changes = json.load(inFile)
    organic = changes['organic']
    return getChangeScore(organic)

# Give each query a change score for the amount of changes it undergone between the two consecutive given dates
# appear if given 3 points; movement of less than 5 positions is given 1 point; movement of greater or equal to 5 positions is given 2 points
# the number of appear and movement are recorded
def getChangeScore (organic): 
    changeScore = 0
    appear = 0
    move = 0
    for item in organic:
        if organic[item]['change_type'] != 'unchanged':
            #print(organic[item]['change_type'])
            if organic[item]['change_type'] == 'appear':
                changeScore += 3
                appear+=1
            if organic[item]['change_type'] == 'move':
                move+=1
                if abs(organic[item]['change']) < 5:
                    changeScore += 1
                else:
                    changeScore += 2

    return changeScore, appear, move

'''
Generate the json file for the rank of the changes for all queries between the two given dates (rankforquerychangebetween_date1_and_date2.json) and sort the queries based on their change score (Higher score is ranked higher)
# scores is a dictionary with the key being the query and the value being a dictionary whose keys are score (change score), appear (count), and move (count).
# categories_date1 is all the category folders (Identities, Relationship) for the earlier date; categories_date2 is all the category folders (Identities, Relationship) for the later date;
# category is the individual category folder (e.g. Identities)
# files is all the query.html files inside each category folder; file is the individual query.html file
# query is the query term without of the .html extension
'''

def generateRankForQueryChangeBetweenTwoDates(date1, date2, category):
    
    scores = {}
    #categories_date1 = os.listdir(f'bp.root_path+f"/static/SERP_Collection/{category}/{date1}') # earlier date
    #categories_date2 = os.listdir(f'bp.root_path+f"/static/SERP_Collection/{category}/{date2}') # later date
    
    files = os.listdir(bp.root_path+f"/static/SERP_Collection/{category}/{date2}")
    files.sort()
    for file in files:
        if not file.startswith('.'): # ignore .DStore
            query = file[:file.index('.')] # get rid of the .html extension
            try:
                scores[query] = {}
                score, appear, move = getChanges(f"{query}_changebetween_{date1}_and_{date2}.json")
                scores[query]['score'] = score
                scores[query]['appear'] = appear
                scores[query]['move'] = move
            except: # if the query.html file is not in both date folders
                print("file not found")
                scores[query]['score'] = -1
                scores[query]['appear'] = -1
                scores[query]['move'] = -1

    
            #print(query)

    # for k_v in scores.items():
    #     print(k_v[1]['score'])
    #scores = sorted(scores,key=lambda x:scores[x]['score'], reverse=True)
    
    # Sort the queries based on their change score (Higher score is ranked higher)
    scores = dict(sorted(scores.items(), key=lambda k_v: k_v[1]['score'], reverse=True))
    i=1
    for item in scores:
        scores[item]['rank'] = i
        i+=1
    logging.warning(scores)

    return scores



@bp.route('/<category>/<date>/rankchanges')
def rankchanges(category, date):
    logging.warning(date)
    if date == '6-8-22':
        return '<h1>Nothing to Compare To</h1>'
    else:
        with current_app.app_context():
            crsr = get_db().cursor()

            ## Sort the folders based on date
            os.chdir(bp.root_path+f"/static/SERP_Collection/{category}")
            dateFolders = os.listdir()
            datesList = []
            # Place the date folders in order (Most recent on top)
            for d in dateFolders:
                if not d.startswith('.'):
                    dateComponents = d.split("-")
                    datesList.append({'month':int(dateComponents[0]), 'day':int(dateComponents[1]), 'year':int(dateComponents[2])})
                datesList = sorted(datesList, key=lambda x: (x['year'], x['month'], x['day']),reverse=True)
                sortedDates = []
                for d in datesList:
                    sortedDates.append(str(d['month'])+'-'+str(d['day'])+'-'+str(d['year']))
                dateFolders = sortedDates 
            logging.warning(dateFolders)
            date1 = date

            # Get the current and previous date
            for i in range(0,len(dateFolders)):
                if date == dateFolders[i]:
                    date0=dateFolders[i+1]
            logging.warning(date0)
            logging.warning(date1)

            # Go through each of the query.html file that exists in both dates
            # Access the domain entries for that query on the specific dates in the database
            files1 = os.listdir(f"{date0}")
            files2 = os.listdir(f"{date1}")
            files2.sort()
            for file2 in files2:
                if not file2.startswith('.') and file2 in files1: # ignores .DStore and checks that the query.html file exists in both /date/category folders
                    query = file2[:file2.index('.')]
                    
                    # execute the command to fetch all the domains for the query on the previous date from the table organic
                    crsr.execute(f"SELECT * FROM organic WHERE query='{query}' AND date='{date0}'")
                    # store all the fetched data in the organicDomainsDate0 variable
                    organicDomainsDate0 = crsr.fetchall()
                    logging.warning(organicDomainsDate0)

                    # execute the command to fetch all the domains for the query on the current date from the table organic
                    crsr.execute(f"SELECT * FROM organic WHERE query='{query}' AND date='{date1}'")
                    organicDomainsDate1 = crsr.fetchall()
                    logging.warning(organicDomainsDate1)

                    # Code from comparing_serps.py
                    # Find movement, appearance, disappearnace for organic results
                    organicResult = {}
                    for orgDomain0 in organicDomainsDate0:
                        url0 = orgDomain0[5]
                        position0 = orgDomain0[4]
                        domain0 = orgDomain0[3]
                        found=False
                        #logging.warning(orgDomain0[5])
                        for orgDomain1 in organicDomainsDate1:
                            url1 = orgDomain1[5]
                            position1 = orgDomain1[4]
                            domain1 = orgDomain1[3]
                            if url0 == url1: ### if the change type is move or unchanged
                                found = True
                                diff = position0-position1
                                d = {'change': diff, 'url': url0, 'pos1':position0, 'pos2':position1} 
                                if diff == 0:
                                    d['change_type'] = 'unchanged'
                                else:
                                    d['change_type'] = 'move'
                                organicResult[domain0] = d
                        if found == False: ## if results disappeared
                            organicResult[domain0] = {'url': url0, 'change_type': 'disappear'}
                    for orgDomain1 in organicDomainsDate1:
                        url1 = orgDomain1[5]
                        position1 = orgDomain1[4]
                        domain1 = orgDomain1[3]
                        if domain1 not in organicResult: ### if new results appeared
                            organicResult[domain1] = {'url': url1, 'change': position1, 'change_type': 'appear'}
                    result={}
                    result['organic'] = organicResult

                    os.chdir(bp.root_path+f"/SERP-database/")
                    if not os.path.isdir("changes"):
                        os.mkdir('changes')

                    with open(f'changes/{query}_changebetween_{date0}_and_{date1}.json', "w") as outfile:
                        json.dump(result, outfile)

                    if not os.path.isdir("changeswithVar"):
                        os.mkdir('changeswithVar')

                    s = 'var data = {}'.format(json.dumps(result))
                    with open(f'changeswithVar/{query}_changebetween_{date0}_and_{date1}_addVar.json', "w") as outfile:
                        outfile.write(s)
                    
                    logging.warning(os.getcwd())
            
            ranks = generateRankForQueryChangeBetweenTwoDates(date0, date1, category)
            
            
            return render_template('rankchanges/rankChanges.html', title='Home', category=category, currentdate=date1, previousdate=date0, ranks=ranks)   
                
            #logging.warning(categories)


    