import random

import numpy as np
import skimage.io as sio
import skimage.color as sc
import skimage.transform as st

import torch
from torchvision import transforms

def get_patch(img_in, img_tar,img_in4,img_in2, args, scale, ix=-1, iy=-1):
    (ih, iw, c) = img_in.shape
    (th, tw) = (scale * ih, scale * iw)
    (th_4, tw_4) = (2 * ih, 2 * iw)
    (th_2, tw_2) = (4 * ih,4 * iw)



    #patch_mult = scale if len(args.scale) > 1 else 1
    #patch_mult = 0.5
    tp = args.patch_mult * args.patch_size
    ip = tp // scale
    tp_4 = tp //4
    tp_2 = tp //2
    
    if ix == -1:
       ix = random.randrange(30, iw - (ip+30) + 1)
	#ix = random.randint(0,iw - ip + 1)
    if iy == -1:
       iy = random.randrange(30, ih - (ip+30) + 1)
	#iy =random.randint(0,ih - ip + 1)
    (tx, ty) = (scale * ix, scale * iy)
    (tx_4, ty_4) = (2 * ix, 2 * iy)
    (tx_2, ty_2) = (4 * ix, 4 * iy)

    
    img_in = img_in[iy:iy + ip, ix:ix + ip, :]
    img_tar = img_tar[ty:ty + tp, tx:tx + tp, :]
    img_in4 = img_in4[ty_4:ty_4 + tp_4, tx_4:tx_4 + tp_4, :]
    img_in2 = img_in2[ty_2:ty_2 + tp_2, tx_2:tx_2 + tp_2, :]    
    info_patch = {
        'ix': ix, 'iy': iy, 'ip': ip, 'tx': tx, 'ty': ty, 'tp': tp}

    return img_in, img_tar,img_in4, img_in2,info_patch

def get_patch_DW(img_in, img_tar, args, scale, ix=-1, iy=-1):
    (ih, iw, c) = img_in.shape
    (th, tw) = (scale * ih, scale * iw)
    #patch_mult = scale if len(args.scale) > 1 else 1
    patch_mult = args.patch_mult
    tp = int(patch_mult * args.patch_size)
    ip = int(tp // scale)
    #print(iw-ip+1)
    if ix == -1:
       ix = random.randrange(30, iw - (ip+30) + 1)
	#ix = random.randint(0,iw-ip+1)
    if iy == -1:
	#iy = random.randint(0,ih-ip+1)
       iy = random.randrange(30, ih - (ip+30) + 1)

    (tx, ty) = (scale * ix, scale * iy)


    
    img_in = img_in[iy:iy + ip, ix:ix + ip, :]
    img_tar = img_tar[ty:ty + tp, tx:tx + tp, :]

    info_patch = {
        'ix': ix, 'iy': iy, 'ip': ip, 'tx': tx, 'ty': ty, 'tp': tp}

    return img_in, img_tar,None, None,info_patch


def get_patch_DW_test(img_in, img_tar, args, scale, ix=-1, iy=-1):
    (ih, iw, c) = img_in.shape
    (th, tw) = (scale * ih, scale * iw)
    #patch_mult = scale if len(args.scale) > 1 else 1
#    patch_mult = args.patch_mult
    tp = int(args.patch_size)
    ip = int(tp // scale)
#  
    iw_h = iw//2
    ih_h = ih//2
    ix = iw_h - (ip//2)
    iy = ih_h - (ip//2)

    (tx, ty) = (scale * ix, scale * iy)



    img_in = img_in[iy:iy + ip, ix:ix + ip, :]
    img_tar = img_tar[ty:ty + tp, tx:tx + tp, :]

    info_patch = {
        'ix': ix, 'iy': iy, 'ip': ip, 'tx': tx, 'ty': ty, 'tp': tp}

    return img_in, img_tar,None, None,info_patch







def set_channel(img_in, img_tar, n_channel):
    (h, w, c) = img_tar.shape
    if n_channel == 1 and c == 3:
        img_in = np.expand_dims(sc.rgb2ycbcr(img_in)[:, :, 0], 2)
        img_tar = np.expand_dims(sc.rgb2ycbcr(img_tar)[:, :, 0], 2)
    elif n_channel == 3 and c == 1:
        img_in = np.concatenate([img_in] * n_channel, 2)
        img_tar = np.concatenate([img_tar] * n_channel, 2)

    return img_in, img_tar
def set_channel_Three(img_in, img_tar,img_in_4, img_in_2, n_channel):
    (h, w, c) = img_tar.shape
    if n_channel == 1 and c == 3:
        img_in = np.expand_dims(sc.rgb2ycbcr(img_in)[:, :, 0], 2)
        img_tar = np.expand_dims(sc.rgb2ycbcr(img_tar)[:, :, 0], 2)
        img_in_4 = np.expand_dims(sc.rgb2ycbcr(img_in_4)[:, :, 0], 2)
        img_in_2 = np.expand_dims(sc.rgb2ycbcr(img_in_2)[:, :, 0], 2)
    elif n_channel == 3 and c == 1:
        img_in = np.concatenate([img_in] * n_channel, 2)
        img_tar = np.concatenate([img_tar] * n_channel, 2)
        img_in_4 = np.concatenate([img_in_4] * n_channel, 2)
        img_in_2 = np.concatenate([img_in_2] * n_channel, 2)
        
    return img_in, img_tar,img_in_4,img_in_2


def np2Tensor_DW(img_in, img_tar,img_in_4,img_in_2, rgb_range):
    ts = (2, 0, 1)
    img_mul = rgb_range / 255
    img_in = torch.Tensor(img_in.transpose(ts).astype(float)).mul_(img_mul)
    img_tar = torch.Tensor(img_tar.transpose(ts).astype(float)).mul_(img_mul)
    img_in_4 = torch.Tensor(img_in_4.transpose(ts).astype(float)).mul_(img_mul)
    img_in_2 = torch.Tensor(img_in_2.transpose(ts).astype(float)).mul_(img_mul)
    #print(img_in_4.shape)
    return img_in, img_tar,img_in_4,img_in_2



def np2Tensor(img_in, img_tar, rgb_range):
    ts = (2, 0, 1)
    img_mul = rgb_range / 255
    a = img_in.transpose(ts).astype(float)
    #print(a.shape)
    img_in = torch.Tensor(img_in.transpose(ts).astype(float)).mul_(img_mul)
    img_tar = torch.Tensor(img_tar.transpose(ts).astype(float)).mul_(img_mul)

    #img_in = torch.Tensor(np.transpose(img_in,ts)).mul_(img_mul)
    #img_tar = torch.Tensor(np.transpose(img_tar,ts)).mul_(img_mul)
    #print(img_in.shape)
    #print(img_tar.shape)
    return img_in, img_tar

def augment(img_in, img_tar,img_in4,img_in2,flip_h=True, rot=True):
    info_aug = {'flip_h': False, 'flip_v': False, 'trans': False}

    if random.random() < 0.5 and flip_h:
        img_in = img_in[:, ::-1, :]
        img_tar = img_tar[:, ::-1, :]
        img_in4 = img_in4[:,::-1,:]
        img_in2 = img_in2[:,::-1,:]
        info_aug['flip_h'] = True

    if rot:
        if random.random() < 0.5:
            img_in = img_in[::-1, :, :]
            img_tar = img_tar[::-1, :, :]
            img_in4 = img_in4[::-1, :, :]
            img_in2 = img_in2[::-1, :, :]

            info_aug['flip_v'] = True
        if random.random() < 0.5:
            img_in = img_in.transpose(1, 0, 2)
            img_tar = img_tar.transpose(1, 0, 2)
            img_in4 = img_in4.transpose(1, 0, 2)
            img_in2 = img_in2.transpose(1, 0, 2)            
            info_aug['trans'] = True

    return img_in, img_tar,img_in4,img_in2, info_aug
def augment_DW(img_in, img_tar,flip_h=True, rot=True):
    info_aug = {'flip_h': False, 'flip_v': False, 'trans': False}

    if random.random() < 0.5 and flip_h:
        img_in = img_in[:, ::-1, :]
        img_tar = img_tar[:, ::-1, :]
        info_aug['flip_h'] = True

    if rot:
        if random.random() < 0.5:
            img_in = img_in[::-1, :, :]
            img_tar = img_tar[::-1, :, :]


            info_aug['flip_v'] = True
        if random.random() < 0.5:
            img_in = img_in.transpose(1, 0, 2)
            img_tar = img_tar.transpose(1, 0, 2)
         
            info_aug['trans'] = True

    return img_in, img_tar,None,None, info_aug
