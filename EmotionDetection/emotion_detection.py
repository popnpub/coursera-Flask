import requests
import json
from pprint import pprint

def emotion_detector(text_to_analyse):
    # Define the URL for the sentiment analysis API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Create the payload with the text to be analyzed
    myobj = { "raw_document": { "text": text_to_analyse } }

    # Set the headers with the required model ID for the API
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Make a POST request to the API with the payload and headers
    response = requests.post(url, json=myobj, headers=header)

    if response.status_code == 400:
        res = {'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None,
            }
    else:
        # Parse the response from the API
        formatted_response = json.loads(response.text)

        # Return the label and score in a dictionary
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        res = {'anger': float(emotions['anger']),
                'disgust': float(emotions['disgust']),
                'fear': float(emotions['fear']),
                'joy': float(emotions['joy']),
                'sadness': float(emotions['sadness']),
                }

        dominant = sorted([(v,k) for k,v in res.items()])[-1][1]
        res['dominant_emotion'] = dominant

    return res