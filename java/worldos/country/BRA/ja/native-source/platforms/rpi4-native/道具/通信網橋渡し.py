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

機械番地 = bytes.fromhex('525400123456')
中継門機器番地 = bytes.fromhex('52550a000202')
インターネット番地値 = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class 通信網橋渡し:
    def __init__(自身値, ファイル転送ポート番号=2121, 転送中規則一覧=(), 捕獲=False, ゲスト番地=None, ホスト番地='127.0.0.1'):
        if not 1024 <= ファイル転送ポート番号 <= 65535 or 50000 <= ファイル転送ポート番号 <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        自身値.ファイル転送ポート番号 = ファイル転送ポート番号
        自身値.ip_config = read_config(Path(__file__).resolve().parents[1])
        ゲスト番地 = ゲスト番地 or 自身値.ip_config['IP']
        qemu_network(自身値.ip_config, ゲスト番地)
        番地=ipaddress.IPv4Address(ゲスト番地)
        自身値.ゲスト番地=str(番地); 自身値.現在番地=番地.packed
        番地=ipaddress.IPv4Address(ホスト番地)
        if 番地.is_multicast or str(番地)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        自身値.ホスト番地=str(番地)
        自身値.捕獲 = 捕獲; 自身値.追跡履歴記録 = []
        自身値.転送中規則一覧 = []
        占有済み = {('tcp', ファイル転送ポート番号)} | {('tcp', データ位置) for データ位置 in range(50000,50008)}
        for 規則値 in 転送中規則一覧:
            経路構成要素 = 規則値.split(':')
            if len(経路構成要素) != 3 or 経路構成要素[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            通信網ABI, ホスト, ゲスト = 経路構成要素[0], int(経路構成要素[1]), int(経路構成要素[2])
            if not 1024 <= ホスト <= 65535 or not 1 <= ゲスト <= 65535 or (通信網ABI, ホスト) in 占有済み:
                raise ValueError('invalid or duplicate forward: ' + 規則値)
            占有済み.add((通信網ABI, ホスト)); 自身値.転送中規則一覧.append((通信網ABI, ホスト, ゲスト))
        自身値.ポート一覧受取 = []
        for _ in range(2):
            サーバー値 = socket.socket()
            サーバー値.bind(('127.0.0.1', 0)); サーバー値.listen(1); サーバー値.setblocking(False)
            自身値.ポート一覧受取.append(サーバー値)
        自身値.接続元一覧 = [None, None]
        自身値.判定未処理 = [bytearray(), bytearray()]
        自身値.Ethernet = bytearray(); 自身値.直列データグラム = bytearray(); 自身値.退避済み = 自身値.判定無効 = False
        自身値.一時停止イベント = threading.Event(); 自身値.エラー = None
        自身値.枠一覧到達先ゲスト = 自身値.枠一覧起点ゲスト = 0
        自身値.作業担当 = threading.Thread(target=自身値.周期値, daemon=True)
        自身値.作業担当.start()

    def 転送済み引数(自身値):
        直列ポート番号, Ethernetポート = [文字列データ.getsockname()[1] for 文字列データ in 自身値.ポート一覧受取]
        転送中規則 = 'user,id=wan,' + qemu_network(自身値.ip_config, 自身値.ゲスト番地) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(自身値.ファイル転送ポート番号, 自身値.ゲスト番地)
        for ポート番号 in range(50000, 50008):
            転送中規則 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(ポート番号, 自身値.ゲスト番地)
        for 通信網ABI, ホスト, ゲスト in 自身値.転送中規則一覧:
            転送中規則 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(通信網ABI, ホスト, 自身値.ゲスト番地, ゲスト)
        転送中規則=転送中規則.replace('127.0.0.1:',自身値.ホスト番地+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(直列ポート番号),
                '-serial', 'chardev:slip', '-netdev', 転送中規則,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(Ethernetポート),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 実行状態枠組(自身値, パケットデータ):
        自身値.判定未処理[1] += struct.pack('!I', len(パケットデータ)) + パケットデータ

    def 追跡パケット(自身値, 方向, パケットデータ):
        if not 自身値.捕獲 or len(パケットデータ)<20: return
        変位量値=(パケットデータ[0]&15)*4
        入口値={'time':time.monotonic(),'direction':方向,'bytes':len(パケットデータ),'protocol':パケットデータ[9]}
        if パケットデータ[9]==6 and len(パケットデータ)>=変位量値+20:
            原本データ,宛先データ番地,順序番号,確認状態番号,構成設定ビット列,窓=struct.unpack_from('!HHIIHH',パケットデータ,変位量値)
            入口値.update(source=原本データ,destination=宛先データ番地,seq=順序番号,ack=確認状態番号,flags=構成設定ビット列&255,window=窓,
                        payload=len(パケットデータ)-変位量値-((パケットデータ[変位量値+12]>>4)*4))
        自身値.追跡履歴記録.append(入口値)
        if len(自身値.追跡履歴記録)>2048: del 自身値.追跡履歴記録[:1024]

    def SLIP入力(自身値, データ):
        for 文字コード in データ:
            if 文字コード == 192:
                if 自身値.直列データグラム and not 自身値.判定無効 and not 自身値.退避済み:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(自身値.直列データグラム)>=20 and 自身値.直列データグラム[0]>>4==4:
                        番地=bytes(自身値.直列データグラム[12:16])
                        try:
                            qemu_network(自身値.ip_config, str(ipaddress.IPv4Address(番地)))
                            自身値.現在番地=番地
                        except ValueError:
                            pass
                    自身値.追跡パケット('from_guest',自身値.直列データグラム)
                    自身値.実行状態枠組(中継門機器番地 + 機械番地 + b'\x08\x00' + 自身値.直列データグラム)
                    自身値.枠一覧起点ゲスト += 1
                自身値.直列データグラム.clear(); 自身値.退避済み = 自身値.判定無効 = False
            elif 文字コード == 219 and not 自身値.退避済み:
                自身値.退避済み = True
            else:
                if 自身値.退避済み:
                    if 文字コード not in (220, 221): 自身値.判定無効 = True
                    文字コード = 192 if 文字コード == 220 else 219
                    自身値.退避済み = False
                if len(自身値.直列データグラム) < 1600: 自身値.直列データグラム.append(文字コード)
                else: 自身値.判定無効 = True

    def Ethernet入力(自身値, データ):
        自身値.Ethernet += データ
        while len(自身値.Ethernet) >= 4:
            項目個数 = struct.unpack_from('!I', 自身値.Ethernet)[0]
            if 項目個数 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(自身値.Ethernet) < 項目個数 + 4: return
            実行状態枠組 = bytes(自身値.Ethernet[4:4+項目個数]); del 自身値.Ethernet[:4+項目個数]
            if len(実行状態枠組) < 14: continue
            if 実行状態枠組[12:14] == b'\x08\x06' and len(実行状態枠組) >= 42:
                番地解像度パケット = 実行状態枠組[14:42]
                if 番地解像度パケット[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and 番地解像度パケット[24:28] == 自身値.現在番地:
                    応答 = 番地解像度パケット[:6] + b'\x00\x02' + 機械番地 + 自身値.現在番地 + 番地解像度パケット[8:18]
                    自身値.実行状態枠組(実行状態枠組[6:12] + 機械番地 + b'\x08\x06' + 応答)
            elif 実行状態枠組[12:14] == b'\x08\x00':
                パケットデータ = 実行状態枠組[14:]
                自身値.追跡パケット('to_guest',パケットデータ)
                自身値.判定未処理[0] += b'\xc0' + パケットデータ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                自身値.枠一覧到達先ゲスト += 1

    def 周期値(自身値):
        try:
            while not 自身値.一時停止イベント.is_set():
                読取器群 = [文字列データ for 序数添字, 文字列データ in enumerate(自身値.ポート一覧受取) if 自身値.接続元一覧[序数添字] is None]
                読取器群 += [文字列データ for 文字列データ in 自身値.接続元一覧 if 文字列データ is not None]
                書込器群 = [文字列データ for 序数添字, 文字列データ in enumerate(自身値.接続元一覧) if 文字列データ is not None and 自身値.判定未処理[序数添字]]
                可能判定読取, 書込可能, _ = select.select(読取器群, 書込器群, [], .05)
                for 文字列データ in 可能判定読取:
                    if 文字列データ in 自身値.ポート一覧受取:
                        序数添字 = 自身値.ポート一覧受取.index(文字列データ); 自身値.接続元一覧[序数添字], _ = 文字列データ.accept(); 自身値.接続元一覧[序数添字].setblocking(False)
                    else:
                        序数添字 = 自身値.接続元一覧.index(文字列データ); データ = 文字列データ.recv(16384)
                        if not データ: return
                        (自身値.SLIP入力 if 序数添字 == 0 else 自身値.Ethernet入力)(データ)
                for 文字列データ in 書込可能:
                    序数添字 = 自身値.接続元一覧.index(文字列データ)
                    try: 項目個数 = 文字列データ.send(自身値.判定未処理[序数添字])
                    except BlockingIOError: continue
                    del 自身値.判定未処理[序数添字][:項目個数]
                if any(len(第二値) > 1024 * 1024 for 第二値 in 自身値.判定未処理):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 補助入口:
            if not 自身値.一時停止イベント.is_set(): 自身値.エラー = str(補助入口)

    def 閉鎖(自身値):
        自身値.一時停止イベント.set(); 自身値.作業担当.join(timeout=2)
        for 文字列データ in 自身値.ポート一覧受取 + 自身値.接続元一覧:
            if 文字列データ is not None: 文字列データ.close()

    def __enter__(自身値): return 自身値
    def __exit__(自身値, *引数配列): 自身値.閉鎖()
