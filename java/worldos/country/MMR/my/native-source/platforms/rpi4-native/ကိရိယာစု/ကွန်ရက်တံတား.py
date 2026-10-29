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

စက်လိပ်စာ = bytes.fromhex('525400123456')
관문기계주소 = bytes.fromhex('52550a000202')
အင်တာနက်လိပ်စာတန်ဖိုး = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class ကွန်ရက်တံတား:
    def __init__(자신, ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း=2121, 전달규칙들=(), 포착여부=False, ဧည့်သည်လိပ်စာ=None, အိမ်ရှင်လိပ်စာ='127.0.0.1'):
        if not 1024 <= ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း <= 65535 or 50000 <= ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း = ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ဧည့်သည်လိပ်စာ = ဧည့်သည်လိပ်စာ or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ဧည့်သည်လိပ်စာ)
        လိပ်စာ=ipaddress.IPv4Address(ဧည့်သည်လိပ်စာ)
        자신.ဧည့်သည်လိပ်စာ=str(လိပ်စာ); 자신.လက်ရှိလိပ်စာ=လိပ်စာ.packed
        လိပ်စာ=ipaddress.IPv4Address(အိမ်ရှင်လိပ်စာ)
        if လိပ်စာ.is_multicast or str(လိပ်စာ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.အိမ်ရှင်လိပ်စာ=str(လိပ်စာ)
        자신.포착여부 = 포착여부; 자신.ခြေရာမှတ်တမ်း = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း)} | {('tcp', ဒေတာနေရာ) for ဒေတာနေရာ in range(50000,50008)}
        for စည်းမျဉ်းတန်ဖိုး in 전달규칙들:
            လမ်းကြောင်းအစိတ်အပိုင်း = စည်းမျဉ်းတန်ဖိုး.split(':')
            if len(လမ်းကြောင်းအစိတ်အပိုင်း) != 3 or လမ်းကြောင်းအစိတ်အပိုင်း[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, အိမ်ရှင်, ဧည့်သည် = လမ်းကြောင်းအစိတ်အပိုင်း[0], int(လမ်းကြောင်းအစိတ်အပိုင်း[1]), int(လမ်းကြောင်းအစိတ်အပိုင်း[2])
            if not 1024 <= အိမ်ရှင် <= 65535 or not 1 <= ဧည့်သည် <= 65535 or (통신규약, အိမ်ရှင်) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + စည်းမျဉ်းတန်ဖိုး)
            사용중주소.add((통신규약, အိမ်ရှင်)); 자신.전달규칙들.append((통신규약, အိမ်ရှင်, ဧည့်သည်))
        자신.수신창구들 = []
        for _ in range(2):
            ဝန်ဆောင်စက်တန်ဖိုး = socket.socket()
            ဝန်ဆောင်စက်တန်ဖိုး.bind(('127.0.0.1', 0)); ဝန်ဆောင်စက်တန်ဖိုး.listen(1); ဝန်ဆောင်စက်တန်ဖိုး.setblocking(False)
            자신.수신창구들.append(ဝန်ဆောင်စက်တန်ဖိုး)
        자신.접속자들 = [None, None]
        자신.ဖြစ်သောဆိုင်းငံ့ = [bytearray(), bytearray()]
        자신.이더넷자료 = bytearray(); 자신.အစဉ်ဆက်ဒေတာစာ = bytearray(); 자신.탈출됨 = 자신.ဖြစ်သောမမှန်ကန် = False
        자신.ခဏရပ်ဖြစ်ရပ် = threading.Event(); 자신.အမှား = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.အလုပ်သမား = threading.Thread(target=자신.순환, daemon=True)
        자신.အလုပ်သမား.start()

    def 전달인수(자신):
        အစဉ်ဆက်ဆက်သွယ်ပေါက်ကိန်း, 이더넷접속번호 = [အက္ခရာစဉ်ဒေတာ.getsockname()[1] for အက္ခရာစဉ်ဒေတာ in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ဧည့်သည်လိပ်စာ) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ဖိုင်လွှဲပြောင်းဆက်သွယ်ပေါက်ကိန်း, 자신.ဧည့်သည်လိပ်စာ)
        for ဆက်သွယ်ပေါက်ကိန်း in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(ဆက်သွယ်ပေါက်ကိန်း, 자신.ဧည့်သည်လိပ်စာ)
        for 통신규약, အိမ်ရှင်, ဧည့်သည် in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, အိမ်ရှင်, 자신.ဧည့်သည်လိပ်စာ, ဧည့်သည်)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.အိမ်ရှင်လိပ်စာ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(အစဉ်ဆက်ဆက်သွယ်ပေါက်ကိန်း),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(이더넷접속번호),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def လုပ်ဆောင်မှုဘောင်(자신, ဒေတာထုပ်ဒေတာ):
        자신.ဖြစ်သောဆိုင်းငံ့[1] += struct.pack('!I', len(ဒေတာထုပ်ဒေတာ)) + ဒေတာထုပ်ဒေတာ

    def ခြေရာဒေတာထုပ်(자신, 방향, ဒေတာထုပ်ဒေတာ):
        if not 자신.포착여부 or len(ဒေတာထုပ်ဒေတာ)<20: return
        အရွေ့တန်ဖိုး=(ဒေတာထုပ်ဒေတာ[0]&15)*4
        အချက်တန်ဖိုး={'time':time.monotonic(),'direction':방향,'bytes':len(ဒေတာထုပ်ဒေတာ),'protocol':ဒေတာထုပ်ဒေတာ[9]}
        if ဒေတာထုပ်ဒေတာ[9]==6 and len(ဒေတာထုပ်ဒေတာ)>=အရွေ့တန်ဖိုး+20:
            မူရင်းဒေတာ,ဦးတည်ရာဒေတာလိပ်စာ,အစဉ်ကိန်း,확인번호,ပြင်ဆင်မှုဘစ်များ,ဝင်း=struct.unpack_from('!HHIIHH',ဒေတာထုပ်ဒေတာ,အရွေ့တန်ဖိုး)
            အချက်တန်ဖိုး.update(source=မူရင်းဒေတာ,destination=ဦးတည်ရာဒေတာလိပ်စာ,seq=အစဉ်ကိန်း,ack=확인번호,flags=ပြင်ဆင်မှုဘစ်များ&255,window=ဝင်း,
                        payload=len(ဒေတာထုပ်ဒေတာ)-အရွေ့တန်ဖိုး-((ဒေတာထုပ်ဒေတာ[အရွေ့တန်ဖိုး+12]>>4)*4))
        자신.ခြေရာမှတ်တမ်း.append(အချက်တန်ဖိုး)
        if len(자신.ခြေရာမှတ်တမ်း)>2048: del 자신.ခြေရာမှတ်တမ်း[:1024]

    def 직렬전문입력(자신, ဒေတာ):
        for အက္ခရာကုဒ် in ဒေတာ:
            if အက္ခရာကုဒ် == 192:
                if 자신.အစဉ်ဆက်ဒေတာစာ and not 자신.ဖြစ်သောမမှန်ကန် and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.အစဉ်ဆက်ဒေတာစာ)>=20 and 자신.အစဉ်ဆက်ဒေတာစာ[0]>>4==4:
                        လိပ်စာ=bytes(자신.အစဉ်ဆက်ဒေတာစာ[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(လိပ်စာ)))
                            자신.လက်ရှိလိပ်စာ=လိပ်စာ
                        except ValueError:
                            pass
                    자신.ခြေရာဒေတာထုပ်('from_guest',자신.အစဉ်ဆက်ဒေတာစာ)
                    자신.လုပ်ဆောင်မှုဘောင်(관문기계주소 + စက်လိပ်စာ + b'\x08\x00' + 자신.အစဉ်ဆက်ဒေတာစာ)
                    자신.커널발신틀수 += 1
                자신.အစဉ်ဆက်ဒေတာစာ.clear(); 자신.탈출됨 = 자신.ဖြစ်သောမမှန်ကန် = False
            elif အက္ခရာကုဒ် == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if အက္ခရာကုဒ် not in (220, 221): 자신.ဖြစ်သောမမှန်ကန် = True
                    အက္ခရာကုဒ် = 192 if အက္ခရာကုဒ် == 220 else 219
                    자신.탈출됨 = False
                if len(자신.အစဉ်ဆက်ဒေတာစာ) < 1600: 자신.အစဉ်ဆက်ဒေတာစာ.append(အက္ခရာကုဒ်)
                else: 자신.ဖြစ်သောမမှန်ကန် = True

    def 이더넷입력(자신, ဒေတာ):
        자신.이더넷자료 += ဒေတာ
        while len(자신.이더넷자료) >= 4:
            အရေအတွက် = struct.unpack_from('!I', 자신.이더넷자료)[0]
            if အရေအတွက် > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.이더넷자료) < အရေအတွက် + 4: return
            လုပ်ဆောင်မှုဘောင် = bytes(자신.이더넷자료[4:4+အရေအတွက်]); del 자신.이더넷자료[:4+အရေအတွက်]
            if len(လုပ်ဆောင်မှုဘောင်) < 14: continue
            if လုပ်ဆောင်မှုဘောင်[12:14] == b'\x08\x06' and len(လုပ်ဆောင်မှုဘောင်) >= 42:
                လိပ်စာကြည်လင်ပြတ်သားမှုဒေတာထုပ် = လုပ်ဆောင်မှုဘောင်[14:42]
                if လိပ်စာကြည်လင်ပြတ်သားမှုဒေတာထုပ်[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and လိပ်စာကြည်လင်ပြတ်သားမှုဒေတာထုပ်[24:28] == 자신.လက်ရှိလိပ်စာ:
                    응답자료 = လိပ်စာကြည်လင်ပြတ်သားမှုဒေတာထုပ်[:6] + b'\x00\x02' + စက်လိပ်စာ + 자신.လက်ရှိလိပ်စာ + လိပ်စာကြည်လင်ပြတ်သားမှုဒေတာထုပ်[8:18]
                    자신.လုပ်ဆောင်မှုဘောင်(လုပ်ဆောင်မှုဘောင်[6:12] + စက်လိပ်စာ + b'\x08\x06' + 응답자료)
            elif လုပ်ဆောင်မှုဘောင်[12:14] == b'\x08\x00':
                ဒေတာထုပ်ဒေတာ = လုပ်ဆောင်မှုဘောင်[14:]
                자신.ခြေရာဒေတာထုပ်('to_guest',ဒေတာထုပ်ဒေတာ)
                자신.ဖြစ်သောဆိုင်းငံ့[0] += b'\xc0' + ဒေတာထုပ်ဒေတာ.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def 순환(자신):
        try:
            while not 자신.ခဏရပ်ဖြစ်ရပ်.is_set():
                읽기대상들 = [အက္ခရာစဉ်ဒေတာ for အစဉ်အမှတ်, အက္ခရာစဉ်ဒေတာ in enumerate(자신.수신창구들) if 자신.접속자들[အစဉ်အမှတ်] is None]
                읽기대상들 += [အက္ခရာစဉ်ဒေတာ for အက္ခရာစဉ်ဒေတာ in 자신.접속자들 if အက္ခရာစဉ်ဒေတာ is not None]
                쓰기대상들 = [အက္ခရာစဉ်ဒေတာ for အစဉ်အမှတ်, အက္ခရာစဉ်ဒေတာ in enumerate(자신.접속자들) if အက္ခရာစဉ်ဒေတာ is not None and 자신.ဖြစ်သောဆိုင်းငံ့[အစဉ်အမှတ်]]
                နိုင်ဖတ်, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for အက္ခရာစဉ်ဒေတာ in နိုင်ဖတ်:
                    if အက္ခရာစဉ်ဒေတာ in 자신.수신창구들:
                        အစဉ်အမှတ် = 자신.수신창구들.index(အက္ခရာစဉ်ဒေတာ); 자신.접속자들[အစဉ်အမှတ်], _ = အက္ခရာစဉ်ဒေတာ.accept(); 자신.접속자들[အစဉ်အမှတ်].setblocking(False)
                    else:
                        အစဉ်အမှတ် = 자신.접속자들.index(အက္ခရာစဉ်ဒေတာ); ဒေတာ = အက္ခရာစဉ်ဒေတာ.recv(16384)
                        if not ဒေတာ: return
                        (자신.직렬전문입력 if အစဉ်အမှတ် == 0 else 자신.이더넷입력)(ဒေတာ)
                for အက္ခရာစဉ်ဒေတာ in 쓸수있음:
                    အစဉ်အမှတ် = 자신.접속자들.index(အက္ခရာစဉ်ဒေတာ)
                    try: အရေအတွက် = အက္ခရာစဉ်ဒေတာ.send(자신.ဖြစ်သောဆိုင်းငံ့[အစဉ်အမှတ်])
                    except BlockingIOError: continue
                    del 자신.ဖြစ်သောဆိုင်းငံ့[အစဉ်အမှတ်][:အရေအတွက်]
                if any(len(ဒုတိယတန်ဖိုး) > 1024 * 1024 for ဒုတိယတန်ဖိုး in 자신.ဖြစ်သောဆိုင်းငံ့):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ခဏရပ်ဖြစ်ရပ်.is_set(): 자신.အမှား = str(보조항목)

    def ပိတ်(자신):
        자신.ခဏရပ်ဖြစ်ရပ်.set(); 자신.အလုပ်သမား.join(timeout=2)
        for အက္ခရာစဉ်ဒေတာ in 자신.수신창구들 + 자신.접속자들:
            if အက္ခရာစဉ်ဒေတာ is not None: အက္ခရာစဉ်ဒေတာ.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ပေးအချက်အခင်းအကျင်း): 자신.ပိတ်()
