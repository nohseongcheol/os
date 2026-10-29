"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class 回顯測試夾具:
    def __enter__(自身值):
        自身值.連接狀態控制 = socket.socket(); 自身值.連接狀態控制.bind(('127.0.0.1', 0)); 自身值.連接狀態控制.listen(1)
        自身值.數據報控制 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 自身值.數據報控制.bind(('127.0.0.1', 0))
        自身值.連接狀態控制.settimeout(30); 自身值.數據報控制.settimeout(30)
        自身值.TCP埠 = 自身值.連接狀態控制.getsockname()[1]; 自身值.UDP埠 = 自身值.數據報控制.getsockname()[1]
        自身值.錯誤列 = []; 自身值.擁有已接收 = {}
        def 連接狀態控制():
            try:
                接通狀態, _ = 自身值.連接狀態控制.accept()
                with 接通狀態:
                    接通狀態.settimeout(5); 資料 = bytearray()
                    while b'\n' not in 資料:
                        片段值 = 接通狀態.recv(512)
                        if not 片段值: raise RuntimeError('TCP EOF before request')
                        資料.extend(片段值)
                    自身值.擁有已接收['tcp'] = bytes(資料); 接通狀態.sendall(資料)
            except Exception as 輔助條目: 自身值.錯誤列.append(str(輔助條目))
        def 數據報控制():
            try:
                資料, 對端值 = 自身值.數據報控制.recvfrom(512); 自身值.擁有已接收['udp'] = 資料; 自身值.數據報控制.sendto(資料, 對端值)
            except Exception as 輔助條目: 自身值.錯誤列.append(str(輔助條目))
        自身值.執行緒集 = [threading.Thread(target=檔案條目, daemon=True) for 檔案條目 in (連接狀態控制, 數據報控制)]
        for 終端條目 in 自身值.執行緒集: 終端條目.start()
        return 自身值

    def __exit__(自身值, *實際參數陣列):
        自身值.連接狀態控制.close(); 自身值.數據報控制.close()
        for 終端條目 in 自身值.執行緒集: 終端條目.join(timeout=1)
