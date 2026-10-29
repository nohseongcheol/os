from 中文 import 輸出, 打開數據報, 發送外部數據報, 接收數據報, 關閉網路, 毫秒
from 中文 import 系統錯誤, 嘗試執行再次錯誤, 編碼文本, 命令參數列, 整數
端點 = 打開數據報(0)
try:
    數據報 = 編碼文本("PYTHON UDP Chinese")
    發送外部數據報(端點, "10.0.2.2", 整數(命令參數列[1]), 數據報)
    運行 = 毫秒()
    while True:
        try:
            回覆, 埠值 = 接收數據報(端點)
            break
        except 系統錯誤 as 錯誤:
            if 錯誤.編號 != 嘗試執行再次錯誤 or 毫秒() - 運行 >= 700:
                raise
    assert 回覆 == 數據報
    輸出("PYTHON 네트워크 驗證: UDP Chinese")
finally:
    關閉網路(端點)
