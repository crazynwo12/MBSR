from model import common

import torch.nn as nn
from torch.autograd import Variable

def make_model(args, parent=False):
    return EDSR(args)

class EDSR(nn.Module):
    def __init__(self, args, conv=common.default_conv):
        super(EDSR, self).__init__()
        self.fullTrain = args.fullTrain
        self.fullInputScale = args.fullInputScale
        self.fullTargetScale = args.fullTargetScale
        n_resblock = args.n_resblocks
        batch_norm = args.BN
        n_feats = args.n_feats
        kernel_size = 3 
        scale = args.scale[0]
        act = nn.ReLU(True)

        rgb_mean = (0.4488, 0.4371, 0.4040)
        self.sub_mean = common.MeanShift(args.rgb_range, rgb_mean, -1)
        
        # define head module
        
        modules_head = [conv(args.n_colors, n_feats, kernel_size)]
        modules_head_DNN = [conv(args.n_colors, n_feats, 7)]
        modules_head_DNN.append(act)

        # define body module
        modules_body = [
            common.ResBlock(
                conv, n_feats, kernel_size, act=act, res_scale=args.res_scale) \
            for _ in range(n_resblock)]
        modules_body.append(conv(n_feats, n_feats, kernel_size))

        modules_body_DNN = [
            common.ResBlock(
                conv, n_feats, kernel_size, act=act,bias = True,bn=batch_norm, res_scale=args.res_scale) \
            for _ in range(n_resblock)]
        modules_body.append(conv(n_feats, n_feats, kernel_size))



        # define tail module
        modules_tail = [
            common.Upsampler(conv, 2, n_feats, act=False),
            conv(n_feats, args.n_colors, kernel_size)]
        

        modules_tail_DNN = [
            conv(n_feats, args.n_colors, kernel_size)]

        self.add_mean = common.MeanShift(args.rgb_range, rgb_mean, 1)

        self.head_DNN = nn.Sequential(*modules_head_DNN)
        self.body_DNN = nn.Sequential(*modules_body_DNN)
        #self.tail_4 = nn.Sequential(*modules_tail)
        self.tail_DNN = nn.Sequential(*modules_tail_DNN)
        

        self.head_2 = nn.Sequential(*modules_head)
        self.body_2 = nn.Sequential(*modules_body)
        self.tail_2 = nn.Sequential(*modules_tail)

        self.head = nn.Sequential(*modules_head)
        self.body = nn.Sequential(*modules_body)
        self.tail = nn.Sequential(*modules_tail)
    def forward(self, x):
        if self.fullTrain:
            x = self.sub_mean(x)
            x = self.head_4(x)
            res = self.body_4(x)
            res += x
            x = self.tail_4(res)
            x4_1 = self.add_mean(x)

            x4 = self.sub_mean(x4_1)
            x4 = self.head_2(x4)
            res4 = self.body_2(x4)
            res4 += x4
            x4 = self.tail_2(res4)
            x2_1 = self.add_mean(x4)

            x2 = self.sub_mean(x2_1)
            x2 = self.head(x2)
            res2 = self.body(x2)
            res2 += x2
            x2 = self.tail(res2)
            x_output = self.add_mean(x2)
            return x_output,x2_1,x4_1
        else:
            if self.fullInputScale == '2':
                x2_1 = x
                x2 = self.sub_mean(x2_1)
                x2 = self.head(x2)
                res2 = self.body(x2)
                res2 += x2
                x2 = self.tail(res2)
                x_output = self.add_mean(x2)
                return x_output
            
            elif self.fullInputScale == '4':
                x4_1 = x
                x4 = self.sub_mean(x4_1)
                x4 = self.head_2(x4)
                res4 = self.body_2(x4)
                res4 += x4
                x4 = self.tail_2(res4)
                x2_1 = self.add_mean(x4)                
                if self.fullTargetScale == '2':
                    return x2_1
                else:
                    x2 = self.sub_mean(x2_1)
                    x2 = self.head(x2)
                    res2 = self.body(x2)
                    res2 += x2
                    x2 = self.tail(res2)
                    x_output = self.add_mean(x2)
                    return x_output
############################################################3                
            elif self.fullInputScale == '8':
                x = self.sub_mean(x)
                res_ = self.head_DNN(x)
                res = self.body_DNN(res_)
                #res += res_
                #x = self.tail_4(res)
                res = self.tail_DNN(res)
                res = res + x
                x4_1 = self.add_mean(res)
                if self.fullTargetScale == '4':
                    return x4_1
                else:
##############################################
                  # x4_1 = Variable(x4_1.data)
                   # x4_1 = x4_1.detach()
                    x4 = self.sub_mean(x4_1)
                    x4 = self.head_2(x4)
                    res4 = self.body_2(x4)
                    res4 += x4
                    x4 = self.tail_2(res4)
                    x2_1 = self.add_mean(x4)
##############################################
                if self.fullTargetScale == '2':
                    return x2_1
                else:
                    x2 = self.sub_mean(x2_1)
                    x2 = self.head(x2)
                    res2 = self.body(x2)
                    res2 += x2
                    x2 = self.tail(res2)
                    x_output = self.add_mean(x2)
            
            
                    return x_output            
            
            
            
            
    def load_state_dict_8_4(self, state_dict, strict=True):
        own_state = self.state_dict()
        for name, param in state_dict.items():
            #name_check = name
            #print(name_check[:6])
            #print(name_check)
            if name[:6] != 'body_D' and name[:6] != 'tail_D'and name[:6] != 'head_D' :
               continue
            #if name_check[:6] != 'tail_4':
            #   continue
            print(name)
            print(33)
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') >= 0:
                        print('Replace pre-trained upsampler to new one...')
                    else:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))

        if strict:
            missing = set(own_state.keys()) - set(state_dict.keys())
#            if len(missing) > 0:
#                raise KeyError('missing keys in state_dict: "{}"'.format(missing))

    def load_state_dict_4_2(self, state_dict, strict=True):
        own_state = self.state_dict()
        for name, param in state_dict.items():
            
            if name[:6] != 'body_2' and name[:6] != 'tail_2'and name[:6] != 'head_2' :
               continue
#            print(name)
#            print(22)
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') >= 0:
                        print('Replace pre-trained upsampler to new one...')
                    else:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))

        if strict:
            missing = set(own_state.keys()) - set(state_dict.keys())
#            if len(missing) > 0:
#                raise KeyError('missing keys in state_dict: "{}"'.format(missing))

    def load_state_dict(self, state_dict, strict=True):
        own_state = self.state_dict()
        for name, param in state_dict.items():
            
#            if name[:6] == 'body_2' or name[:6] == 'tail_2'or name[:6] == 'head_2'or name[:6] == 'body_4' or name[:6] == 'tail_4'or name[:6] == 'head':
#               continue
#            print(name)
#            print(11)
            if name in own_state:
                if isinstance(param, nn.Parameter):
                    param = param.data
                try:
                    own_state[name].copy_(param)
                except Exception:
                    if name.find('tail') >= 0:
                        print('Replace pre-trained upsampler to new one...')
                    else:
                        raise RuntimeError('While copying the parameter named {}, '
                                           'whose dimensions in the model are {} and '
                                           'whose dimensions in the checkpoint are {}.'
                                           .format(name, own_state[name].size(), param.size()))
            elif strict:
                if name.find('tail') == -1:
                    raise KeyError('unexpected key "{}" in state_dict'
                                   .format(name))

        if strict:
            missing = set(own_state.keys()) - set(state_dict.keys())
            if len(missing) > 0:
                raise KeyError('missing keys in state_dict: "{}"'.format(missing))

