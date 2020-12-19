import torch
import models
import JCModel
import programs
import json

def get_gradients(model, x):
    x_tensor = torch.tensor(x, requires_grad=True)
    y = model(x_tensor)
    y.backward(torch.ones_like(y))
    return x_tensor.grad

def run_neutaint(inps, p):
    cname = p.__class__.__name__
    model = getattr(models, f"{cname}Model")(p.input_length).nn
    model.load_state_dict(torch.load(f"models/{p.name}.pl"))
    if p.typ == 'string':
        inps = convert_json_string_JC(inps)
    saliency_map = get_gradients(model, inps)
    return saliency_map

def convert_json_string_JC(json_strings):
    """
    Convert JSON string input to something that can be processed by Neutaint model
    """
    p = programs.JC()
    t = list()
    y = list()
    for json_string in json_strings:
        program_output = p(json_string)
        inpt_dict = json.loads(json_string)
        x1, x2 = list(inpt_dict.values())
        # x1 = json.loads(x1)
        # x2 = json.loads(x2)
        temp = list()
        for key in x1:
            temp.append(key.ljust(5))
            temp.append(x1[key].ljust(5))

        for key in x2:
            temp.append(key.ljust(5))
            temp.append(x2[key].ljust(5))

        t.append(words_to_ascii(temp))
        y.append(program_output)

    return torch.tensor(t, dtype=torch.float), \
            torch.tensor(y, dtype=torch.float).reshape(len(json_strings), 1)

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



