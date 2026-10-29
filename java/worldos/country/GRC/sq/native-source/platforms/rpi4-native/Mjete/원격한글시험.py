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
from zbatoj_komandë import Project_rrënjë


def Ekzekuto():
    llogaritje_të_dhëna=Project_rrënjë/'build/verification/remmina';llogaritje_të_dhëna.mkdir(parents=True,exist_ok=True)
    miratim_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];përzgjedhësi=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtual_afishim=shutil.which('Xvfb')
            if virtual_afishim: server_VALUE=[virtual_afishim]
            else:
                뿌리파일계층=Project_rrënjë.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Ekzekuto(argument_ARRAY,환경=None,**이름붙인인수):
                LOG_RECORD=(llogaritje_të_dhëna/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                të_dhëna_pozicioni=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(të_dhëna_pozicioni);return të_dhëna_pozicioni
            환경=dict(os.environ)
            for Emër in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Emër,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(njësi_COUNT for njësi_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(njësi_COUNT)).exists() and not Path('/tmp/.X%d-lock'%njësi_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            afishim=Ekzekuto(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert afishim.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            i_ftuar=subprocess.Popen(['python3',str(Project_rrënjë/'Mjete/zbatoj_komandë.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(i_ftuar);përzgjedhësi.register(i_ftuar.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert i_ftuar.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in përzgjedhësi.select(.1):
                        të_dhëna=누름값.fileobj.read(65536)
                        if të_dhëna:직렬입출력.extend(të_dhëna)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            numri_i_portës=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            profil=작업경로/'test.remmina'
            profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%numri_i_portës)
            Ekzekuto(['dbus-run-session','--','remmina','-c',str(profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;Dritare=None
            while time.monotonic()<마감시각:
                Kërkim_llogaritje=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Kërkim_llogaritje.returncode==0:
                    후보=Kërkim_llogaritje.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    I_E_fokusuar=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if I_E_fokusuar.returncode==0:Dritare=후보;break
                time.sleep(.1)
            assert Dritare,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Dritare,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Teksti):가상입력도구('type','--clearmodifiers','--delay','50',Teksti)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 tast_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Dritare,str(llogaritje_të_dhëna/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # aktual_të_dhëna Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            vizatim_VALUE=Image.open(str(llogaritje_të_dhëna/'remmina-korean.png')).convert('RGB')
            shiriti_i_titullit=None
            for Vertikal_pozicioni in range(vizatim_VALUE.height):
                가로들=[가로 for 가로 in range(vizatim_VALUE.width) if vizatim_VALUE.getpixel((가로,Vertikal_pozicioni))==(32,80,144)]
                if len(가로들)>=500:shiriti_i_titullit=(min(가로들),Vertikal_pozicioni);break
            assert shiriti_i_titullit,'native terminal title bar not found'
            가로,Vertikal_pozicioni=shiriti_i_titullit[0]+564,shiriti_i_titullit[1]+356
            가상입력도구('mousemove','--window',Dritare,str(가로),str(Vertikal_pozicioni))
            def 화상기다리기(Emër,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Dritare,str(llogaritje_të_dhëna/Emër)])
                    bitmap_IMAGE=Image.open(str(llogaritje_të_dhëna/Emër)).convert('RGB')
                    if all(bitmap_IMAGE.getpixel(Pozicioni)==빛 for Pozicioni,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Emër
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertikal_pozicioni-7),(255,255,255)),((가로+7,Vertikal_pozicioni+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Dritare,str(가로-120),str(Vertikal_pozicioni-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',Dritare,'500','45')
            화상기다리기('remmina-resized.png',[
                ((shiriti_i_titullit[0]+447,shiriti_i_titullit[1]+279),(39,49,64)),((가로,Vertikal_pozicioni),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            miratim_raport.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not miratim_raport['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(llogaritje_të_dhëna/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for të_dhëna_pozicioni in reversed(실행과정들):
                if të_dhëna_pozicioni.poll() is None:
                    if të_dhëna_pozicioni.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(të_dhëna_pozicioni.pid,signal.SIGTERM)
                    else:të_dhëna_pozicioni.terminate()
                    try:të_dhëna_pozicioni.wait(timeout=5)
                    except subprocess.TimeoutExpired:të_dhëna_pozicioni.kill();të_dhëna_pozicioni.wait()
            përzgjedhësi.close()
            for skedar_futje in 기록들:skedar_futje.close()
            (llogaritje_të_dhëna/'serial.log').write_bytes(직렬입출력)
            (llogaritje_të_dhëna/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Ekzekuto()
