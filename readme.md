# 肺实质提取

【2022年7月更新】因为数据隐私的问题，在public版本的repo中去掉了所有CT扫描图片。


## 神经网络

使用 https://github.com/JoHof/lungmask 来提取肺部实质内容.


这是一个已经训练过的网络（不是在本数据集上训练的），训练的数据是HU文件，因此对于jpg文件有一定的误差（如42、43、44三幅CT图像中，左部肺部分成两段，网络直接舍弃了左肺的一部分）
（后续可以考虑用膨胀之后的图像再做处理）

脚本文件名为processCT.py


遇到的问题：https://github.com/JoHof/lungmask 只能正确处理一部分jpg文件:


['honeycombing_23.jpg_output.jpg', 'honeycombing_24.jpg_output.jpg', 'honeycombing_25.jpg_output.jpg', 'honeycombing_26.jpg_output.jpg', 'honeycombing_27.jpg_output.jpg', 'honeycombing_31.jpg_output.jpg', 'reticulation_42.jpg_output.jpg', 'reticulation_43.jpg_output.jpg', 'reticulation_44.jpg_output.jpg', 'reticulation_45.jpg_output.jpg', 'reticulation_46.jpg_output.jpg', 'reticulation_47.jpg_output.jpg', 'reticulation_48.jpg_output.jpg']


提取出mask后，对原图进行处理，得到一部分肺部实质图像，脚本文件名为processMask.py。

mask位于/non-smooth/mask/，
肺部实质图像位于/non-smooth/output/


观察到mask和实质图像的边缘锯齿现象比较严重，因此我对mask首先做了一次平滑，观察到了明显的改善。

于是，我尝试使用不同的平滑方法。
包括：
* 2D Convolution
* Image Blurring
* Gaussian Filtering
* Median Filtering
* Bilateral Filtering

经过实验对比发现， Median Filtering 不管是对mask还是最终提取的肺实质区域，效果都是最好的。

这部分的图片文件存在/parenchyma/network-lungmask/下：

* non-smooth: 没有经过平滑处理的mask和肺实质
    * mask: 直接通过lungmask获得的mask
    * output: 通过mask和原图获得的肺实质图像
* smooth：经过平滑处理的mask和肺实质
    * mask: 通过对../non-smooth/mask文件夹下mask做平滑处理得到的mask（使用Median Filtering）
    * output：通过平滑的mask和原图得到的肺实质图像（因为担心影响后续纹理分析的准确度，因此没有对output做平滑）
    * smooth-method：使用第23张CT图像来进行各种平滑方法对比的结果，脚本文件为smooth.py，文件名称对应平滑方法为：
        * filter: 2D Convolution
        * blur: Image Blurring
        * gblur: Gaussian Filtering
        * median: Median Filtering
        * bblur: Bilateral Filtering

## 传统方法

最终采用的算法如下图：
 ![](.\readme-img\pipeline.png)


### 尝试1

然后我尝试了使用传统方法来进行肺实质分割，这部分的图片存在/parenchyma/traditional/下
参考了CSDN的这篇文章：https://blog.csdn.net/tianjinyikedaxue/article/details/89951069

步骤：
1. 使用大津阈值算法将CT图片处理为前景和背景，存在/mask-OTSU/下。脚本文件为threshold.py
2. 对大津阈值算法得到的结果使用开操作，然后做一次Median Filtering平滑，存在/mask-open/下。脚本文件为openAndBlur.py
3. 对第2步得到的结果，找到图片中的所有轮廓，填充除了最大的轮廓外的其他轮廓（最大的轮廓是胸腔），以此摆脱床板。脚本文件为getMask.py

存在/mask/下。我在这一步注意到气管仍然存在，尤其是对第19幅图像。然而，在开操作时，如果使用更小的kernel，就会导致肺实质有很多孔洞无法被填充。因此，我决定到纹理分析时再处理这个问题。



### 尝试2

后续我经过思考，采用了新的办法（脚本文件：allInOne.py, close.py, getParenchyma.py)
1. 使用大津阈值算法将CT图片处理为前景和背景
2. 先对第一步结果取反，进行闭操作，再取反
3. 找到最大连通域，填充除去最大连通域外的连通域
4. 再次取反，做一次腐蚀操作，去除面积比较小的联通区域，然后以同样的kernel做一次膨胀操作（主要是为了去掉血管）  
    对于mask有缺陷的，迭代使用闭操作填充mask，对mask做一次Median Filtering
5. 根据mask和原图得到肺实质区域

最终使用的算法：
* allInOne.py
* close.py
* getParenchyma.py
<!-- 使用VGG标注 -->


# 纹理分析
1. 图片分类  
我发现consolidation类症状会有一整片灰度接近的区域，对标注好的真实数据求灰度直方图后发现，consolidation病灶区的灰度集中分布在[90, 110]范围内。  
然后，我对所有图片的病灶区域，求取[90,110]在整体病灶区域内灰度的占比，得到数据：

![](.\readme-img\consolidation灰度占比.png)

其中，最低占比为第三张图片，占比为11%.



其他种类图片大多占比小于1%，最高占比为6%.



使用灰度判断的方法，对consolidation种类划分病灶区域，选用不同大小的kernel，效果对比如下。（以图11为输入数据）
