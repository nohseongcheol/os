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
from Vykdyti_komanda import Project_šaknis


def Paleisti():
    KR_duomenys=Project_šaknis/'build/verification/remmina';KR_duomenys.mkdir(parents=True,exist_ok=True)
    tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];išrinkiklis=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            가상표시장치=shutil.which('Xvfb')
            if 가상표시장치: serveris_VALUE=[가상표시장치]
            else:
                뿌리파일계층=Project_šaknis.parent/'rpi4/build/rootfs'
                serveris_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Paleisti(argumentas_ARRAY,환경=None,**įvardytasis_argumentas):
                LOG_RECORD=(KR_duomenys/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                duomenys_padėtis=subprocess.Popen(argumentas_ARRAY,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**įvardytasis_argumentas)
                실행과정들.append(duomenys_padėtis);return duomenys_padėtis
            환경=dict(os.environ)
            for Pavadinimas_2 in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Pavadinimas_2,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(prekė_COUNT for prekė_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(prekė_COUNT)).exists() and not Path('/tmp/.X%d-lock'%prekė_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            ekranas=Paleisti(serveris_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            terminas_TIME=time.monotonic()+30
            while True:
                assert ekranas.poll() is None and time.monotonic()<terminas_TIME,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            svečias=subprocess.Popen(['python3',str(Project_šaknis/'Įrankiai/Vykdyti_komanda.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(svečias);išrinkiklis.register(svečias.stdout,selectors.EVENT_READ)
            def 기다리기(žymeklis,OFFSET_VALUE=0):
                terminas_TIME=time.monotonic()+45
                while žymeklis not in 직렬입출력[OFFSET_VALUE:]:
                    assert svečias.poll() is None and time.monotonic()<terminas_TIME,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in išrinkiklis.select(.1):
                        duomenys=누름값.fileobj.read(65536)
                        if duomenys:직렬입출력.extend(duomenys)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            prievado_numeris=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profilis=작업경로/'test.remmina'
            Profilis.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%prievado_numeris)
            Paleisti(['dbus-run-session','--','remmina','-c',str(Profilis)],환경=환경,start_new_session=True)
            def 가상입력도구(*argumentas_ARRAY):return subprocess.check_output(['xdotool']+list(argumentas_ARRAY),env=환경,stderr=subprocess.STDOUT)
            terminas_TIME=time.monotonic()+60;Langas=None
            while time.monotonic()<terminas_TIME:
                Ieška_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Ieška_KR.returncode==0:
                    후보=Ieška_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Reikšmingiausi=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Reikšmingiausi.returncode==0:Langas=후보;break
                time.sleep(.1)
            assert Langas,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Langas,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Tekstas):가상입력도구('type','--clearmodifiers','--delay','50',Tekstas)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/nulis_operandas Raktas_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Langas,str(KR_duomenys/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # faktinis_duomenys Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            piešinys_VALUE=Image.open(str(KR_duomenys/'remmina-korean.png')).convert('RGB')
            pavadinimo_juosta=None
            for segmentas_padėtis in range(piešinys_VALUE.height):
                가로들=[가로 for 가로 in range(piešinys_VALUE.width) if piešinys_VALUE.getpixel((가로,segmentas_padėtis))==(32,80,144)]
                if len(가로들)>=500:pavadinimo_juosta=(min(가로들),segmentas_padėtis);break
            assert pavadinimo_juosta,'native terminal title bar not found'
            가로,segmentas_padėtis=pavadinimo_juosta[0]+564,pavadinimo_juosta[1]+356
            가상입력도구('mousemove','--window',Langas,str(가로),str(segmentas_padėtis))
            def 화상기다리기(Pavadinimas_2,점들):
                terminas_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',Langas,str(KR_duomenys/Pavadinimas_2)])
                    rastras_IMAGE=Image.open(str(KR_duomenys/Pavadinimas_2)).convert('RGB')
                    if all(rastras_IMAGE.getpixel(Pozicija)==빛 for Pozicija,빛 in 점들):return
                    assert time.monotonic()<terminas_VALUE,'Remmina framebuffer did not settle: '+Pavadinimas_2
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,segmentas_padėtis-7),(255,255,255)),((가로+7,segmentas_padėtis+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Langas,str(가로-120),str(segmentas_padėtis-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',Langas,'500','45')
            화상기다리기('remmina-resized.png',[
                ((pavadinimo_juosta[0]+447,pavadinimo_juosta[1]+279),(39,49,64)),((가로,segmentas_padėtis),(24,32,48))])
            if shutil.which('dpkg-query'):
                versijos_numeris=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versijos_numeris=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            tikrinimas_pranešti.update(passed=True,display=환경['DISPLAY'],remmina_version=versijos_numeris,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not tikrinimas_pranešti['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(KR_duomenys/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for duomenys_padėtis in reversed(실행과정들):
                if duomenys_padėtis.poll() is None:
                    if duomenys_padėtis.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(duomenys_padėtis.pid,signal.SIGTERM)
                    else:duomenys_padėtis.terminate()
                    try:duomenys_padėtis.wait(timeout=5)
                    except subprocess.TimeoutExpired:duomenys_padėtis.kill();duomenys_padėtis.wait()
            išrinkiklis.close()
            for Failas_įrašas in 기록들:Failas_įrašas.close()
            (KR_duomenys/'serial.log').write_bytes(직렬입출력)
            (KR_duomenys/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Paleisti()
