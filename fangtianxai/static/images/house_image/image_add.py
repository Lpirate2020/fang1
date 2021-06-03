# @Time : 2021/4/24 19:46 
# @Author : Lpirate
# @File : image_add.py 
# @Software: PyCharm

# 给没有图片的文件添加图片

import os, shutil


# 文件复制移动
def copy_test(file_add, target_add):
    """
    :param file_add: # 需要移动的文件夹
    :param target_add: # 目标文件夹
    :return: 无返回
    """
    # file_add = r'E:/0000bs/fang1/fangtianxai/static/images/house_image/change'  # 需要移动的文件夹
    # target_add = r'D:/1'  # 目标文件夹
    path_ = os.path.abspath(file_add)  # os读路径
    target_ = os.path.abspath(target_add)  # os读路径

    for i in os.listdir(file_add):  # 获取文件夹下文件
        new_p = path_ + '\\' + i  # 写的文件地址 这里不知道为什么跳过父目录
        target_add_new = target_ + '\\' + i  # 存的地址

        with open(new_p, 'rb') as rf:  # 打开读取地址
            image_info = rf.read()  # 读取需要写入的地址
            with open(target_add_new, 'wb') as wf:  # 打开写入地址
                wf.write(image_info)  # 写入目标地址

    print("完事")


# copy_test('E:/0000bs/fang1/fangtianxai/static/images/house_image/change', 'D:/1/2')#测试

# 填补空文件
def search(path):
    """
    :param path: 所有图片文件夹的父目录
    :return:
    """
    files = os.listdir(path)  # 查找路径下的所有的文件夹及文件
    for file in files:
        if file != os.path.basename('.idea'):  # 去除工程文件
            if os.path.isdir(file):  # 判断是文件夹还是文件
                if os.listdir(file):  # 判断文件夹是否为空
                    pass
                    # print(os.listdir(file))

                else:
                    change_path = os.path.abspath(file)
                    copy_test('E:/0000bs/fang1/fangtianxai/static/images/house_image/change',change_path)  # 调用自己写的函数

    print(len(files))


path = 'E:/0000bs/fang1/fangtianxai/static/images/house_image'
search(str(path))
