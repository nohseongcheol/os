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

计算机地址 = bytes.fromhex('525400123456')
网关硬件地址 = bytes.fromhex('52550a000202')
互联网地址值 = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 网络桥接:
    def __init__(自身值, 文件传送端口编号=2121, 转发中规则列=(), 捕获=False, 客户机地址=None, 宿主地址='127.0.0.1'):
        if not 1024 <= 文件传送端口编号 <= 65535 or 50000 <= 文件传送端口编号 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        自身值.文件传送端口编号 = 文件传送端口编号
        自身值.ip_config = read_config(Path(__file__).resolve().parents[1])
        客户机地址 = 客户机地址 or 自身值.ip_config['IP']
        qemu_network(自身值.ip_config, 客户机地址)
        地址=ipaddress.IPv4Address(客户机地址)
        自身值.客户机地址=str(地址); 自身值.当前地址=地址.packed
        地址=ipaddress.IPv4Address(宿主地址)
        if 地址.is_multicast or str(地址)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        自身值.宿主地址=str(地址)
        自身值.捕获 = 捕获; 自身值.追踪日志 = []
        自身值.转发中规则列 = []
        已占用 = {('tcp', 文件传送端口编号)} | {('tcp', 数据位置) for 数据位置 in range(50000,50008)}
        for 规则值 in 转发中规则列:
            路径组件 = 规则值.split(':')
            if len(路径组件) != 3 or 路径组件[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            网络ABI, 宿主, 客户机 = 路径组件[0], int(路径组件[1]), int(路径组件[2])
            if not 1024 <= 宿主 <= 65535 or not 1 <= 客户机 <= 65535 or (网络ABI, 宿主) in 已占用:
                raise ValueError('invalid or duplicate forward: ' + 规则值)
            已占用.add((网络ABI, 宿主)); 自身值.转发中规则列.append((网络ABI, 宿主, 客户机))
        自身值.接收端口列 = []
        for _ in range(2):
            服务器值 = socket.socket()
            服务器值.bind(('127.0.0.1', 0)); 服务器值.listen(1); 服务器值.setblocking(False)
            自身值.接收端口列.append(服务器值)
        自身值.客户端列 = [None, None]
        自身值.是否待处理 = [bytearray(), bytearray()]
        自身值.以太网 = bytearray(); 自身值.串行数据报 = bytearray(); 自身值.已转义 = 自身值.是否无效 = False
        自身值.暂停事件 = threading.Event(); 自身值.错误 = None
        自身值.帧列目标侧客户机 = 自身值.帧列起点客户机 = 0
        自身值.后台任务 = threading.Thread(target=自身值.周期值, daemon=True)
        自身值.后台任务.start()

    def 已转发参数(自身值):
        串行端口编号, 以太网端口 = [字符串数据.getsockname()[1] for 字符串数据 in 自身值.接收端口列]
        转发中规则 = 'user,id=wan,' + qemu_network(自身值.ip_config, 自身值.客户机地址) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(自身值.文件传送端口编号, 自身值.客户机地址)
        for 端口编号 in range(50000, 50008):
            转发中规则 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(端口编号, 自身值.客户机地址)
        for 网络ABI, 宿主, 客户机 in 自身值.转发中规则列:
            转发中规则 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(网络ABI, 宿主, 自身值.客户机地址, 客户机)
        转发中规则=转发中规则.replace('127.0.0.1:',自身值.宿主地址+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(串行端口编号),
                '-serial', 'chardev:slip', '-netdev', 转发中规则,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(以太网端口),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 执行状态帧(自身值, 数据包数据):
        自身值.是否待处理[1] += struct.pack('!I', len(数据包数据)) + 数据包数据

    def 追踪数据包(自身值, 方向, 数据包数据):
        if not 自身值.捕获 or len(数据包数据)<20: return
        偏移值=(数据包数据[0]&15)*4
        条目值={'time':time.monotonic(),'direction':方向,'bytes':len(数据包数据),'protocol':数据包数据[9]}
        if 数据包数据[9]==6 and len(数据包数据)>=偏移值+20:
            原始数据,目的地址数据地址,排序编号,确认状态编号,配置项位列,窗口=struct.unpack_from('!HHIIHH',数据包数据,偏移值)
            条目值.update(source=原始数据,destination=目的地址数据地址,seq=排序编号,ack=确认状态编号,flags=配置项位列&255,window=窗口,
                        payload=len(数据包数据)-偏移值-((数据包数据[偏移值+12]>>4)*4))
        自身值.追踪日志.append(条目值)
        if len(自身值.追踪日志)>2048: del 自身值.追踪日志[:1024]

    def 串行线路_Internet_协议输入(自身值, 数据):
        for 字符代码 in 数据:
            if 字符代码 == 192:
                if 自身值.串行数据报 and not 自身值.是否无效 and not 自身值.已转义:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(自身值.串行数据报)>=20 and 自身值.串行数据报[0]>>4==4:
                        地址=bytes(自身值.串行数据报[12:16])
                        try:
                            qemu_network(自身值.ip_config, str(ipaddress.IPv4Address(地址)))
                            自身值.当前地址=地址
                        except ValueError:
                            pass
                    自身值.追踪数据包('from_guest',自身值.串行数据报)
                    自身值.执行状态帧(网关硬件地址 + 计算机地址 + b'\x08\x00' + 自身值.串行数据报)
                    自身值.帧列起点客户机 += 1
                自身值.串行数据报.clear(); 自身值.已转义 = 自身值.是否无效 = False
            elif 字符代码 == 219 and not 自身值.已转义:
                自身值.已转义 = True
            else:
                if 自身值.已转义:
                    if 字符代码 not in (220, 221): 自身值.是否无效 = True
                    字符代码 = 192 if 字符代码 == 220 else 219
                    自身值.已转义 = False
                if len(自身值.串行数据报) < 1600: 自身值.串行数据报.append(字符代码)
                else: 自身值.是否无效 = True

    def 以太网输入(自身值, 数据):
        自身值.以太网 += 数据
        while len(自身值.以太网) >= 4:
            项目个数 = struct.unpack_from('!I', 自身值.以太网)[0]
            if 项目个数 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(自身值.以太网) < 项目个数 + 4: return
            执行状态帧 = bytes(自身值.以太网[4:4+项目个数]); del 自身值.以太网[:4+项目个数]
            if len(执行状态帧) < 14: continue
            if 执行状态帧[12:14] == b'\x08\x06' and len(执行状态帧) >= 42:
                地址分辨率数据包 = 执行状态帧[14:42]
                if 地址分辨率数据包[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 地址分辨率数据包[24:28] == 自身值.当前地址:
                    响应 = 地址分辨率数据包[:6] + b'\x00\x02' + 计算机地址 + 自身值.当前地址 + 地址分辨率数据包[8:18]
                    自身值.执行状态帧(执行状态帧[6:12] + 计算机地址 + b'\x08\x06' + 响应)
            elif 执行状态帧[12:14] == b'\x08\x00':
                数据包数据 = 执行状态帧[14:]
                自身值.追踪数据包('to_guest',数据包数据)
                自身值.是否待处理[0] += b'\xc0' + 数据包数据.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                自身值.帧列目标侧客户机 += 1

    def 周期值(自身值):
        try:
            while not 自身值.暂停事件.is_set():
                读取器集 = [字符串数据 for 序数索引, 字符串数据 in enumerate(自身值.接收端口列) if 自身值.客户端列[序数索引] is None]
                读取器集 += [字符串数据 for 字符串数据 in 自身值.客户端列 if 字符串数据 is not None]
                写入器集 = [字符串数据 for 序数索引, 字符串数据 in enumerate(自身值.客户端列) if 字符串数据 is not None and 自身值.是否待处理[序数索引]]
                能够读取, 可写, _ = select.select(读取器集, 写入器集, [], .05)
                for 字符串数据 in 能够读取:
                    if 字符串数据 in 自身值.接收端口列:
                        序数索引 = 自身值.接收端口列.index(字符串数据); 自身值.客户端列[序数索引], _ = 字符串数据.accept(); 自身值.客户端列[序数索引].setblocking(False)
                    else:
                        序数索引 = 自身值.客户端列.index(字符串数据); 数据 = 字符串数据.recv(16384)
                        if not 数据: return
                        (自身值.串行线路_Internet_协议输入 if 序数索引 == 0 else 自身值.以太网输入)(数据)
                for 字符串数据 in 可写:
                    序数索引 = 自身值.客户端列.index(字符串数据)
                    try: 项目个数 = 字符串数据.send(自身值.是否待处理[序数索引])
                    except BlockingIOError: continue
                    del 自身值.是否待处理[序数索引][:项目个数]
                if any(len(第二值) > 1024 * 1024 for 第二值 in 自身值.是否待处理):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 辅助条目:
            if not 自身值.暂停事件.is_set(): 自身值.错误 = str(辅助条目)

    def 关闭(自身值):
        自身值.暂停事件.set(); 自身值.后台任务.join(timeout=2)
        for 字符串数据 in 自身值.接收端口列 + 自身值.客户端列:
            if 字符串数据 is not None: 字符串数据.close()

    def __enter__(自身值): return 自身值
    def __exit__(自身值, *参数数组): 自身值.关闭()
