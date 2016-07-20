#!/usr/bin/python

import os
import pandas as pd
import webbrowser
from colour import Color

# TODO
'''
* shorten prdeictions
* convert to pdf w compressed img and page breaks
* Larger text?
* add prediction timestamp?
* table of contents
* insert col before img with green/yel/red icon for prediciton
'''


title = 'Test Results V1'
notes = '''
<h5>Version 1 benchmark 7/15/16</h5>
<p> This report has approx 5000 prelabeled dog pics, and the top 3 predictions.
The predictions include a confidence which is between 0 and 1, 1 being 100% confident.
To improve readability, I mapped the confidence to colors (0 = red, 1 = green).
Ideally, the top guess is green and other guesses are red, however, sometimes they
are all simlar shades indicating no obvious choice.</p>
<p>You may notice sometimes the prediction is not a dog breed (ex Burrito) The next
version will fix this</p>
<p>The classifier seems to struggle with a few breed (American Bulldog, Shiba Inu and more).
In the next version, I will automate a method that determines the overall error
in the predictions by seeing if the top choices match the label (higher score
will be given when the top score matches the label, partial credit if the second
or third is correct) This way each version will have an overall accuracy for this dataset</p>
'''


def loadLog(f):
    ext = os.path.splitext(f)[1]
    if ext in '.tsv':
        return pd.read_csv(f, delimiter='\t')
    else:
        return pd.read_csv(f)


def getBody(log):
    body = ''
    for row in log.itertuples():
        body += addEntry(row)
    return body


def dict2html(s, filename):
    with open(filename, 'w+') as html:
        html.write(s['header'] + s['body'] + s['footer'])


def score2color(score):
    # hue map: 0 = red = lowscore, 0.35 = green = highscore
    c = Color(hsl=(score*0.35, 1, 0.7))
    return str(c.hex)


def getArgs(r):
    args = {}
    args['breed1'] = r.breed1.title()
    args['breed2'] = r.breed2.title()
    args['breed3'] = r.breed3.title()
    args['score1'] = r.score1
    args['score2'] = r.score2
    args['score3'] = r.score3
    args['color1'] = score2color(r.score1)
    args['color2'] = score2color(r.score2)
    args['color3'] = score2color(r.score3)
    args['timestamp'] = r.timestamp
    # need to use thumb version (see `batch_resize.py`)
    args['path'] = r.path + '_thumb.jpg'
    # hacky way to convert filename to label
    filename = ' '.join(os.path.splitext(r.filename)[0].split('_')[0:-1]).title()
    args['filename'] = filename
    return args


def getSkeleton(log):
    report = {'title': title, 'notes': notes}
    skeleton = {}
    skeleton['header'] = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Woof Report</title>
        <link rel="stylesheet" href="stylesheet.css" type="text/css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="jquery.lazyload.js" type="text/javascript"></script>
        <script src="scroll.js"></script>
    </head>
    <body>
        <div id="header">
            <h3>{title}</h3>
            <p>{notes}</p>
        </div>
        <table>
            <thead>
                <th>Labeled Image</th>
                <th>Prediction</th>
                <th>Score</th>
            </thead>

            '''.format(**report)
    skeleton['body'] = getBody(log)
    skeleton['footer'] = '''
        </table>
    </body>
    </html>
    '''
    return skeleton


def addEntry(row):
    args = getArgs(row)
    entry = '''
        <div class="scrollable-data">
            <tbody>
                <tr>
                    <td rowspan="4">
                        <img class="lazy" data-original="{path}">
                        <br><b>{filename}</b>
                    </td>
                    <td>{breed1}</td>
                    <td style="background-color:{color1}" ><b>{score1}</b></td>
                </tr>
                <tr>
                    <td>{breed2}</td>
                    <td style="background-color:{color2}"><b>{score2}</b></td>
                </tr>
                <tr>
                    <td>{breed3}</td>
                    <td style="background-color:{color3}"><b>{score3}</b></td>
                </tr>
            </tbody>
            <thead class="splitter"><th colspan="3"></th></thead>
        </div>

        '''.format(**args)
    return entry


def main():
    log_file = "results.tsv"
    report_file = "index.html"
    log = loadLog(log_file)
    s = getSkeleton(log)
    dict2html(s, report_file)
    webbrowser.open("file:///" + os.path.abspath(report_file))

if __name__ == '__main__':
    main()
