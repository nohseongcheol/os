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
from Täida_käsk import Project_juur


def Käivita_2():
    näitaja_andmed=Project_juur/'build/verification/remmina';näitaja_andmed.mkdir(parents=True,exist_ok=True)
    kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];valija=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: server_VALUE=[가상표시장치]
            else:
                뿌리파일계층=Project_juur.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Käivita_2(argument_ARRAY,환경=None,**nimeline_argument):
                LOG_kirje=(näitaja_andmed/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_kirje)
                andmed_ametikoht=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_kirje,stderr=subprocess.STDOUT,**nimeline_argument)
                실행과정들.append(andmed_ametikoht);return andmed_ametikoht
            환경=dict(os.environ)
            for Nimi_2 in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Nimi_2,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(kaup_COUNT for kaup_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(kaup_COUNT)).exists() and not Path('/tmp/.X%d-lock'%kaup_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            ekraan=Käivita_2(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            tähtaeg_Aeg=time.monotonic()+30
            while True:
                assert ekraan.poll() is None and time.monotonic()<tähtaeg_Aeg,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            külaline=subprocess.Popen(['python3',str(Project_juur/'Tööriistad/Täida_käsk.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(külaline);valija.register(külaline.stdout,selectors.EVENT_READ)
            def 기다리기(marker,nihe_VALUE=0):
                tähtaeg_Aeg=time.monotonic()+45
                while marker not in 직렬입출력[nihe_VALUE:]:
                    assert külaline.poll() is None and time.monotonic()<tähtaeg_Aeg,직렬입출력[nihe_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in valija.select(.1):
                        andmed=누름값.fileobj.read(65536)
                        if andmed:직렬입출력.extend(andmed)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            pordinumber=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profiil=작업경로/'test.remmina'
            Profiil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%pordinumber)
            Käivita_2(['dbus-run-session','--','remmina','-c',str(Profiil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            tähtaeg_Aeg=time.monotonic()+60;aken=None
            while time.monotonic()<tähtaeg_Aeg:
                Otsi_näitaja=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Otsi_näitaja.returncode==0:
                    후보=Otsi_näitaja.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Fookuses=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Fookuses.returncode==0:aken=후보;break
                time.sleep(.1)
            assert aken,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',aken,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekst):가상입력도구('type','--clearmodifiers','--delay','50',Tekst)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            nihe_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),nihe_VALUE)
            nihe_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),nihe_VALUE)
            nihe_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/null_operand Võti_VALUE, Shift+Space 또는 F9'.encode(),nihe_VALUE);기다리기(b'jkoros-native> ',nihe_VALUE)
            nihe_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),nihe_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',aken,str(näitaja_andmed/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',nihe_VALUE)
            # tegelik_andmed Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            joonis_VALUE=Image.open(str(näitaja_andmed/'remmina-korean.png')).convert('RGB')
            tiitelriba=None
            for vertikaal_ametikoht in range(joonis_VALUE.height):
                가로들=[가로 for 가로 in range(joonis_VALUE.width) if joonis_VALUE.getpixel((가로,vertikaal_ametikoht))==(32,80,144)]
                if len(가로들)>=500:tiitelriba=(min(가로들),vertikaal_ametikoht);break
            assert tiitelriba,'native terminal title bar not found'
            가로,vertikaal_ametikoht=tiitelriba[0]+564,tiitelriba[1]+356
            가상입력도구('mousemove','--window',aken,str(가로),str(vertikaal_ametikoht))
            def 화상기다리기(Nimi_2,점들):
                tähtaeg_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',aken,str(näitaja_andmed/Nimi_2)])
                    bittraster_pilt=Image.open(str(näitaja_andmed/Nimi_2)).convert('RGB')
                    if all(bittraster_pilt.getpixel(Asukoht)==빛 for Asukoht,빛 in 점들):return
                    assert time.monotonic()<tähtaeg_VALUE,'Remmina framebuffer did not settle: '+Nimi_2
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,vertikaal_ametikoht-7),(255,255,255)),((가로+7,vertikaal_ametikoht+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',aken,str(가로-120),str(vertikaal_ametikoht-80),'mouseup','1')
            time.sleep(.4)
            nihe_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',nihe_VALUE)
            가상입력도구('mousemove','--window',aken,'500','45')
            화상기다리기('remmina-resized.png',[
                ((tiitelriba[0]+447,tiitelriba[1]+279),(39,49,64)),((가로,vertikaal_ametikoht),(24,32,48))])
            if shutil.which('dpkg-query'):
                versiooninumber=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versiooninumber=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            kinnitamine_aruanne.update(passed=True,display=환경['DISPLAY'],remmina_version=versiooninumber,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not kinnitamine_aruanne['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(näitaja_andmed/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for andmed_ametikoht in reversed(실행과정들):
                if andmed_ametikoht.poll() is None:
                    if andmed_ametikoht.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(andmed_ametikoht.pid,signal.SIGTERM)
                    else:andmed_ametikoht.terminate()
                    try:andmed_ametikoht.wait(timeout=5)
                    except subprocess.TimeoutExpired:andmed_ametikoht.kill();andmed_ametikoht.wait()
            valija.close()
            for Fail_kirje in 기록들:Fail_kirje.close()
            (näitaja_andmed/'serial.log').write_bytes(직렬입출력)
            (näitaja_andmed/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Käivita_2()
