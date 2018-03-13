#用于截屏的脚本，实现对电子书的截屏备份。

#测试环境：

    windows 10

    Python2.7

    PIL             截屏

    pyautogui       模拟键盘和鼠标操作

    OpenCV          图像处理

#安装：
    Python：
        下载：官网下载对应的安装包，运行。
        https://www.python.org/downloads/release/python-2714/

    PIL：
        pip install PIL

    pyautogui：
        pip install pyautogui

    OpenCV：
        pip install opencv

#jd_ebook_screen_capture_keyboard.py
    
    用来对京东电子书客户端进行截屏。

    用法：
        python jd_ebook_screen_capture_keyboard.py --dir "../screen" --page_num 100
    
        dir         用于指定存储截屏所获图片的路径
        page_num    用于指定需要多少次翻页操作
                    每次翻页会截屏一次，由于电脑不一定在一个屏幕显示一页，所以这个次数和电子书的页数不一定相等。


todo： find_button, capture_screen, select button by user, locate button.

stringio

辨别两侧黑边，裁剪。