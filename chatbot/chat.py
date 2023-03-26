import random
import json
from urllib import response
import torch
from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words,tokenize
from chatbot.utils import log_activities
from core.exceptions.app_exceptions import LogActivitiesException
from text_to_speech.text_to_speech import get_audio_feedback

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('chatbot/intents.json','r') as f:
    intents=json.load(f)


#We saved in train.py and here we load

FILE="chatbot/data.pth"
data=torch.load(FILE)

input_size=data["input_size"]
hidden_size=data["hidden_size"]
output_size=data["output_size"]
all_words=data["all_words"]
tags=data["tags"]
model_state=data["model_state"]
model=NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state) #Data loading from data.pth
model.eval()


#Creating bot

bot_name="KCT bot"
def get_response(msg):
    try:
        sentence = tokenize(msg)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    response_message = random.choice(intent['responses'])
                    response_audio_url = get_audio_feedback(response_message)
                    log_activities(tag, intent)
                    return response_message, response_audio_url
        
        response_message = "I do not understand..."
        response_audio_url = get_audio_feedback(response_message)
        return response_message, response_audio_url

    except LogActivitiesException as e:
        return response_message
    except Exception as e:
        return "Error"


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
        
        
        
        
        
        
        
        



# print("Let's chat! type 'quit' to exit")
# while True:
#     sentence=input("you: ")
#     if(sentence=="quit"):
#         break 
    
#     sentence=tokenize(sentence)
#     X=bag_of_words(sentence,all_words)
#     X=X.reshape(1,X.shape[0])
#     X=torch.from_numpy()
    
#     output=model(X)
#     _, predicted=torch.max(output,dim=1)
#     tag=tags[predicted.item()]
    
#     #softmax layer for probability
#     probs=torch.softmax(output,dim=1)
#     prob=probs[0][predicted.item()]
    
#     #only if probability >0.75 means there is a chance
#     if prob.item()>0.75:
#         for intent in intents["intents"]:
#             if tag==intent["tag"]:
#                 print(f'{bot_name} : {random.choice(intent["responses"])}')
#     else:
#         print(f'{bot_name} : I do not understand :(')
