#!/usr/bin/python

import os
import pandas as pd
import webbrowser
from colour import Color

# TODO
'''
* dark line between entries
* shorten prdeictions
* color score based off val
* convert to pdf w compressed img and page breaks
* Narrow pic column
* Larger text?
* move correct label under image_path
* add prediction timestamp?
* insert col before img with green/yel/red icon for prediciton
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
    skeleton = {}
    skeleton['header'] = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Woof Report</title>
        <link rel="stylesheet" href="stylesheet.css" type="text/css">
    </head>
    <body>
        <div id="header">
            <h3>TITLE</h3>
            <p> Notes.......</p>
        </div>

        <table>
            <thead>
                <th>Labeled Image</th>
                <th>Prediction</th>
                <th>Score</th>
            </thead>

            '''
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
        <tbody>
            <tr>
                <td rowspan="4"><img src="{path}" /> <br><b>{filename}</b></td>
                <td>{breed1}</td>
                <td style="background-color:{color1}" >{score1}</td>
            </tr>
            <tr>
                <td>{breed2}</td>
                <td style="background-color:{color2}">{score2}</td>
            </tr>
            <tr>
                <td>{breed3}</td>
                <td style="background-color:{color3}">{score3}</td>
            </tr>
        </tbody>
        <thead class="splitter"><th colspan="3"></th></thead>

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
