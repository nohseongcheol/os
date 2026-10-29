from 中文 import 輸出, 寫入檔案, 讀取檔案, 編碼文本, 解碼文本
資料 = "PYTHON 檔案: zh_Hant 😀\n"
寫入檔案("python.txt", 編碼文本(資料))
讀取文本值 = 解碼文本(讀取檔案("python.txt"))
assert 讀取文本值 == 資料
輸出(讀取文本值, 結尾="")
