# intweenexport.py

import time
import math

def genSVG(strName, datapts):
	strSVG = ""

	numPts = len(datapts)

	nWidth = 1024
	nHeight = 640

	strGridX = ""
	strGridX = strGridX + '''<g class="grid x-grid" id="xGrid">'''
	for i in range(0, numPts):
		strGridX = strGridX + '''<line x1="''' + str(100 + 25*i) + '''" x2="''' + str(100 + 25*i) + '''" y1="140" y2="380"></line>'''
	strGridX = strGridX + "</g>"

	strGridY = ""
	strGridY = strGridY + '''<g class="grid y-grid" id="yGrid">'''
	for i in range(0, 10 + 1):
		strGridY = strGridY + '''<line x1="80" x2="600" y1="''' + str(360 - 20*i) + '''" y2="''' + str(360 - 20*i) + '''"></line>'''
	strGridY = strGridY + "</g>"

	strCirclePts = ""
	for i in range(0, numPts):
		strCirclePts = strCirclePts + '''<circle cx="'''
		strCirclePts = strCirclePts + str(100 + 25*i)
		strCirclePts = strCirclePts + '''" cy="'''
		strCirclePts = strCirclePts + str(360 - 20*datapts[i])
		strCirclePts = strCirclePts + '''" data-value="'''
		strCirclePts = strCirclePts + str(datapts[i])
		strCirclePts = strCirclePts + '''" r="5"></circle>'''

	strGraph = '''
		<g class="''' + strName + ''' points" data-setname="''' + strName + ''' data">
			''' + strCirclePts + '''
		</g>
	'''

	strSurface = ""
	strSurface = strSurface  + '''<g class="surfaces">'''
	strSurface = strSurface  + '''<path class="surfaces" d="M100,360 '''

	for i in range(0, numPts):
		strSurface = strSurface  + '''L''' + str(100 + 25*i) + ''',''' + str(360 - 20*datapts[i]) + ''' '''

	strSurface = strSurface  + '''L''' + str(100 + 25*(numPts-1)) + ''',''' + str(360) + ''' '''
	strSurface = strSurface  + ''' Z"></path>'''
	strSurface = strSurface  + '''</g>'''

	strLabels = '''
	<g class="labels title">
		<text x="250" y="430">''' + strName + '''</text>
	</g>
	<g class="labels x-labels">
		<text x="113" y="400">2008</text>
		<text x="259" y="400">2009</text>
		<text x="405" y="400">2010</text>
		<text x="551" y="400">2011</text>
	</g>
	<g class="labels y-labels">
		<text x="80" y="131">10</text>
		<text x="80" y="248">5</text>
		<text x="80" y="365">0</text>
	</g>
	'''

	strSVG = '''<svg width="''' + str(nWidth) + '''px" height="''' + str(nHeight) + '''px" class="graph" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg">'''
	strSVG = strSVG + strGridX
	strSVG = strSVG + strGridY
	strSVG = strSVG + strSurface
	strSVG = strSVG + strGraph
	strSVG = strSVG + strLabels
	strSVG = strSVG + '''</svg>'''

	return strSVG

def genHTML(strName, datapts):
	strHTML = ""

	strHTML_top = '''
	<!DOCTYPE html>
	<html>
		<head>
			<title>''' + strName + '''</title>
			<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
			<meta charset="utf-8"/>
			<style>
				body {
					background-color: #353432;
				}

				svg.graph {
					height: 500px;
					width: 800px;
				}

				svg.graph .grid {
					stroke: #4E4D4A;
					stroke-width: 1;
				}

				svg.graph .points {
					fill: #94BA65;
					fill-opacity: 0.4;

					stroke: white;
					stroke-opacity: 0.4;
					stroke-width: 2;
				}

				svg.graph .surfaces {
					fill: #94BA65;
				}

				svg.graph .grid.double {
					stroke-opacity: 0.4;
				}

				svg.graph .labels {
					fill: #94BA65;
					font-family: Sans;
					font-size: 12px;
					kerning: 1;
				}

				svg.graph .labels.title {
					fill: white;
				}

				svg.graph .labels.x-labels {
					text-anchor: middle;
				}

				svg.graph .labels.y-labels {
					text-anchor: end;
				}

			</style>
		</head>
		<body>
			<div>
				'''

	strHTML_bottom = '''
			</div>
		</body>
	</html>
	'''

	strHTML = strHTML + strHTML_top
	strHTML = strHTML + genSVG(strName, datapts)
	strHTML = strHTML + strHTML_bottom

	return strHTML
