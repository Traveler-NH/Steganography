from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
def FormatArray(array, mode):   #因numpy.array()生成的数组在运用时产生了困难，故创建此函数。
        Array = []
        index_1d = 0
        for rows in array:
            index_2d = 0
            Array.append([])
            for cols in rows:
                Array[index_1d].append([])
                for channels in cols:
                    if mode ==  1:
                        Array[index_1d][index_2d].append('{:08b}'.format(channels))   #把十进制整型转换为8位无符号二进制(字符串)
                    if mode == 2:
                        Array[index_1d][index_2d].append(int(channels, 2))   #把二进制文本转换为十进制整型
                index_2d = index_2d + 1
            index_1d = index_1d + 1
        return Array
def array_str(array):
    im_string = ''
    for rows in array:
        for cols in rows:
            for channels in cols:
                for char in channels:
                    im_string = im_string + char   #用于把数组中的所有元素排列成一个字符串
    return im_string    

print('请选择模式。合成混合图输入1，取出里图输入2')
mode = int(input('模式：'))

if mode == 1:
    im_outside = Image.open(input('表图路径：').replace('\\', '/')).convert('RGBA')   #载入图片并转为RGBA模式(4*8像素，真彩+透明通道)
    im_inside = Image.open(input('里图路径：').replace('\\', '/')).convert('RGBA')   #因为在Python中反斜杠是转义字符，所以要用replace方法替换掉文件路径中的反斜杠
    im_mix_path = input('混合图输出路径及其文件名：').replace('\\', '/')

    im_outside_array = FormatArray(np.array(im_outside), 1)   #把图片转换成三维数组(元素已转换为二进制文本)
    im_inside_array = FormatArray(np.array(im_inside), 1)

    im_outside_strlist = list(array_str(im_outside_array))   #把图片数组排列成字符串，再转换成每个元素都是一个字符的数组
    im_inside_strlist = list(array_str(im_inside_array))

    n = 0
    for index in im_inside_strlist:   #用里图的每一个bit替换掉混合图每个字节的最后一个bit
        im_outside_strlist[(n+1)*8-1] = index
        n = n + 1
    im_inside_width = list('{:016b}'.format(im_inside.size[0]))   #从里到外依次为：取里图宽度、把里图宽度转换为16位无符号二进制(字符串)、把二进制字符串转化为每个字符为一个元素的数组
    im_inside_high = list('{:016b}'.format(im_inside.size[1]))   #从里到外依次为：取里图高度、把里图高度转换为16位无符号二进制(字符串)、把二进制字符串转化为每个字符为一个元素的数组
    n = 0
    for index in im_inside_width + im_inside_high:   #把里图的尺寸存入混合图每个字节中的第7个bit，即把里图的宽度和高度转换为二进制字符串后，再用依次用每一个字符替换掉混合图每个字节的第7个bit（此时的“混合图”实际上是整合后的表图，因为其尚未存入到混合图数组中）
        im_outside_strlist[(n+1)*8-2] = index
        n = n + 1

    im_mix_array = [ [ [ [] for k in range(4) ] for j in range(im_outside.size[0]) ] for i in range(im_outside.size[1]) ]   #创建混合图的三维数组，以便下面把整合后的表图存进去
    index = 0
    index_1d = 0
    for rows in im_mix_array:   #把整合后的表图存入混合图的数组中
        index_2d = 0
        for cols in rows:
            index_3d = 0
            for channels in cols:
                im_mix_array[index_1d][index_2d][index_3d] = im_outside_strlist[index] + im_outside_strlist[index+1] + im_outside_strlist[index+2] + im_outside_strlist[index+3] + im_outside_strlist[index+4] + im_outside_strlist[index+5] + im_outside_strlist[index+6] + im_outside_strlist[index+7]
                index = index + 8
                index_3d = index_3d + 1
            index_2d = index_2d + 1
        index_1d = index_1d + 1
    im_mix = np.array(FormatArray(im_mix_array, 2), dtype='uint8')   #从里到外依次为：把混合图数组中的元素转换为十进制整型、再转换为8位无符号整型

    plt.imsave(im_mix_path, im_mix)   #把数组输出成图片

if mode == 2:
    im_mix = Image.open(input('混合图路径：').replace('\\', '/')).convert('RGBA')
    im_inside_path = input('里图输出路径及其文件名：').replace('\\', '/')
    im_mix_array = FormatArray(np.array(im_mix), 1)
    im_mix_strlist = list(array_str(im_mix_array))

    im_inside_width = ''
    for index in range(16):
        im_inside_width = im_inside_width + im_mix_strlist[(index+1)*8-2]
    im_inside_high = ''
    for index in range(16):
        im_inside_high = im_inside_high + im_mix_strlist[(16+index+1)*8-2]
    im_inside_width = int(im_inside_width, 2)
    im_inside_high = int(im_inside_high, 2)
    
    im_inside_strlist = [[] for i in range(8*4*im_inside_width*im_inside_high)]
    n = 0
    for index in im_inside_strlist:
        im_inside_strlist[n] = im_mix_strlist[(n+1)*8-1]
        n = n + 1
    im_inside_array = [ [ [ [] for k in range(4) ] for j in range(im_inside_width) ] for i in range(im_inside_high) ]
    n = 0
    index_1d = 0
    for rows in im_inside_array:
        index_2d = 0
        for cols in rows:
            index_3d = 0
            for channels in cols:
                im_inside_array[index_1d][index_2d][index_3d] = im_inside_strlist[n] + im_inside_strlist[n+1] + im_inside_strlist[n+2] + im_inside_strlist[n+3] + im_inside_strlist[n+4] + im_inside_strlist[n+5] + im_inside_strlist[n+6] + im_inside_strlist[n+7]
                n = n + 8
                index_3d = index_3d + 1
            index_2d = index_2d + 1
        index_1d = index_1d + 1
    im_inside = np.array(FormatArray(im_inside_array, 2), dtype='uint8')

    plt.imsave(im_inside_path, im_inside)