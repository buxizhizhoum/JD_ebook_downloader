用于截屏的脚本，实现对电子书的截屏备份。

jd_ebook_screen_capture_keyboard.py 
    
    用来对京东电子书客户端进行截屏，仅在windows 10进行了测试。

    程序依赖python库PIL和pyautogui. PIL用于截屏，pyautogui用于模拟键盘操作实现翻页。
    
    用法：
        python jd_ebook_screen_capture_keyboard.py --dir "../screen" --page_num 100
    
        dir         用于指定存储截屏所获图片的路径
        page_num    用于指定需要多少次翻页操作
                    每次翻页会截屏一次，由于电脑不一定在一个屏幕显示一页，所以这个次数和电子书的页数不一定相等。