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

ମେସିନ୍_ଠିକଣା = bytes.fromhex('525400123456')
ପ୍ରବେଶ_ପଥ_ହାର୍ଡୱେର୍_ଠିକଣା = bytes.fromhex('52550a000202')
ଇଣ୍ଟର୍ନେଟ୍_ଠିକଣା_ମୂଲ୍ୟ = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍:
    def __init__(자신, ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍=2121, 전달규칙들=(), କ୍ୟାପଚର୍_କରିବା=False, ଅତିଥି_ଠିକଣା=None, ଆୟୋଜକ_ଠିକଣା='127.0.0.1'):
        if not 1024 <= ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍ <= 65535 or 50000 <= ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍ <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍ = ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        ଅତିଥି_ଠିକଣା = ଅତିଥି_ଠିକଣା or 자신.ip_config['IP']
        qemu_network(자신.ip_config, ଅତିଥି_ଠିକଣା)
        ଠିକଣା=ipaddress.IPv4Address(ଅତିଥି_ଠିକଣା)
        자신.ଅତିଥି_ଠିକଣା=str(ଠିକଣା); 자신.현재주소=ଠିକଣା.packed
        ଠିକଣା=ipaddress.IPv4Address(ଆୟୋଜକ_ଠିକଣା)
        if ଠିକଣା.is_multicast or str(ଠିକଣା)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ଆୟୋଜକ_ଠିକଣା=str(ଠିକଣା)
        자신.କ୍ୟାପଚର୍_କରିବା = କ୍ୟାପଚର୍_କରିବା; 자신.ଚିହ୍ନଟ_ଲଗ୍ = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍)} | {('tcp', ଡାଟା_ସ୍ଥିତି) for ଡାଟା_ସ୍ଥିତି in range(50000,50008)}
        for ନିୟମ_ମୂଲ୍ୟ in 전달규칙들:
            ପଥ_ଉପାଦାନ = ନିୟମ_ମୂଲ୍ୟ.split(':')
            if len(ପଥ_ଉପାଦାନ) != 3 or ପଥ_ଉପାଦାନ[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            통신규약, ଆୟୋଜକ, ଅତିଥି = ପଥ_ଉପାଦାନ[0], int(ପଥ_ଉପାଦାନ[1]), int(ପଥ_ଉପାଦାନ[2])
            if not 1024 <= ଆୟୋଜକ <= 65535 or not 1 <= ଅତିଥି <= 65535 or (통신규약, ଆୟୋଜକ) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + ନିୟମ_ମୂଲ୍ୟ)
            사용중주소.add((통신규약, ଆୟୋଜକ)); 자신.전달규칙들.append((통신규약, ଆୟୋଜକ, ଅତିଥି))
        자신.수신창구들 = []
        for _ in range(2):
            ସର୍ଭର୍_ମୂଲ୍ୟ = socket.socket()
            ସର୍ଭର୍_ମୂଲ୍ୟ.bind(('127.0.0.1', 0)); ସର୍ଭର୍_ମୂଲ୍ୟ.listen(1); ସର୍ଭର୍_ମୂଲ୍ୟ.setblocking(False)
            자신.수신창구들.append(ସର୍ଭର୍_ମୂଲ୍ୟ)
        자신.접속자들 = [None, None]
        자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ = [bytearray(), bytearray()]
        자신.ଇଥରନେଟ୍ = bytearray(); 자신.직렬전문 = bytearray(); 자신.탈출됨 = 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅବୈଧ = False
        자신.ବିରାମ_ଘଟଣା = threading.Event(); 자신.ତ୍ରୁଟି = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.작업가닥 = threading.Thread(target=자신.ଚକ୍ରାକାର_ମୂଲ୍ୟ, daemon=True)
        자신.작업가닥.start()

    def 전달인수(자신):
        직렬접속번호, ଇଥରନେଟ୍_ପୋର୍ଟ = [ଷ୍ଟ୍ରିଂ_ଡାଟା.getsockname()[1] for ଷ୍ଟ୍ରିଂ_ଡାଟା in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.ଅତିଥି_ଠିକଣା) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍, 자신.ଅତିଥି_ଠିକଣା)
        for ପୋର୍ଟ୍_ନମ୍ଵର୍ in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(ପୋର୍ଟ୍_ନମ୍ଵର୍, 자신.ଅତିଥି_ଠିକଣା)
        for 통신규약, ଆୟୋଜକ, ଅତିଥି in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(통신규약, ଆୟୋଜକ, 자신.ଅତିଥି_ଠିକଣା, ଅତିଥି)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ଆୟୋଜକ_ଠିକଣା+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(직렬접속번호),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ଇଥରନେଟ୍_ପୋର୍ଟ),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def 실행틀(자신, ପ୍ୟାକେଟ୍_ଡାଟା):
        자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ[1] += struct.pack('!I', len(ପ୍ୟାକେଟ୍_ଡାଟା)) + ପ୍ୟାକେଟ୍_ଡାଟା

    def ଚିହ୍ନଟ_ପ୍ୟାକେଟ୍(자신, 방향, ପ୍ୟାକେଟ୍_ଡାଟା):
        if not 자신.କ୍ୟାପଚର୍_କରିବା or len(ପ୍ୟାକେଟ୍_ଡାଟା)<20: return
        ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=(ପ୍ୟାକେଟ୍_ଡାଟା[0]&15)*4
        ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ={'time':time.monotonic(),'direction':방향,'bytes':len(ପ୍ୟାକେଟ୍_ଡାଟା),'protocol':ପ୍ୟାକେଟ୍_ଡାଟା[9]}
        if ପ୍ୟାକେଟ୍_ଡାଟା[9]==6 and len(ପ୍ୟାକେଟ୍_ଡାଟା)>=ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ+20:
            원본자료,ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା,순서번호,확인번호,설정비트,ଓ୍ୱିଣ୍ଡୋ=struct.unpack_from('!HHIIHH',ପ୍ୟାକେଟ୍_ଡାଟା,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.update(source=원본자료,destination=ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା,seq=순서번호,ack=확인번호,flags=설정비트&255,window=ଓ୍ୱିଣ୍ଡୋ,
                        payload=len(ପ୍ୟାକେଟ୍_ଡାଟା)-ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ-((ପ୍ୟାକେଟ୍_ଡାଟା[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ+12]>>4)*4))
        자신.ଚିହ୍ନଟ_ଲଗ୍.append(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)
        if len(자신.ଚିହ୍ନଟ_ଲଗ୍)>2048: del 자신.ଚିହ୍ନଟ_ଲଗ୍[:1024]

    def 직렬전문입력(자신, ଡାଟା):
        for ବର୍ଣ୍ଣ_କୋଡ଼୍ in ଡାଟା:
            if ବର୍ଣ୍ଣ_କୋଡ଼୍ == 192:
                if 자신.직렬전문 and not 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅବୈଧ and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.직렬전문)>=20 and 자신.직렬전문[0]>>4==4:
                        ଠିକଣା=bytes(자신.직렬전문[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(ଠିକଣା)))
                            자신.현재주소=ଠିକଣା
                        except ValueError:
                            pass
                    자신.ଚିହ୍ନଟ_ପ୍ୟାକେଟ୍('from_guest',자신.직렬전문)
                    자신.실행틀(ପ୍ରବେଶ_ପଥ_ହାର୍ଡୱେର୍_ଠିକଣା + ମେସିନ୍_ଠିକଣା + b'\x08\x00' + 자신.직렬전문)
                    자신.커널발신틀수 += 1
                자신.직렬전문.clear(); 자신.탈출됨 = 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅବୈଧ = False
            elif ବର୍ଣ୍ଣ_କୋଡ଼୍ == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if ବର୍ଣ୍ଣ_କୋଡ଼୍ not in (220, 221): 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅବୈଧ = True
                    ବର୍ଣ୍ଣ_କୋଡ଼୍ = 192 if ବର୍ଣ୍ଣ_କୋଡ଼୍ == 220 else 219
                    자신.탈출됨 = False
                if len(자신.직렬전문) < 1600: 자신.직렬전문.append(ବର୍ଣ୍ଣ_କୋଡ଼୍)
                else: 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଅବୈଧ = True

    def 이더넷입력(자신, ଡାଟା):
        자신.ଇଥରନେଟ୍ += ଡାଟା
        while len(자신.ଇଥରନେଟ୍) >= 4:
            개수 = struct.unpack_from('!I', 자신.ଇଥରନେଟ୍)[0]
            if 개수 > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.ଇଥରନେଟ୍) < 개수 + 4: return
            실행틀 = bytes(자신.ଇଥରନେଟ୍[4:4+개수]); del 자신.ଇଥରନେଟ୍[:4+개수]
            if len(실행틀) < 14: continue
            if 실행틀[12:14] == b'\x08\x06' and len(실행틀) >= 42:
                ଠିକଣା_ସ୍ପଷ୍ଟତା_ପ୍ୟାକେଟ୍ = 실행틀[14:42]
                if ଠିକଣା_ସ୍ପଷ୍ଟତା_ପ୍ୟାକେଟ୍[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and ଠିକଣା_ସ୍ପଷ୍ଟତା_ପ୍ୟାକେଟ୍[24:28] == 자신.현재주소:
                    응답자료 = ଠିକଣା_ସ୍ପଷ୍ଟତା_ପ୍ୟାକେଟ୍[:6] + b'\x00\x02' + ମେସିନ୍_ଠିକଣା + 자신.현재주소 + ଠିକଣା_ସ୍ପଷ୍ଟତା_ପ୍ୟାକେଟ୍[8:18]
                    자신.실행틀(실행틀[6:12] + ମେସିନ୍_ଠିକଣା + b'\x08\x06' + 응답자료)
            elif 실행틀[12:14] == b'\x08\x00':
                ପ୍ୟାକେଟ୍_ଡାଟା = 실행틀[14:]
                자신.ଚିହ୍ନଟ_ପ୍ୟାକେଟ୍('to_guest',ପ୍ୟାକେଟ୍_ଡାଟା)
                자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ[0] += b'\xc0' + ପ୍ୟାକେଟ୍_ଡାଟା.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def ଚକ୍ରାକାର_ମୂଲ୍ୟ(자신):
        try:
            while not 자신.ବିରାମ_ଘଟଣା.is_set():
                읽기대상들 = [ଷ୍ଟ୍ରିଂ_ଡାଟା for 순번, ଷ୍ଟ୍ରିଂ_ଡାଟା in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [ଷ୍ଟ୍ରିଂ_ଡାଟା for ଷ୍ଟ୍ରିଂ_ଡାଟା in 자신.접속자들 if ଷ୍ଟ୍ରିଂ_ଡାଟା is not None]
                쓰기대상들 = [ଷ୍ଟ୍ରିଂ_ଡାଟା for 순번, ଷ୍ଟ୍ରିଂ_ଡାଟା in enumerate(자신.접속자들) if ଷ୍ଟ୍ରିଂ_ଡାଟା is not None and 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ[순번]]
                읽을수있음, 쓸수있음, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for ଷ୍ଟ୍ରିଂ_ଡାଟା in 읽을수있음:
                    if ଷ୍ଟ୍ରିଂ_ଡାଟା in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(ଷ୍ଟ୍ରିଂ_ଡାଟା); 자신.접속자들[순번], _ = ଷ୍ଟ୍ରିଂ_ଡାଟା.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(ଷ୍ଟ୍ରିଂ_ଡାଟା); ଡାଟା = ଷ୍ଟ୍ରିଂ_ଡାଟା.recv(16384)
                        if not ଡାଟା: return
                        (자신.직렬전문입력 if 순번 == 0 else 자신.이더넷입력)(ଡାଟା)
                for ଷ୍ଟ୍ରିଂ_ଡାଟା in 쓸수있음:
                    순번 = 자신.접속자들.index(ଷ୍ଟ୍ରିଂ_ଡାଟା)
                    try: 개수 = ଷ୍ଟ୍ରିଂ_ଡାଟା.send(자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ[순번])
                    except BlockingIOError: continue
                    del 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ[순번][:개수]
                if any(len(둘째값) > 1024 * 1024 for 둘째값 in 자신.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ବିଚାରାଧୀନ):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.ବିରାମ_ଘଟଣା.is_set(): 자신.ତ୍ରୁଟି = str(보조항목)

    def ବନ୍ଦ_କରନ୍ତୁ(자신):
        자신.ବିରାମ_ଘଟଣା.set(); 자신.작업가닥.join(timeout=2)
        for ଷ୍ଟ୍ରିଂ_ଡାଟା in 자신.수신창구들 + 자신.접속자들:
            if ଷ୍ଟ୍ରିଂ_ଡାଟା is not None: ଷ୍ଟ୍ରିଂ_ଡାଟା.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *ଯୁକ୍ତି_ଆରେ): 자신.ବନ୍ଦ_କରନ୍ତୁ()
