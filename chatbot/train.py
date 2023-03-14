import json
from chatbot.nltk_utils import tokenize,stem,bag_of_words
import numpy as np

#To read about this
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader

from chatbot.model import NeuralNet

with open('intents.json','r') as f:   # r is read 
    intents=json.load(f) 

all_words=[]  #for bag of words
tags=[]  #for the tags
xy=[] #hold patterns and tags

#TOKENIZATION

for intent in intents['intents']:   #object.notation similar 
    tag=intent['tag'] #in intents json file we take tag
    tags.append(tag)
    for pattern in intent['patterns']:
        w=tokenize(pattern)
        all_words.extend(w) # this is also array we wnt put array of array in all_words so we extend method
        xy.append((w,tag)) # (w,tag) -> pattern and its tag (Tuple)
        
        
#STEMMING

ignore_words=['?','!','.',',']
all_words=[stem(w) for w in all_words if w not in ignore_words]
all_words=sorted(set(all_words)) #sorted and unique words
tags=sorted(set(tags))


#Bag_of_words

X_train=[] #for bag of words
y_train=[] #for the tags

for (pattern_sentence,tag) in xy:
    bag=bag_of_words(pattern_sentence,all_words) # we defined this function in nltk_utils.py
    X_train.append(bag)
    
    label=tags.index(tag)  # takes the index of tags list
    y_train.append(label) #CrossEntropyLoss
    
#TRAINING DATA  
X_train=np.array(X_train)
y_train=np.array(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples=len(X_train)
        self.x_data=X_train
        self.y_data=y_train
        
    #dataset[idx]
    def __getitem__(self,index):
        return self.x_data[index],self.y_data[index]
     
                               
        
    def __len__(self):
        return self.n_samples
           


#Hyperparamter

batch_size=8  
hidden_size=8
output_size=len(tags) #no of differnet tags we have
input_size=len(X_train[0]) #lenght of all words
learning_rate=0.001
num_epochs=1000
# print(input_size,len(all_words))
# print(output_size,tags)


dataset=ChatDataset()
train_loader=DataLoader(dataset=dataset, 
                        batch_size=batch_size,
                        shuffle=True,
                        num_workers=0
                        ) #,shuffle=True,num_workers=2 
        
#Create Model

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model=NeuralNet(input_size,hidden_size,output_size).to(device)
 
#lose and optimizer
criterion=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.parameters(),lr=learning_rate)

for epoch in range(num_epochs):
    for (words,labels) in train_loader:
        words=words.to(device)
        labels=labels.to(dtype=torch.long).to(device)
    
        
        #forward
        
        outputs=model(words)
        loss=criterion(outputs,labels)
        
        #backward and optimizer
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1)%100 ==0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
print(f'final loss:{loss.item():.4f}')


#Saving Data
data={
    "model_state":model.state_dict(),
    "input_size":input_size,
    "output_size":output_size,
    "hidden_size":hidden_size,
    "all_words":all_words,
    "tags":tags
}

FILE="data.pth"
torch.save(data,FILE)
print(f'Training complete. file saved to {FILE} ' )
