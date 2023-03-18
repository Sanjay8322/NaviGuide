import random
import json
from urllib import response
import torch
from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words,tokenize
from chatbot.utils import process_activities
from PurposeRecommender.SparkALS import get_recommendations

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
                process_activities(tag, intent)
                recommendations = get_recommendations(1)
                response_message = random.choice(intent['responses'])
                return response_message
    
    return "I do not understand..."


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
