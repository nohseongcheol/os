#!/usr/bin/env python3
"""Exercise the installed Remmina in an isolated X display and D-Bus session.

Needs Remmina's VNC plugin, xdotool, Xvfb (or the existing ARM64 Xvfb rootfs
and qemu-aarch64), dbus-run-session, and ImageMagick import. Never uses :0.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from thựcThiLệnh import gốcCâyDựÁn


def chạy():
    dữLiệuKếtQuả=gốcCâyDựÁn/'build/verification/remmina';dữLiệuKếtQuả.mkdir(parents=True,exist_ok=True)
    báoCáoViệcThẩmĐịnh={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as đườngDẫnĐangLàmViệc:
        đườngDẫnĐangLàmViệc=Path(đườngDẫnĐangLàmViệc);cácTiếnTrìnhĐangChạy=[];bộChọn=selectors.DefaultSelector();vàoRaNốiTiếp=bytearray()
        cácBảnGhiNhậtKý=[]
        try:
            hiểnThịẢo=shutil.which('Xvfb')
            if hiểnThịẢo: giáTrịMáyChủ=[hiểnThịẢo]
            else:
                hệTệpGốc=gốcCâyDựÁn.parent/'rpi4/build/rootfs'
                giáTrịMáyChủ=['qemu-aarch64','-L',str(hệTệpGốc),str(hệTệpGốc/'usr/bin/Xvfb')]
            def chạy(mảngĐốiSố,môiTrường=None,**đốiSốĐượcĐặtTên):
                bảnGhiNhậtKý=(dữLiệuKếtQuả/('process-%d.log'%len(cácBảnGhiNhậtKý))).open('wb');cácBảnGhiNhậtKý.append(bảnGhiNhậtKý)
                vịTríDữLiệu=subprocess.Popen(mảngĐốiSố,env=môiTrường,stdout=bảnGhiNhậtKý,stderr=subprocess.STDOUT,**đốiSốĐượcĐặtTên)
                cácTiếnTrìnhĐangChạy.append(vịTríDữLiệu);return vịTríDữLiệu
            môiTrường=dict(os.environ)
            for tên in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):môiTrường.pop(tên,None)
            môiTrường.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(đườngDẫnĐangLàmViệc/'config'),XDG_DATA_HOME=str(đườngDẫnĐangLàmViệc/'data'),XDG_CACHE_HOME=str(đườngDẫnĐangLàmViệc/'cache'))
            giáTrịThuộcSố=next(sốLượngPhầnMục for sốLượngPhầnMục in range(80,200) if not Path('/tmp/.X11-unix/X'+str(sốLượngPhầnMục)).exists() and not Path('/tmp/.X%d-lock'%sốLượngPhầnMục).exists())
            môiTrường['DISPLAY']=':'+str(giáTrịThuộcSố)
            thiếtBịHiểnThị=chạy(giáTrịMáyChủ+[môiTrường['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],môiTrường=môiTrường)
            thờiGianHạnChót=time.monotonic()+30
            while True:
                assert thiếtBịHiểnThị.poll() is None and time.monotonic()<thờiGianHạnChót,'Xvfb failed; see process-0.log'
                đầyĐủSựChuẩnBị=subprocess.run(['xdotool','getdisplaygeometry'],env=môiTrường,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if đầyĐủSựChuẩnBị.returncode==0:break
                time.sleep(.1)
            khách=subprocess.Popen(['python3',str(gốcCâyDựÁn/'CôngCụ/thựcThiLệnh.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            cácTiếnTrìnhĐangChạy.append(khách);bộChọn.register(khách.stdout,selectors.EVENT_READ)
            def đợi(dấuMốc,giáTrịĐộLệch=0):
                thờiGianHạnChót=time.monotonic()+45
                while dấuMốc not in vàoRaNốiTiếp[giáTrịĐộLệch:]:
                    assert khách.poll() is None and time.monotonic()<thờiGianHạnChót,vàoRaNốiTiếp[giáTrịĐộLệch:].decode('utf-8','replace')
                    for giáTrịĐãNhấn,_ in bộChọn.select(.1):
                        DữLiệu=giáTrịĐãNhấn.fileobj.read(65536)
                        if DữLiệu:vàoRaNốiTiếp.extend(DữLiệu)
            đợi(b'TERMINAL READY');đợi(b'jkoros-native> ',vàoRaNốiTiếp.rfind(b'TERMINAL READY'))
            sốCổng=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',vàoRaNốiTiếp).group(1))
            hồSơ=đườngDẫnĐangLàmViệc/'test.remmina'
            hồSơ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%sốCổng)
            chạy(['dbus-run-session','--','remmina','-c',str(hồSơ)],môiTrường=môiTrường,start_new_session=True)
            def côngCụĐầuVàoẢo(*mảngĐốiSố):return subprocess.check_output(['xdotool']+list(mảngĐốiSố),env=môiTrường,stderr=subprocess.STDOUT)
            thờiGianHạnChót=time.monotonic()+60;cửaSổ=None
            while time.monotonic()<thờiGianHạnChót:
                tìmKiếmKếtQuả=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=môiTrường,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if tìmKiếmKếtQuả.returncode==0:
                    ứngViên=tìmKiếmKếtQuả.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    cóTiêuĐiểm=subprocess.run(['xdotool','windowfocus','--sync',ứngViên],env=môiTrường,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if cóTiêuĐiểm.returncode==0:cửaSổ=ứngViên;break
                time.sleep(.1)
            assert cửaSổ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            côngCụĐầuVàoẢo('mousemove','--window',cửaSổ,'280','240','click','1')
            time.sleep(1)
            def kýTựCóKiểu(vănBản):côngCụĐầuVàoẢo('type','--clearmodifiers','--delay','50',vănBản)
            def giáTrịĐãNhấn(*cácPhímĐãNhấn):côngCụĐầuVàoẢo('key','--clearmodifiers',*cácPhímĐãNhấn)
            giáTrịĐộLệch=len(vàoRaNốiTiếp);kýTựCóKiểu('echo ');giáTrịĐãNhấn('F9');kýTựCóKiểu('dkssudgktpdy gksrmf');giáTrịĐãNhấn('F9','Return')
            đợi('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),giáTrịĐộLệch)
            giáTrịĐộLệch=len(vàoRaNốiTiếp);kýTựCóKiểu('echo ');giáTrịĐãNhấn('shift+space');kýTựCóKiểu('rhk rkqtk');giáTrịĐãNhấn('shift+space','Return')
            đợi('\r\n과 갑사\r\njkoros-native> '.encode(),giáTrịĐộLệch)
            giáTrịĐộLệch=len(vàoRaNốiTiếp);kýTựCóKiểu('help ko');giáTrịĐãNhấn('Return')
            đợi('한/toánHạngKhôngSố giáTrịPhím, Shift+Space 또는 F9'.encode(),giáTrịĐộLệch);đợi(b'jkoros-native> ',giáTrịĐộLệch)
            giáTrịĐộLệch=len(vàoRaNốiTiếp);kýTựCóKiểu('echo ');giáTrịĐãNhấn('F9');kýTựCóKiểu('gksrmf dlfr')
            đợi('읽'.encode(),giáTrịĐộLệch)
            subprocess.check_call(['import','-display',môiTrường['DISPLAY'],'-window',cửaSổ,str(dữLiệuKếtQuả/'remmina-korean.png')])
            giáTrịĐãNhấn('F9','Return')
            đợi(b'jkoros-native> ',giáTrịĐộLệch)
            # dữLiệuThựcTế Remmina의 MànHình 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            HìnhVẽ=Image.open(str(dữLiệuKếtQuả/'remmina-korean.png')).convert('RGB')
            thanhTiêuĐề=None
            for vịTríDọc in range(HìnhVẽ.height):
                cácVịTríNgang=[vịTríNgang for vịTríNgang in range(HìnhVẽ.width) if HìnhVẽ.getpixel((vịTríNgang,vịTríDọc))==(32,80,144)]
                if len(cácVịTríNgang)>=500:thanhTiêuĐề=(min(cácVịTríNgang),vịTríDọc);break
            assert thanhTiêuĐề,'native terminal title bar not found'
            vịTríNgang,vịTríDọc=thanhTiêuĐề[0]+564,thanhTiêuĐề[1]+356
            côngCụĐầuVàoẢo('mousemove','--window',cửaSổ,str(vịTríNgang),str(vịTríDọc))
            def chờBảnĐồBitCho(tên,danhSáchCácĐiểm):
                giáTrịHạnChót=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',môiTrường['DISPLAY'],'-window',cửaSổ,str(dữLiệuKếtQuả/tên)])
                    ảnhBảnĐồBit=Image.open(str(dữLiệuKếtQuả/tên)).convert('RGB')
                    if all(ảnhBảnĐồBit.getpixel(vịTrí)==Màu for vịTrí,Màu in danhSáchCácĐiểm):return
                    assert time.monotonic()<giáTrịHạnChót,'Remmina framebuffer did not settle: '+tên
                    time.sleep(.1)
            chờBảnĐồBitCho('remmina-resize-cursor.png',[
                ((vịTríNgang-7,vịTríDọc-7),(255,255,255)),((vịTríNgang+7,vịTríDọc+7),(255,255,255))])
            côngCụĐầuVàoẢo('mousedown','1','mousemove','--window',cửaSổ,str(vịTríNgang-120),str(vịTríDọc-80),'mouseup','1')
            time.sleep(.4)
            giáTrịĐộLệch=len(vàoRaNốiTiếp);kýTựCóKiểu('terminal size');giáTrịĐãNhấn('Return')
            đợi(b'TERMINAL SIZE 53x14\r\n',giáTrịĐộLệch)
            côngCụĐầuVàoẢo('mousemove','--window',cửaSổ,'500','45')
            chờBảnĐồBitCho('remmina-resized.png',[
                ((thanhTiêuĐề[0]+447,thanhTiêuĐề[1]+279),(39,49,64)),((vịTríNgang,vịTríDọc),(24,32,48))])
            if shutil.which('dpkg-query'):
                sốPhiênBản=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                sốPhiênBản=subprocess.check_output(['remmina','--version'],env=môiTrường,stderr=subprocess.STDOUT).decode('utf-8','replace')
            báoCáoViệcThẩmĐịnh.update(passed=True,display=môiTrường['DISPLAY'],remmina_version=sốPhiênBản,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not báoCáoViệcThẩmĐịnh['passed'] and 'môiTrường' in locals() and môiTrường.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',môiTrường['DISPLAY'],'-window','root',str(dữLiệuKếtQuả/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for vịTríDữLiệu in reversed(cácTiếnTrìnhĐangChạy):
                if vịTríDữLiệu.poll() is None:
                    if vịTríDữLiệu.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(vịTríDữLiệu.pid,signal.SIGTERM)
                    else:vịTríDữLiệu.terminate()
                    try:vịTríDữLiệu.wait(timeout=5)
                    except subprocess.TimeoutExpired:vịTríDữLiệu.kill();vịTríDữLiệu.wait()
            bộChọn.close()
            for mụcTệp in cácBảnGhiNhậtKý:mụcTệp.close()
            (dữLiệuKếtQuả/'serial.log').write_bytes(vàoRaNốiTiếp)
            (dữLiệuKếtQuả/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':chạy()
