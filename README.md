# PrecogSummer '17
## Task A - Twitter Analysis
<br>
#### Link to Webapp: http://precogsummer-arsh.herokuapp.com/
---------
## Details
### Step 1 : Scraping and parsing
For scraping I used selenium to scroll the twitter pages till 'n' actual tweets are loaded, then use lxml xpaths to extract the tweet objects. These raw tweet objects are then parsed and 
relevant information is saved in MongoDB. 
<br>Files - [scraper.py](https://gitlab.com/Arsh23/PS17_arsh/blob/master/code/scraper.py) and [parser.py](https://gitlab.com/Arsh23/PS17_arsh/blob/master/code/parser.py)

### Step 2 : Analysis
I took this part as a kind of challenge in writing the smallest code possible, so the result might not be the best in readability but it sure has some of the best generator comprehensions 
I have ever written (It was fun :P ) . For sentiment analysis I used [HPE Haven API](https://dev.havenondemand.com/apis/analyzesentiment#overview).
<br>
File for frequency analysis, top hashtags and user engagement is [analyzer.py](https://gitlab.com/Arsh23/PS17_arsh/blob/master/code/analyzer.py) and for sentiment analysis [sentiment.py](https://gitlab.com/Arsh23/PS17_arsh/blob/master/code/sentiment.py)


### Step 3 : Visualizations
For visualizations, I tried to go for graphs that would convey the most relevant information in a quick glance, So I deviated from the usual bar graphs and pie charts and made custom graphs.
All graphs are made with D3.js. The app is hosted on Heroku and runs on Flask.
<br>
Graph Files : [freqgraph.html](https://gitlab.com/Arsh23/PS17_arsh/blob/master/templates/freqgraph.html), 
[top10graph.html](https://gitlab.com/Arsh23/PS17_arsh/blob/master/templates/top10graph.html), 
[sentigraph.html](https://gitlab.com/Arsh23/PS17_arsh/blob/master/templates/sentigraph.html) and 
[engagement.html](https://gitlab.com/Arsh23/PS17_arsh/blob/master/templates/engagement.html)
<br>
Flask File: [app.py](https://gitlab.com/Arsh23/PS17_arsh/blob/master/app.py)

### Running any of the above files -
```sh
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
sudo service mongod start
python <filename>.py
```

### Data
* The scraped data was stored in a MongoDB database named `precog` with 5 collections for each of the accounts.
        <br>
        The JSON dump of all these collections is present in [/data](https://gitlab.com/Arsh23/PS17_arsh/tree/master/data)
* All the JSON Files used to draw the graphs are stored in [/static/data](https://gitlab.com/Arsh23/PS17_arsh/tree/master/static/data)

<br><br>
#### Made by: [Arsh](http://github.com/arsh23)