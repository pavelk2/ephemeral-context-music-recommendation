import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

from hybrid.hybrid import calcRecommendations, getNotes
from soundcloud.soundcloud import getSongs

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    weights = getHTTPParamArray("weights")
    context = getHTTPParamArray("context")

    if (len(context) != 8 or len(weights) != 3):
        response = {"error":"context should consist exactly out of 8 features, weights should be exactly 3"}
    else:
        recommendations = calcRecommendations(weights, context)
    response = formResponse(recommendations)
    return jsonify(response)

# ==================
def getHTTPParamArray(param):
  return list(map(float, request.args.get(param).split(',')))


def formResponse(recommendations):
  (rm_1,rm_2,rm_3,hybrid) = recommendations
  print(rm_1)
  print(hybrid)
  
  return {
      "individual":[
        {
          "name":"recommender_1",
          "recommendation" : getNotes(rm_1.tolist())
        },{
          "name":"recommender_2",
          "recommendation" : getNotes(rm_2.tolist())
        },{
          "name":"recommender_3",
          "recommendation" : getNotes(rm_3.tolist())
        }
      ],
      "hybrid":getNotes(hybrid.tolist()),
      "songs" : getSongs(hybrid.tolist())
    }


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
