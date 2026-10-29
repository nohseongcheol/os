"""內建 커널의 檔案·通信·屏幕 호출과 中文 異常. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as 操作系統
import sys as 運行時

def 輸出(*值, 分隔條=" ", 結尾="\n", **舊的參數列):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 舊的參數列: 舊的參數列["sep"] = 分隔條
    if "end" not in 舊的參數列: 舊的參數列["end"] = 結尾
    print(*值, **舊的參數列)

整數 = int
命令參數列 = 運行時.argv
嘗試執行再次錯誤 = 11

class 系統錯誤(OSError):
    def __init__(自身值, 編號, 說明="操作系統 작업에 실패했습니다."):
        super().__init__(編號, 說明)
        自身值.編號 = 編號
        自身值.說明 = 說明

def 運行環境調用(函數, *實參):
    try:
        return 函數(*實參)
    except OSError as 錯誤:
        編號 = 錯誤.args[0] if 錯誤.args else 0
        raise 系統錯誤(編號)

def 編碼文本(文本):
    return 文本.encode("utf-8")

def 解碼文本(資料):
    return 資料.decode("utf-8")

def 讀取檔案(名稱):
    return 運行環境調用(操作系統.read, 名稱)

def 寫入檔案(名稱, 資料):
    return 運行環境調用(操作系統.write, 名稱, 資料)

def 移除檔案(名稱):
    return 運行環境調用(操作系統.remove, 名稱)

def 打開數據報(埠編號):
    return 運行環境調用(操作系統.udp_open, 埠編號)

def 發送數據報(端點, 埠編號, 資料):
    return 運行環境調用(操作系統.udp_send, 端點, 埠編號, 資料)

def 發送外部數據報(端點, 地址, 埠編號, 資料):
    return 運行環境調用(操作系統.udp_sendto, 端點, 地址, 埠編號, 資料)

def 接收數據報(端點):
    return 運行環境調用(操作系統.udp_recv, 端點)

def 關閉網路(端點):
    return 運行環境調用(操作系統.udp_close, 端點)

def 繪製矩形(*實參):
    return 運行環境調用(操作系統.rect, *實參)

def 屏幕大小():
    return 運行環境調用(操作系統.screen_size)

def 等待狀態用於繪圖():
    return 運行環境調用(操作系統.wait_key)

毫秒 = 操作系統.ticks_ms
