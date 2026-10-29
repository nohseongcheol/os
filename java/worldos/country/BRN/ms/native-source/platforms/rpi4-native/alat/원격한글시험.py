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
from laksanakan_perintah import projek_akar


def Jalan():
    ukuran_data=projek_akar/'build/verification/remmina';ukuran_data.mkdir(parents=True,exist_ok=True)
    pensahihan_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];준비선택기=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            maya_papar=shutil.which('Xvfb')
            if maya_papar: pelayan_VALUE=[maya_papar]
            else:
                뿌리파일계층=projek_akar.parent/'rpi4/build/rootfs'
                pelayan_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Jalan(argumen_ARRAY,persekitaran=None,**이름붙인인수):
                LOG_baris=(ukuran_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_baris)
                data_jawatan=subprocess.Popen(argumen_ARRAY,env=persekitaran,stdout=LOG_baris,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(data_jawatan);return data_jawatan
            persekitaran=dict(os.environ)
            for Nama in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):persekitaran.pop(Nama,None)
            persekitaran.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(item_COUNT for item_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(item_COUNT)).exists() and not Path('/tmp/.X%d-lock'%item_COUNT).exists())
            persekitaran['DISPLAY']=':'+str(수치)
            paparan=Jalan(pelayan_VALUE+[persekitaran['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],persekitaran=persekitaran)
            마감시각=time.monotonic()+30
            while True:
                assert paparan.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=persekitaran,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            tetamu=subprocess.Popen(['python3',str(projek_akar/'alat/laksanakan_perintah.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(tetamu);준비선택기.register(tetamu.stdout,selectors.EVENT_READ)
            def 기다리기(penanda,Ofset_VALUE=0):
                마감시각=time.monotonic()+45
                while penanda not in 직렬입출력[Ofset_VALUE:]:
                    assert tetamu.poll() is None and time.monotonic()<마감시각,직렬입출력[Ofset_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in 준비선택기.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            nombor_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%nombor_port)
            Jalan(['dbus-run-session','--','remmina','-c',str(Profil)],persekitaran=persekitaran,start_new_session=True)
            def 가상입력도구(*argumen_ARRAY):return subprocess.check_output(['xdotool']+list(argumen_ARRAY),env=persekitaran,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Tetingkap=None
            while time.monotonic()<마감시각:
                Cari_ukuran=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=persekitaran,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Cari_ukuran.returncode==0:
                    후보=Cari_ukuran.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Tumpuan=subprocess.run(['xdotool','windowfocus','--sync',후보],env=persekitaran,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Tumpuan.returncode==0:Tetingkap=후보;break
                time.sleep(.1)
            assert Tetingkap,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Tetingkap,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Teks):가상입력도구('type','--clearmodifiers','--delay','50',Teks)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            Ofset_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Ofset_VALUE)
            Ofset_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),Ofset_VALUE)
            Ofset_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Kunci_VALUE, Shift+Space 또는 F9'.encode(),Ofset_VALUE);기다리기(b'jkoros-native> ',Ofset_VALUE)
            Ofset_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),Ofset_VALUE)
            subprocess.check_call(['import','-display',persekitaran['DISPLAY'],'-window',Tetingkap,str(ukuran_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',Ofset_VALUE)
            # sebenar_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            lukisan_VALUE=Image.open(str(ukuran_data/'remmina-korean.png')).convert('RGB')
            bar_tajuk=None
            for Menegak_jawatan in range(lukisan_VALUE.height):
                가로들=[가로 for 가로 in range(lukisan_VALUE.width) if lukisan_VALUE.getpixel((가로,Menegak_jawatan))==(32,80,144)]
                if len(가로들)>=500:bar_tajuk=(min(가로들),Menegak_jawatan);break
            assert bar_tajuk,'native terminal title bar not found'
            가로,Menegak_jawatan=bar_tajuk[0]+564,bar_tajuk[1]+356
            가상입력도구('mousemove','--window',Tetingkap,str(가로),str(Menegak_jawatan))
            def 화상기다리기(Nama,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',persekitaran['DISPLAY'],'-window',Tetingkap,str(ukuran_data/Nama)])
                    peta_bit_imej=Image.open(str(ukuran_data/Nama)).convert('RGB')
                    if all(peta_bit_imej.getpixel(Kedudukan)==빛 for Kedudukan,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Nama
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Menegak_jawatan-7),(255,255,255)),((가로+7,Menegak_jawatan+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Tetingkap,str(가로-120),str(Menegak_jawatan-80),'mouseup','1')
            time.sleep(.4)
            Ofset_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',Ofset_VALUE)
            가상입력도구('mousemove','--window',Tetingkap,'500','45')
            화상기다리기('remmina-resized.png',[
                ((bar_tajuk[0]+447,bar_tajuk[1]+279),(39,49,64)),((가로,Menegak_jawatan),(24,32,48))])
            if shutil.which('dpkg-query'):
                nombor_versi=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                nombor_versi=subprocess.check_output(['remmina','--version'],env=persekitaran,stderr=subprocess.STDOUT).decode('utf-8','replace')
            pensahihan_lapor.update(passed=True,display=persekitaran['DISPLAY'],remmina_version=nombor_versi,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not pensahihan_lapor['passed'] and 'persekitaran' in locals() and persekitaran.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',persekitaran['DISPLAY'],'-window','root',str(ukuran_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_jawatan in reversed(실행과정들):
                if data_jawatan.poll() is None:
                    if data_jawatan.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_jawatan.pid,signal.SIGTERM)
                    else:data_jawatan.terminate()
                    try:data_jawatan.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_jawatan.kill();data_jawatan.wait()
            준비선택기.close()
            for fail_pemasukan in 기록들:fail_pemasukan.close()
            (ukuran_data/'serial.log').write_bytes(직렬입출력)
            (ukuran_data/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Jalan()
