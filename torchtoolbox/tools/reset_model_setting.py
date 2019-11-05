# -*- coding: utf-8 -*-
__all__ = ['no_decay_bias', 'reset_model_setting']
from torch import nn


def no_decay_bias(net):
    """split network weights into to categlories,
    one are weights in conv layer and linear layer,
    others are other learnable paramters(conv bias,
    bn weights, bn bias, linear bias)
    Args:
        net: network architecture
    Returns:
        a dictionary of params splite into to categlories
    """

    decay = []
    no_decay = []

    for m in net.modules():
        if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
            decay.append(m.weight)

            if m.bias is not None:
                no_decay.append(m.bias)

        else:
            if hasattr(m, 'weight'):
                no_decay.append(m.weight)
            if hasattr(m, 'bias'):
                no_decay.append(m.bias)

    assert len(list(net.parameters())) == len(decay) + len(no_decay)

    return [dict(params=decay), dict(params=no_decay, weight_decay=0)]


def reset_model_setting(model, layer_names, setting_name, base_value, rate):
    if not isinstance(layer_names, (list, tuple)):
        layer_names = [layer_names]
    ignore_params = []
    for name in layer_names:
        ignore_params.extend(list(map(id, getattr(model, name).parameters())))

    base_param = filter(lambda p: id(p) not in ignore_params, model.parameters())
    reset_param = filter(lambda p: id(p) in ignore_params, model.parameters())

    parameters = [{'params': base_param},
                  {'params': reset_param, setting_name: base_value * rate}]
    return parameters
