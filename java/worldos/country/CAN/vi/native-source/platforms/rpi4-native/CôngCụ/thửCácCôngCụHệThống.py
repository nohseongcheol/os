#!/usr/bin/env python3
"""dữLiệuThựcTế tựThân 커널의 IP/ICMP, giáTrịTrạngThái giáTrịTruyVấn, 현지어 lệnh, 게스트 chươngTrìnhRa thẩmĐịnh."""
import argparse
import ftplib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import selectors
import signal
import socket
import subprocess
import sys
import tempfile
import time


def chạy():
    BộPhânTích=argparse.ArgumentParser();BộPhânTích.add_argument('--edition',type=Path);BộPhânTích.add_argument('--output',type=Path);BộPhânTích.add_argument('--poweroff-only',action='store_true');cácĐốiSố=BộPhânTích.parse_args()
    gốcCâyDựÁn=Path(__file__).resolve().parents[1];cácThiếtLập={};bảngTraTên={}
    if cácĐốiSố.edition:
        giáTrịQuốcGia=cácĐốiSố.edition.resolve();cácThiếtLập=json.loads((giáTrịQuốcGia/'native.json').read_text());bảngTraTên=cácThiếtLập['identifiers'];gốcCâyDựÁn=giáTrịQuốcGia/cácThiếtLập['source']/cácThiếtLập['native']
        # Edition runner extracts its own QEMU archive and verifies source stamps.
        subprocess.check_call([sys.executable,str(giáTrịQuốcGia/'native-edition.py'),'check'])
        Chủ=giáTrịQuốcGia/'host/qemu'
        if Chủ.is_file():os.environ['QEMU_AARCH64']=str(Chủ)
    CôngCụ=gốcCâyDựÁn/Path(cácThiếtLập.get('runner','CôngCụ/thựcThiLệnh.py')).parent
    sys.path.insert(0,str(CôngCụ))
    def đọc(tên):
        đườngDẫn=CôngCụ/(bảngTraTên.get(tên,tên)+'.py');giáTrịQuyƯớc=importlib.util.spec_from_file_location('test_'+tên,str(đườngDẫn));giáTrịMôĐun=importlib.util.module_from_spec(giáTrịQuyƯớc);giáTrịQuyƯớc.loader.exec_module(giáTrịMôĐun);return giáTrịMôĐun
    môĐunViệcThựcThi=đọc('thựcThiLệnh');môĐunMạng=đọc('cầuNốiMạng');lệnh=getattr(môĐunViệcThựcThi,bảngTraTên.get('lệnh','lệnh'));kiểuCầuNối=getattr(môĐunMạng,bảngTraTên.get('cầuNốiMạng','cầuNốiMạng'))
    giáTrịBíDanh=cácThiếtLập.get('commands',{}).get('aliases',{'ipconfig':'아이피설정','ip':'địaChỉIP','ping':'thửPhảnHồi','route':'경로표','netstat':'통신현황','ps':'작업목록','top':'작업현황','free':'기억현황','df':'저장현황','uptime':'가동시간','poweroff':'tắtNguồnĐiện','help':'hiệnTrợGiúp'})
    sys.path.insert(0,str(gốcCâyDựÁn/'tools'))
    from ip_config import read_config
    import ipaddress
    ipSettings=read_config(gốcCâyDựÁn);ipNetwork=ipaddress.IPv4Network(ipSettings['network'])
    ipHosts=[str(ipNetwork.network_address+i) for i in range(4,min(ipNetwork.num_addresses-1,255)) if str(ipNetwork.network_address+i) not in (ipSettings['IP'],ipSettings['GATEWAY'])]
    ipTestMap={'10.0.2.15':ipSettings['IP'],'10.0.2.20':ipHosts[0],'10.0.2.21':ipHosts[1],
               '10.0.2.254':str(ipNetwork.broadcast_address-1),'10.0.2.0':str(ipNetwork.network_address),
               '10.0.2.2':ipSettings['GATEWAY'],'255.255.255.0':ipSettings['NETMASK']}
    def ipTestText(text):
        return re.sub(r'10\.0\.2\.(?:254|15|20|21|0|2)(?![0-9])|255\.255\.255\.0',lambda match:ipTestMap[match.group()],text)
    ĐầuRa=cácĐốiSố.output or gốcCâyDựÁn/'build/verification/system-tools';ĐầuRa.mkdir(parents=True,exist_ok=True)
    giáTrịBáoCáo={'passed':False,'country':cácThiếtLập.get('country','jkoros'),'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    bảnGhiNhậtKý=bytearray();giáTrịDãy=[0]
    with tempfile.TemporaryDirectory(prefix='native-system-') as giáTrịTạm:
        đườngDẫnĐiềuKhiển=Path(giáTrịTạm)/'qmp.sock'
        while True:
            with socket.socket() as tìmKiếmGiáTrị:tìmKiếmGiáTrị.bind(('127.0.0.1',0));sốCổng=tìmKiếmGiáTrị.getsockname()[1]
            if not 50000<=sốCổng<=50007:break
        with kiểuCầuNối(sốCổng,thuGiữ=True,địaChỉKhách=ipTestText('10.0.2.20'),địaChỉChủ='127.0.0.2') as giáTrịCầuNối:
            giáTrịTiếnTrình=subprocess.Popen(lệnh()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(đườngDẫnĐiềuKhiển)]+giáTrịCầuNối.đốiSốĐãChuyểnTiếp(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,start_new_session=True)
            phầnMụcChọn=selectors.DefaultSelector();phầnMụcChọn.register(giáTrịTiếnTrình.stdout,selectors.EVENT_READ)
            def nhận(hiệnGiáTrị,chạy=0,giáTrịGiớiHạn=45):
                phầnKết=time.monotonic()+giáTrịGiớiHạn
                while hiệnGiáTrị not in bảnGhiNhậtKý[chạy:]:
                    if time.monotonic()>phầnKết or giáTrịTiếnTrình.poll() is not None:raise AssertionError('Missing '+repr(hiệnGiáTrị)+'\n'+bảnGhiNhậtKý[chạy:].decode('utf-8','replace'))
                    for giáTrịPhím,_ in phầnMụcChọn.select(.1):
                        DữLiệu=giáTrịPhím.fileobj.read(65536)
                        if DữLiệu:bảnGhiNhậtKý.extend(DữLiệu)
                return bảnGhiNhậtKý[chạy:].decode('utf-8','replace').replace('\r\n','\n')
            def gửi(DữLiệu):giáTrịTiếnTrình.stdin.write(DữLiệu);giáTrịTiếnTrình.stdin.flush()
            def vỏLệnh(vănBản):
                vănBản=ipTestText(vănBản)
                print(giáTrịBáoCáo['country'],vănBản,flush=True);giáTrịDãy[0]+=1;hiệnGiáTrị='__SYSTEM_DONE_'+str(giáTrịDãy[0])+'__';chạy=len(bảnGhiNhậtKý)
                gửi((vănBản+'; echo; echo '+hiệnGiáTrị+'\n').encode())
                dấuMốcKếtThúc=('\r\n'+hiệnGiáTrị+'\r\n').encode();nhận(dấuMốcKếtThúc,chạy)
                vịTríKếtThúc=bảnGhiNhậtKý.index(dấuMốcKếtThúc,chạy)+len(dấuMốcKếtThúc)
                nhận(b'jkoros-native> ',vịTríKếtThúc)
                return bảnGhiNhậtKý[chạy:].decode('utf-8','replace').replace('\r\n','\n')
            def xácMinh(vănBản,*cácGiáTrị):
                lờiĐáp=vỏLệnh(vănBản)
                for giáTrị in cácGiáTrị:assert ipTestText(giáTrị) in lờiĐáp,(vănBản,giáTrị,lờiĐáp)
                return lờiĐáp
            try:
                nhận(b'jkoros-native> ')
                if not cácĐốiSố.poweroff_only:
                    giáTrịTrợGiúp=xácMinh('help system','ipconfig','ping','ps','top','df','poweroff')
                    for tênThayThế in giáTrịBíDanh.values():assert tênThayThế in giáTrịTrợGiúp,(tênThayThế,giáTrịTrợGiúp)
                    xácMinh(giáTrịBíDanh['help']+' system','Network / system')
                    xácMinh('ipconfig','inet 10.0.2.15','netmask 255.255.255.0','gateway 10.0.2.2')
                    xácMinh(giáTrịBíDanh['ipconfig'],'inet 10.0.2.15');xácMinh('ip addr show','sl0: UP');xácMinh('ifconfig','sl0: UP')
                    for cácThiếtLậpKhôngHợpLệ in ['999.0.2.15 255.255.255.0 10.0.2.2','10.0.2.20 255.0.255.0 10.0.2.2','10.0.2.20 255.255.255.0 10.1.2.2','10.0.2.0 255.255.255.0 10.0.2.2']:
                        lỗi=xácMinh('ipconfig set '+cácThiếtLậpKhôngHợpLệ+'; echo STATUS=$?','STATUS=');assert 'STATUS=0\n' not in lỗi,lỗi
                        xácMinh('ipconfig','inet 10.0.2.15')
                    xácMinh('ping -c 1 10.0.2.15','1 transmitted, 1 received, 0% packet loss')
                    xácMinh(giáTrịBíDanh['ping']+' -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    xácMinh('ping -c 1 -W 1 10.0.2.254; echo STATUS=$?','1 transmitted, 0 received, 100% packet loss','STATUS=1')
                    xácMinh('ip link set dev sl0 down','sl0: DOWN');xácMinh('ping -c 1 10.0.2.2; echo STATUS=$?','lỗi -100','STATUS=1')
                    xácMinh('ipconfig up','sl0: UP')
                    xácMinh(giáTrịBíDanh['ipconfig']+' set 10.0.2.20 255.255.255.0 10.0.2.2','configuration applied','inet 10.0.2.20')
                    xácMinh('ping -c 2 10.0.2.2','2 transmitted, 2 received, 0% packet loss')
                    xácMinh('ip route show','10.0.2.0 255.255.255.0','10.0.2.2 sl0');xácMinh(giáTrịBíDanh['route'],'10.0.2.2 sl0')
                    xácMinh('ftpd start','FTP listening')
                    xácMinh(giáTrịBíDanh['netstat'],'10.0.2.20:21','LISTEN');xácMinh('ss','LISTEN')
                    xácMinh('ipconfig set 10.0.2.21 255.255.255.0 10.0.2.2','lỗi -16')
                    with ftplib.FTP() as giáTrịMáyKhách:
                        giáTrịMáyKhách.connect('127.0.0.2',sốCổng,timeout=20);giáTrịMáyKhách.login();DữLiệu=b'Network address was changed in the guest.\n'
                        giáTrịMáyKhách.storbinary('STOR net-state.txt',io.BytesIO(DữLiệu));dữLiệuĐãNhận=bytearray();giáTrịMáyKhách.retrbinary('RETR net-state.txt',dữLiệuĐãNhận.extend);assert dữLiệuĐãNhận==DữLiệu;giáTrịMáyKhách.delete('net-state.txt')
                    xácMinh('ftpd stop','FTP stopped');xácMinh('ipconfig set 10.0.2.15 255.255.255.0 10.0.2.2','inet 10.0.2.15')
                    giáTrịBáoCáo['checks'].append('IPv4 validation, real address/link/route changes, ICMP success/timeout, FTP after IP change, socket table')
                    def đãLưu(vănBản):
                        giáTrịĐãTìmThấy=re.search(r'\nramfs (\d+) (\d+) (\d+) (\d+) (\d+)/64 /',vănBản);assert giáTrịĐãTìmThấy,vănBản;return tuple(map(int,giáTrịĐãTìmThấy.groups()))
                    giáTrịTrướcKhi=đãLưu(xácMinh('df','RAM only'));xácMinh('echo disk-proof > sys-state.txt');trạngTháiSau=đãLưu(xácMinh(giáTrịBíDanh['df'],'RAM only'))
                    assert trạngTháiSau[1]-giáTrịTrướcKhi[1]==16384 and trạngTháiSau[4]-giáTrịTrướcKhi[4]==1 and trạngTháiSau[3]-giáTrịTrướcKhi[3]==11,(giáTrịTrướcKhi,trạngTháiSau)
                    xácMinh('rm sys-state.txt');assert đãLưu(vỏLệnh('df'))==giáTrịTrướcKhi
                    BộNhớ=xácMinh(giáTrịBíDanh['free'],'AOT heap KiB total/used/free:','EL0 mapped KiB: 0');giáTrịĐịnhLượng=list(map(int,re.search(r'total/used/free: (\d+)/(\d+)/(\d+)',BộNhớ).groups()));assert 0<giáTrịĐịnhLượng[1]<=giáTrịĐịnhLượng[0] and giáTrịĐịnhLượng[1]+giáTrịĐịnhLượng[2]==giáTrịĐịnhLượng[0]
                    xácMinh(giáTrịBíDanh['ps'],'kernel/shell');xácMinh(giáTrịBíDanh['uptime'],'seconds')
                    thôngTinTìnhTrạng=xácMinh(giáTrịBíDanh['top']+' -n 2','kernel/shell');assert thôngTinTìnhTrạng.count('PID SLOT STATE')==2,thôngTinTìnhTrạng
                    # Park a real EL0 editor in terminal 0, inspect it from terminal 1.
                    xácMinh('terminal','TERMINAL READY');chạy=len(bảnGhiNhậtKý);gửi(b'vi process.txt\n');nhận(b'NORMAL',chạy)
                    chạy=len(bảnGhiNhậtKý);gửi(bytes([30,2,1,0,0,0,0]));nhận(b'jkoros-native> ',chạy)
                    danhSáchMục=xácMinh('ps','SUSPENDED','vi process.txt');giáTrịĐãTìmThấy=re.search(r'\n(\d+) 0 SUSPENDED (\d+) (\d+) (\d+) vi process.txt',danhSáchMục);assert giáTrịĐãTìmThấy and int(giáTrịĐãTìmThấy.group(2))>0,danhSáchMục
                    xácMinh('free','EL0 mapped KiB: '+giáTrịĐãTìmThấy.group(2))
                    chạy=len(bảnGhiNhậtKý);gửi(b'top\n');nhận(b'PID SLOT STATE',chạy);gửi(b'q');nhận(b'jkoros-native> ',chạy)
                    # Test a multibyte prefix through the real shell completion path.
                    if giáTrịBíDanh['df']!='df':
                        chạy=len(bảnGhiNhậtKý);gửi((giáTrịBíDanh['df'][:-1]+'\t\n').encode());nhận(b'RAM only',chạy);nhận(b'jkoros-native> ',chạy)
                    giáTrịBáoCáo['checks'].append('df create/delete counters, real AOT heap, suspended vi PID/memory, top refresh/quit, UTF-8 aliases and Tab')
                with socket.socket(socket.AF_UNIX) as giáTrịĐiềuKhiển:
                    giáTrịĐiềuKhiển.settimeout(15);giáTrịĐiềuKhiển.connect(str(đườngDẫnĐiềuKhiển));giáTrịLuồng=giáTrịĐiềuKhiển.makefile('rwb');json.loads(giáTrịLuồng.readline());giáTrịLuồng.write(b'{"execute":"qmp_capabilities"}\n');giáTrịLuồng.flush()
                    while 'return' not in json.loads(giáTrịLuồng.readline()):pass
                    gửi((('poweroff' if cácĐốiSố.poweroff_only else giáTrịBíDanh['poweroff'])+'\n').encode())
                    while True:
                        sựKiện=json.loads(giáTrịLuồng.readline())
                        if sựKiện.get('event')=='SHUTDOWN':break
                    assert sựKiện['data']['guest'] and sựKiện['data']['reason']=='guest-shutdown',sựKiện
                    assert giáTrịTiếnTrình.wait(timeout=15)==0
                    giáTrịBáoCáo['shutdown']=sựKiện;giáTrịBáoCáo['checks'].append('guest poweroff causes QEMU SHUTDOWN and clean process exit')
                giáTrịBáoCáo['network_trace']=giáTrịCầuNối.nhậtKýDấuVết
                assert cácĐốiSố.poweroff_only or any(giáTrịMục['protocol']==1 and giáTrịMục['direction']=='from_guest' for giáTrịMục in giáTrịCầuNối.nhậtKýDấuVết)
                giáTrịBáoCáo['passed']=True
            finally:
                if giáTrịTiếnTrình.poll() is None:os.killpg(giáTrịTiếnTrình.pid,signal.SIGTERM)
                try:giáTrịTiếnTrình.wait(timeout=10)
                except subprocess.TimeoutExpired:giáTrịTiếnTrình.kill();giáTrịTiếnTrình.wait()
                phầnMụcChọn.close();(ĐầuRa/'serial.log').write_bytes(bảnGhiNhậtKý);(ĐầuRa/'report.json').write_text(json.dumps(giáTrịBáoCáo,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({giáTrịPhím:giáTrị for giáTrịPhím,giáTrị in giáTrịBáoCáo.items() if giáTrịPhím!='network_trace'},ensure_ascii=False),flush=True)


if __name__=='__main__':chạy()
