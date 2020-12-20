import torch
import models
import JCModel
import programs
import json
import numpy as np

def get_gradients(model, x):
    x_tensor = torch.tensor(x, requires_grad=True)
    y = model(x_tensor)
    y.backward(torch.ones_like(y))
    return x_tensor.grad.unsqueeze(-1).numpy()

def run_neutaint(inps, p):
    cname = p.__class__.__name__
    model = getattr(models, f"{cname}Model")(p.input_length).nn
    model.load_state_dict(torch.load(f"models/{p.name}.pl"))
    if p.typ == 'string':
        inps = convert_json_string_JC(inps)
        saliency_map = get_gradients(model, inps)
        temp = [sum(saliency_map[i:i+10])/len(saliency_map[i:i+10])
                for i in range(0,len(saliency_map),10)]
        saliency_map = temp
    else:
        saliency_map = get_gradients(model, inps)

    return saliency_map

def convert_json_string_JC(json_strings):
    """
    Convert JSON string input to something that can be processed by Neutaint model
    """
    def convert_one(json_string):
        inpt_dict = json.loads(json_string)
        x1, x2 = list(inpt_dict.values())
        temp = list()
        for key in x1:
            temp.append(key.ljust(5))
            temp.append(x1[key].ljust(5))

        for key in x2:
            temp.append(key.ljust(5))
            temp.append(x2[key].ljust(5))
        return temp

    # p = programs.JC()
    t = list()
    if isinstance(json_strings, list):
        for json_string in json_strings:
            temp = convert_one(json_string)
            t.append(words_to_ascii(temp))
    else:
        temp = convert_one(json_strings)
        return words_to_ascii(temp)
        # t.append(words_to_ascii(temp))

    # return torch.tensor(t, dtype=torch.float)
    return t

def words_to_ascii(words):
    t = list()
    for word in words:
        for c in word:
            if c == ' ':
                t.append(0.0)
            else:
                t.append(ord(c)/256)

    return t

if __name__ == "__main__":
    # Test
    import programs
    p = programs.FBD()
    inps = p.gen_inputs(5)
    m = run_neutaint(inps, p)
    print(inps)
    print(m)



