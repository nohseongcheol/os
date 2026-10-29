"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

計算機地址 = bytes.fromhex('525400123456')
網關硬件地址 = bytes.fromhex('52550a000202')
互聯網地址值 = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 網路橋接:
    def __init__(自身值, 檔案傳送埠編號=2121, 轉發中規則列=(), 捕獲=False, 客戶機地址=None, 宿主地址='127.0.0.1'):
        if not 1024 <= 檔案傳送埠編號 <= 65535 or 50000 <= 檔案傳送埠編號 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        自身值.檔案傳送埠編號 = 檔案傳送埠編號
        自身值.ip_config = read_config(Path(__file__).resolve().parents[1])
        客戶機地址 = 客戶機地址 or 自身值.ip_config['IP']
        qemu_network(自身值.ip_config, 客戶機地址)
        地址=ipaddress.IPv4Address(客戶機地址)
        自身值.客戶機地址=str(地址); 自身值.當前地址=地址.packed
        地址=ipaddress.IPv4Address(宿主地址)
        if 地址.is_multicast or str(地址)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        自身值.宿主地址=str(地址)
        自身值.捕獲 = 捕獲; 自身值.追蹤日誌 = []
        自身值.轉發中規則列 = []
        已佔用 = {('tcp', 檔案傳送埠編號)} | {('tcp', 資料位置) for 資料位置 in range(50000,50008)}
        for 規則值 in 轉發中規則列:
            路徑組件 = 規則值.split(':')
            if len(路徑組件) != 3 or 路徑組件[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            網路ABI, 宿主, 客戶機 = 路徑組件[0], int(路徑組件[1]), int(路徑組件[2])
            if not 1024 <= 宿主 <= 65535 or not 1 <= 客戶機 <= 65535 or (網路ABI, 宿主) in 已佔用:
                raise ValueError('invalid or duplicate forward: ' + 規則值)
            已佔用.add((網路ABI, 宿主)); 自身值.轉發中規則列.append((網路ABI, 宿主, 客戶機))
        自身值.接收埠列 = []
        for _ in range(2):
            服務器值 = socket.socket()
            服務器值.bind(('127.0.0.1', 0)); 服務器值.listen(1); 服務器值.setblocking(False)
            自身值.接收埠列.append(服務器值)
        自身值.客戶端列 = [None, None]
        自身值.是否待處理 = [bytearray(), bytearray()]
        自身值.以太網 = bytearray(); 自身值.串行數據報 = bytearray(); 自身值.已轉義 = 自身值.是否無效 = False
        自身值.暫停事件 = threading.Event(); 自身值.錯誤 = None
        自身值.幀列目標側客戶機 = 自身值.幀列起點客戶機 = 0
        自身值.後臺任務 = threading.Thread(target=自身值.週期值, daemon=True)
        自身值.後臺任務.start()

    def 已轉發實際參數(自身值):
        串行埠編號, 以太網埠 = [字符串資料.getsockname()[1] for 字符串資料 in 自身值.接收埠列]
        轉發中規則 = 'user,id=wan,' + qemu_network(自身值.ip_config, 自身值.客戶機地址) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(自身值.檔案傳送埠編號, 自身值.客戶機地址)
        for 埠編號 in range(50000, 50008):
            轉發中規則 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(埠編號, 自身值.客戶機地址)
        for 網路ABI, 宿主, 客戶機 in 自身值.轉發中規則列:
            轉發中規則 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(網路ABI, 宿主, 自身值.客戶機地址, 客戶機)
        轉發中規則=轉發中規則.replace('127.0.0.1:',自身值.宿主地址+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(串行埠編號),
                '-serial', 'chardev:slip', '-netdev', 轉發中規則,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(以太網埠),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 執行狀態幀(自身值, 數據包資料):
        自身值.是否待處理[1] += struct.pack('!I', len(數據包資料)) + 數據包資料

    def 追蹤數據包(自身值, 方向, 數據包資料):
        if not 自身值.捕獲 or len(數據包資料)<20: return
        偏移值=(數據包資料[0]&15)*4
        條目值={'time':time.monotonic(),'direction':方向,'bytes':len(數據包資料),'protocol':數據包資料[9]}
        if 數據包資料[9]==6 and len(數據包資料)>=偏移值+20:
            原始資料,目的地址資料地址,排序編號,確認狀態編號,配置項位元列,窗口=struct.unpack_from('!HHIIHH',數據包資料,偏移值)
            條目值.update(source=原始資料,destination=目的地址資料地址,seq=排序編號,ack=確認狀態編號,flags=配置項位元列&255,window=窗口,
                        payload=len(數據包資料)-偏移值-((數據包資料[偏移值+12]>>4)*4))
        自身值.追蹤日誌.append(條目值)
        if len(自身值.追蹤日誌)>2048: del 自身值.追蹤日誌[:1024]

    def 串行線路_Internet_協議輸入(自身值, 資料):
        for 字元程式碼 in 資料:
            if 字元程式碼 == 192:
                if 自身值.串行數據報 and not 自身值.是否無效 and not 自身值.已轉義:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(自身值.串行數據報)>=20 and 自身值.串行數據報[0]>>4==4:
                        地址=bytes(自身值.串行數據報[12:16])
                        try:
                            qemu_network(自身值.ip_config, str(ipaddress.IPv4Address(地址)))
                            自身值.當前地址=地址
                        except ValueError:
                            pass
                    自身值.追蹤數據包('from_guest',自身值.串行數據報)
                    自身值.執行狀態幀(網關硬件地址 + 計算機地址 + b'\x08\x00' + 自身值.串行數據報)
                    自身值.幀列起點客戶機 += 1
                自身值.串行數據報.clear(); 自身值.已轉義 = 自身值.是否無效 = False
            elif 字元程式碼 == 219 and not 自身值.已轉義:
                自身值.已轉義 = True
            else:
                if 自身值.已轉義:
                    if 字元程式碼 not in (220, 221): 自身值.是否無效 = True
                    字元程式碼 = 192 if 字元程式碼 == 220 else 219
                    自身值.已轉義 = False
                if len(自身值.串行數據報) < 1600: 自身值.串行數據報.append(字元程式碼)
                else: 自身值.是否無效 = True

    def 以太網輸入(自身值, 資料):
        自身值.以太網 += 資料
        while len(自身值.以太網) >= 4:
            項目個數 = struct.unpack_from('!I', 自身值.以太網)[0]
            if 項目個數 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(自身值.以太網) < 項目個數 + 4: return
            執行狀態幀 = bytes(自身值.以太網[4:4+項目個數]); del 自身值.以太網[:4+項目個數]
            if len(執行狀態幀) < 14: continue
            if 執行狀態幀[12:14] == b'\x08\x06' and len(執行狀態幀) >= 42:
                地址分辨率數據包 = 執行狀態幀[14:42]
                if 地址分辨率數據包[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 地址分辨率數據包[24:28] == 自身值.當前地址:
                    響應 = 地址分辨率數據包[:6] + b'\x00\x02' + 計算機地址 + 自身值.當前地址 + 地址分辨率數據包[8:18]
                    自身值.執行狀態幀(執行狀態幀[6:12] + 計算機地址 + b'\x08\x06' + 響應)
            elif 執行狀態幀[12:14] == b'\x08\x00':
                數據包資料 = 執行狀態幀[14:]
                自身值.追蹤數據包('to_guest',數據包資料)
                自身值.是否待處理[0] += b'\xc0' + 數據包資料.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                自身值.幀列目標側客戶機 += 1

    def 週期值(自身值):
        try:
            while not 自身值.暫停事件.is_set():
                讀取器集 = [字符串資料 for 序數索引, 字符串資料 in enumerate(自身值.接收埠列) if 自身值.客戶端列[序數索引] is None]
                讀取器集 += [字符串資料 for 字符串資料 in 自身值.客戶端列 if 字符串資料 is not None]
                寫入器集 = [字符串資料 for 序數索引, 字符串資料 in enumerate(自身值.客戶端列) if 字符串資料 is not None and 自身值.是否待處理[序數索引]]
                能夠讀取, 可寫, _ = select.select(讀取器集, 寫入器集, [], .05)
                for 字符串資料 in 能夠讀取:
                    if 字符串資料 in 自身值.接收埠列:
                        序數索引 = 自身值.接收埠列.index(字符串資料); 自身值.客戶端列[序數索引], _ = 字符串資料.accept(); 自身值.客戶端列[序數索引].setblocking(False)
                    else:
                        序數索引 = 自身值.客戶端列.index(字符串資料); 資料 = 字符串資料.recv(16384)
                        if not 資料: return
                        (自身值.串行線路_Internet_協議輸入 if 序數索引 == 0 else 自身值.以太網輸入)(資料)
                for 字符串資料 in 可寫:
                    序數索引 = 自身值.客戶端列.index(字符串資料)
                    try: 項目個數 = 字符串資料.send(自身值.是否待處理[序數索引])
                    except BlockingIOError: continue
                    del 自身值.是否待處理[序數索引][:項目個數]
                if any(len(第二值) > 1024 * 1024 for 第二值 in 自身值.是否待處理):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 輔助條目:
            if not 自身值.暫停事件.is_set(): 自身值.錯誤 = str(輔助條目)

    def 關閉(自身值):
        自身值.暫停事件.set(); 自身值.後臺任務.join(timeout=2)
        for 字符串資料 in 自身值.接收埠列 + 自身值.客戶端列:
            if 字符串資料 is not None: 字符串資料.close()

    def __enter__(自身值): return 自身值
    def __exit__(自身值, *實際參數陣列): 自身值.關閉()
