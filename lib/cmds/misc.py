import functools
import operator

def help(bot, prefix, cmds):
    bot.send_message("Registered commands: " + ", ".join([f'{prefix}{cmd}' for cmd in sorted(cmds.keys())]))
    
def hello(bot, user, *args):
    bot.send_message(f' Hey {user["name"]}!')

def test(bot, user, *args):
    print(args)    

def bot(bot, user, *args):
    import random
    import json
    import torch
    from chatbot.model import NeuralNet
    from chatbot.nltk_utils import bag_of_words, tokenize

    
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    with open(r"C:\Users\trevo\OneDrive\Desktop\intents.json", 'r') as f:
        intents = json.load(f)
        
    FILE = r'C:\Users\trevo\eclipse-workspace\neuralnet\lib\cmds\data.pth'
    data = torch.load(FILE)
    
    input_size = data['input_size']
    hidden_size = data['hidden_size']
    output_size = data['output_size']
    all_words = data['all_words']
    tags = data['tags']
    model_state = data['model_state']
    
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    

    sentence = convertTuple(args)
    if sentence == 0:
        print()
    else:
        sentence = tokenize(sentence)
        x = bag_of_words(sentence, all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x)
        
        output = model(x)
        _, predicted = torch.max(output, dim=1)
        
        tag = tags[predicted.item()]
        
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        
        if prob.item() > 0.7:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    bot.send_message(f'{user["name"]} {random.choice(intent["responses"])}')
                    
        else:
            bot.send_message('I do not understand...') 
            
def convertTuple(tup):
    try:
        stri = functools.reduce(operator.add, (tup))
        return stri
    except TypeError:
        stri = 0
        return stri  