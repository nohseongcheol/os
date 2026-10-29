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

địaChỉMáy = bytes.fromhex('525400123456')
địaChỉPhầnCứngCổngNối = bytes.fromhex('52550a000202')
giáTrịĐịaChỉLiênMạng = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class cầuNốiMạng:
    def __init__(giáTrịBảnThân, sốCổngChuyểnGiaoTệp=2121, cácQuyTắcViệcChuyểnTiếp=(), thuGiữ=False, địaChỉKhách=None, địaChỉChủ='127.0.0.1'):
        if not 1024 <= sốCổngChuyểnGiaoTệp <= 65535 or 50000 <= sốCổngChuyểnGiaoTệp <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        giáTrịBảnThân.sốCổngChuyểnGiaoTệp = sốCổngChuyểnGiaoTệp
        giáTrịBảnThân.ip_config = read_config(Path(__file__).resolve().parents[1])
        địaChỉKhách = địaChỉKhách or giáTrịBảnThân.ip_config['IP']
        qemu_network(giáTrịBảnThân.ip_config, địaChỉKhách)
        địaChỉ=ipaddress.IPv4Address(địaChỉKhách)
        giáTrịBảnThân.địaChỉKhách=str(địaChỉ); giáTrịBảnThân.địaChỉHiệnTại=địaChỉ.packed
        địaChỉ=ipaddress.IPv4Address(địaChỉChủ)
        if địaChỉ.is_multicast or str(địaChỉ)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        giáTrịBảnThân.địaChỉChủ=str(địaChỉ)
        giáTrịBảnThân.thuGiữ = thuGiữ; giáTrịBảnThân.nhậtKýDấuVết = []
        giáTrịBảnThân.cácQuyTắcViệcChuyểnTiếp = []
        đãChiếm = {('tcp', sốCổngChuyểnGiaoTệp)} | {('tcp', vịTríDữLiệu) for vịTríDữLiệu in range(50000,50008)}
        for giáTrịQuyTắc in cácQuyTắcViệcChuyểnTiếp:
            thànhPhầnĐườngDẫn = giáTrịQuyTắc.split(':')
            if len(thànhPhầnĐườngDẫn) != 3 or thànhPhầnĐườngDẫn[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            ABIMạng, Chủ, khách = thànhPhầnĐườngDẫn[0], int(thànhPhầnĐườngDẫn[1]), int(thànhPhầnĐườngDẫn[2])
            if not 1024 <= Chủ <= 65535 or not 1 <= khách <= 65535 or (ABIMạng, Chủ) in đãChiếm:
                raise ValueError('invalid or duplicate forward: ' + giáTrịQuyTắc)
            đãChiếm.add((ABIMạng, Chủ)); giáTrịBảnThân.cácQuyTắcViệcChuyểnTiếp.append((ABIMạng, Chủ, khách))
        giáTrịBảnThân.nhậnCácCổng = []
        for _ in range(2):
            giáTrịMáyChủ = socket.socket()
            giáTrịMáyChủ.bind(('127.0.0.1', 0)); giáTrịMáyChủ.listen(1); giáTrịMáyChủ.setblocking(False)
            giáTrịBảnThân.nhậnCácCổng.append(giáTrịMáyChủ)
        giáTrịBảnThân.cácMáyKhách = [None, None]
        giáTrịBảnThân.làĐangChờ = [bytearray(), bytearray()]
        giáTrịBảnThân.ethernet = bytearray(); giáTrịBảnThân.điệnDữLiệuNốiTiếp = bytearray(); giáTrịBảnThân.đãThoát = giáTrịBảnThân.làKhôngHợpLệ = False
        giáTrịBảnThân.sựKiệnTạmDừng = threading.Event(); giáTrịBảnThân.lỗi = None
        giáTrịBảnThân.kháchĐếnCácKhung = giáTrịBảnThân.kháchTừCácKhung = 0
        giáTrịBảnThân.bộLàmViệc = threading.Thread(target=giáTrịBảnThân.giáTrịChuKỳ, daemon=True)
        giáTrịBảnThân.bộLàmViệc.start()

    def đốiSốĐãChuyểnTiếp(giáTrịBảnThân):
        sốCổngNốiTiếp, cổngEthernet = [dữLiệuChuỗi.getsockname()[1] for dữLiệuChuỗi in giáTrịBảnThân.nhậnCácCổng]
        quyTắcViệcChuyểnTiếp = 'user,id=wan,' + qemu_network(giáTrịBảnThân.ip_config, giáTrịBảnThân.địaChỉKhách) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(giáTrịBảnThân.sốCổngChuyểnGiaoTệp, giáTrịBảnThân.địaChỉKhách)
        for sốCổng in range(50000, 50008):
            quyTắcViệcChuyểnTiếp += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(sốCổng, giáTrịBảnThân.địaChỉKhách)
        for ABIMạng, Chủ, khách in giáTrịBảnThân.cácQuyTắcViệcChuyểnTiếp:
            quyTắcViệcChuyểnTiếp += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(ABIMạng, Chủ, giáTrịBảnThân.địaChỉKhách, khách)
        quyTắcViệcChuyểnTiếp=quyTắcViệcChuyểnTiếp.replace('127.0.0.1:',giáTrịBảnThân.địaChỉChủ+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(sốCổngNốiTiếp),
                '-serial', 'chardev:slip', '-netdev', quyTắcViệcChuyểnTiếp,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(cổngEthernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def khungViệcThựcThi(giáTrịBảnThân, dữLiệuGóiTin):
        giáTrịBảnThân.làĐangChờ[1] += struct.pack('!I', len(dữLiệuGóiTin)) + dữLiệuGóiTin

    def góiTinDấuVết(giáTrịBảnThân, hướng, dữLiệuGóiTin):
        if not giáTrịBảnThân.thuGiữ or len(dữLiệuGóiTin)<20: return
        giáTrịĐộLệch=(dữLiệuGóiTin[0]&15)*4
        giáTrịMục={'time':time.monotonic(),'direction':hướng,'bytes':len(dữLiệuGóiTin),'protocol':dữLiệuGóiTin[9]}
        if dữLiệuGóiTin[9]==6 and len(dữLiệuGóiTin)>=giáTrịĐộLệch+20:
            dữLiệuNguyênBản,địaChỉDữLiệuĐích,sốThứTự,sốSựXácNhận,cácBitCấuHình,cửaSổ=struct.unpack_from('!HHIIHH',dữLiệuGóiTin,giáTrịĐộLệch)
            giáTrịMục.update(source=dữLiệuNguyênBản,destination=địaChỉDữLiệuĐích,seq=sốThứTự,ack=sốSựXácNhận,flags=cácBitCấuHình&255,window=cửaSổ,
                        payload=len(dữLiệuGóiTin)-giáTrịĐộLệch-((dữLiệuGóiTin[giáTrịĐộLệch+12]>>4)*4))
        giáTrịBảnThân.nhậtKýDấuVết.append(giáTrịMục)
        if len(giáTrịBảnThân.nhậtKýDấuVết)>2048: del giáTrịBảnThân.nhậtKýDấuVết[:1024]

    def đầuVàoSLIP(giáTrịBảnThân, DữLiệu):
        for mãKýTự in DữLiệu:
            if mãKýTự == 192:
                if giáTrịBảnThân.điệnDữLiệuNốiTiếp and not giáTrịBảnThân.làKhôngHợpLệ and not giáTrịBảnThân.đãThoát:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(giáTrịBảnThân.điệnDữLiệuNốiTiếp)>=20 and giáTrịBảnThân.điệnDữLiệuNốiTiếp[0]>>4==4:
                        địaChỉ=bytes(giáTrịBảnThân.điệnDữLiệuNốiTiếp[12:16])
                        try:
                            qemu_network(giáTrịBảnThân.ip_config, str(ipaddress.IPv4Address(địaChỉ)))
                            giáTrịBảnThân.địaChỉHiệnTại=địaChỉ
                        except ValueError:
                            pass
                    giáTrịBảnThân.góiTinDấuVết('from_guest',giáTrịBảnThân.điệnDữLiệuNốiTiếp)
                    giáTrịBảnThân.khungViệcThựcThi(địaChỉPhầnCứngCổngNối + địaChỉMáy + b'\x08\x00' + giáTrịBảnThân.điệnDữLiệuNốiTiếp)
                    giáTrịBảnThân.kháchTừCácKhung += 1
                giáTrịBảnThân.điệnDữLiệuNốiTiếp.clear(); giáTrịBảnThân.đãThoát = giáTrịBảnThân.làKhôngHợpLệ = False
            elif mãKýTự == 219 and not giáTrịBảnThân.đãThoát:
                giáTrịBảnThân.đãThoát = True
            else:
                if giáTrịBảnThân.đãThoát:
                    if mãKýTự not in (220, 221): giáTrịBảnThân.làKhôngHợpLệ = True
                    mãKýTự = 192 if mãKýTự == 220 else 219
                    giáTrịBảnThân.đãThoát = False
                if len(giáTrịBảnThân.điệnDữLiệuNốiTiếp) < 1600: giáTrịBảnThân.điệnDữLiệuNốiTiếp.append(mãKýTự)
                else: giáTrịBảnThân.làKhôngHợpLệ = True

    def đầuVàoEthernet(giáTrịBảnThân, DữLiệu):
        giáTrịBảnThân.ethernet += DữLiệu
        while len(giáTrịBảnThân.ethernet) >= 4:
            sốLượngPhầnMục = struct.unpack_from('!I', giáTrịBảnThân.ethernet)[0]
            if sốLượngPhầnMục > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(giáTrịBảnThân.ethernet) < sốLượngPhầnMục + 4: return
            khungViệcThựcThi = bytes(giáTrịBảnThân.ethernet[4:4+sốLượngPhầnMục]); del giáTrịBảnThân.ethernet[:4+sốLượngPhầnMục]
            if len(khungViệcThựcThi) < 14: continue
            if khungViệcThựcThi[12:14] == b'\x08\x06' and len(khungViệcThựcThi) >= 42:
                góiTinĐộPhânGiảiĐịaChỉ = khungViệcThựcThi[14:42]
                if góiTinĐộPhânGiảiĐịaChỉ[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and góiTinĐộPhânGiảiĐịaChỉ[24:28] == giáTrịBảnThân.địaChỉHiệnTại:
                    phảnHồi = góiTinĐộPhânGiảiĐịaChỉ[:6] + b'\x00\x02' + địaChỉMáy + giáTrịBảnThân.địaChỉHiệnTại + góiTinĐộPhânGiảiĐịaChỉ[8:18]
                    giáTrịBảnThân.khungViệcThựcThi(khungViệcThựcThi[6:12] + địaChỉMáy + b'\x08\x06' + phảnHồi)
            elif khungViệcThựcThi[12:14] == b'\x08\x00':
                dữLiệuGóiTin = khungViệcThựcThi[14:]
                giáTrịBảnThân.góiTinDấuVết('to_guest',dữLiệuGóiTin)
                giáTrịBảnThân.làĐangChờ[0] += b'\xc0' + dữLiệuGóiTin.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                giáTrịBảnThân.kháchĐếnCácKhung += 1

    def giáTrịChuKỳ(giáTrịBảnThân):
        try:
            while not giáTrịBảnThân.sựKiệnTạmDừng.is_set():
                cácBộĐọc = [dữLiệuChuỗi for chỉSốThứBậc, dữLiệuChuỗi in enumerate(giáTrịBảnThân.nhậnCácCổng) if giáTrịBảnThân.cácMáyKhách[chỉSốThứBậc] is None]
                cácBộĐọc += [dữLiệuChuỗi for dữLiệuChuỗi in giáTrịBảnThân.cácMáyKhách if dữLiệuChuỗi is not None]
                cácBộGhi = [dữLiệuChuỗi for chỉSốThứBậc, dữLiệuChuỗi in enumerate(giáTrịBảnThân.cácMáyKhách) if dữLiệuChuỗi is not None and giáTrịBảnThân.làĐangChờ[chỉSốThứBậc]]
                cóThểĐọc, ghiĐược, _ = select.select(cácBộĐọc, cácBộGhi, [], .05)
                for dữLiệuChuỗi in cóThểĐọc:
                    if dữLiệuChuỗi in giáTrịBảnThân.nhậnCácCổng:
                        chỉSốThứBậc = giáTrịBảnThân.nhậnCácCổng.index(dữLiệuChuỗi); giáTrịBảnThân.cácMáyKhách[chỉSốThứBậc], _ = dữLiệuChuỗi.accept(); giáTrịBảnThân.cácMáyKhách[chỉSốThứBậc].setblocking(False)
                    else:
                        chỉSốThứBậc = giáTrịBảnThân.cácMáyKhách.index(dữLiệuChuỗi); DữLiệu = dữLiệuChuỗi.recv(16384)
                        if not DữLiệu: return
                        (giáTrịBảnThân.đầuVàoSLIP if chỉSốThứBậc == 0 else giáTrịBảnThân.đầuVàoEthernet)(DữLiệu)
                for dữLiệuChuỗi in ghiĐược:
                    chỉSốThứBậc = giáTrịBảnThân.cácMáyKhách.index(dữLiệuChuỗi)
                    try: sốLượngPhầnMục = dữLiệuChuỗi.send(giáTrịBảnThân.làĐangChờ[chỉSốThứBậc])
                    except BlockingIOError: continue
                    del giáTrịBảnThân.làĐangChờ[chỉSốThứBậc][:sốLượngPhầnMục]
                if any(len(giáTrịThứHai) > 1024 * 1024 for giáTrịThứHai in giáTrịBảnThân.làĐangChờ):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as mụcPhụTrợ:
            if not giáTrịBảnThân.sựKiệnTạmDừng.is_set(): giáTrịBảnThân.lỗi = str(mụcPhụTrợ)

    def đóng(giáTrịBảnThân):
        giáTrịBảnThân.sựKiệnTạmDừng.set(); giáTrịBảnThân.bộLàmViệc.join(timeout=2)
        for dữLiệuChuỗi in giáTrịBảnThân.nhậnCácCổng + giáTrịBảnThân.cácMáyKhách:
            if dữLiệuChuỗi is not None: dữLiệuChuỗi.close()

    def __enter__(giáTrịBảnThân): return giáTrịBảnThân
    def __exit__(giáTrịBảnThân, *mảngĐốiSố): giáTrịBảnThân.đóng()
