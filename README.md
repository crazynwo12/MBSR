We plan to upload 'learned network for NTIRE competition (CVPRW 2018)' to other places due to capacity.
# Title : Efficient Module Based SR for multiple problems 
# EMBSR
# Dependencies
Python (Tested with 3.6)
PyTorch >= 0.3.1

#Test
If you want to run the code, follow the steps below.

#0.
track1. bicubic x8.
The order of the test code files is.
a). code_8_4.
b). code 4_2_Final.
c). code 2_1_Final.

track2. mild x4
The order of the test code files is
a). code_4_4_DnCNN_tack2_BN_Resnet.
b). code 4_2_Final_2.
c). code 2_1_Fianl_2.

track3. difficult x4
The order of the test code files is
a). code_4_4_DnCNN_track3_BN_Resnet_2.
b). code 4_2_Final_3.
c). code 2_1_Final_3.

#1. Please (appath)set the data location in codex_x/data/MyImage.py.
#2. Modify dir in save_results function in codex_x/utils.py.



# License
You may freely use and distribute this software as long as you retain the author's name (myself and/or my students) with the software.
It would also be courteous for you to cite the toolbox and any related publications in any papers that present results based on this software. A typical citation is like: Dongwon park, "MBSR," available at [url], downloaded [date].
UM and the authors make all the usual disclaimers about liability etc.
If you make changes to any files, then please change the file name before redistributing to avoid confusion (like the GNU software license). Better yet, email me the changes and I'll consider incorporating them into the toolbox.


We get a lot of help from the site below.

https://github.com/thstkdgus35/EDSR-PyTorch
# Reference
[1] Bee Lim, Sanghyun Son, Heewon Kim, Seungjun Nah, and Kyoung Mu Lee, **"Enhanced Deep Residual Networks for Single Image Super-Resolution,"** <i>2nd NTIRE: New Trends in Image Restoration and Enhancement workshop and challenge on image super-resolution in conjunction with **CVPR 2017**. </i> [[PDF](http://openaccess.thecvf.com/content_cvpr_2017_workshops/w12/papers/Lim_Enhanced_Deep_Residual_CVPR_2017_paper.pdf)] [[arXiv](https://arxiv.org/abs/1707.02921)] [[Slide](https://cv.snu.ac.kr/research/EDSR/Presentation_v3(release).pptx)]
```
@InProceedings{Lim_2017_CVPR_Workshops,
  author = {Lim, Bee and Son, Sanghyun and Kim, Heewon and Nah, Seungjun and Lee, Kyoung Mu},
  title = {Enhanced Deep Residual Networks for Single Image Super-Resolution},
  booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR) Workshops},
  month = {July},
  year = {2017}
}