"""內建 內核值 MicroPython에서 사용하는 한글 函數 名稱."""
import jkoros as 操作系統
輸出 = print
讀取檔案 = 操作系統.read
寫入檔案 = 操作系統.write
移除檔案 = 操作系統.remove
讀取輸入 = 操作系統.stdin
繪製矩形 = 操作系統.rect
等待狀態用於繪圖 = 操作系統.wait_key
毫秒 = 操作系統.ticks_ms
打開數據報 = 操作系統.udp_open
發送數據報 = 操作系統.udp_send
發送外部數據報 = 操作系統.udp_sendto
接收數據報 = 操作系統.udp_recv
關閉網路 = 操作系統.udp_close

def 解碼文本(資料):
    return 資料.decode("utf-8")
