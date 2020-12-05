import torch
import models

def get_gradients(model, x):
    x_tensor = torch.tensor(x, requires_grad=True)
    y = model(x_tensor)
    y.backward(torch.ones_like(y))
    return x_tensor.grad


def run_neutaint(inps, p):
    cname = p.__class__.__name__
    model = getattr(models, f"{cname}Model")(p.input_length).nn
    model.load_state_dict(torch.load(f"models/{p.name}.pl"))
    saliency_map = get_gradients(model, inps)
    return saliency_map

if __name__ == "__main__":
    # Test
    import programs
    p = programs.FBD()
    inps = p.gen_inputs(5)
    m = run_neutaint(inps, p)
    print(inps)
    print(m)



