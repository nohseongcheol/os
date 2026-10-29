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
from eżegwixxa_kmand import pprojetta_għerq


def serje():
    miżura_data=pprojetta_għerq/'build/verification/remmina';miżura_data.mkdir(parents=True,exist_ok=True)
    validazzjoni_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];selettur=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtwali_wera=shutil.which('Xvfb')
            if virtwali_wera: server_VALUE=[virtwali_wera]
            else:
                뿌리파일계층=pprojetta_għerq.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def serje(argument_ARRAY,환경=None,**이름붙인인수):
                LOG_RECORD=(miżura_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_RECORD)
                data_pożizzjoni=subprocess.Popen(argument_ARRAY,env=환경,stdout=LOG_RECORD,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(data_pożizzjoni);return data_pożizzjoni
            환경=dict(os.environ)
            for isem in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(isem,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(element_COUNT for element_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(element_COUNT)).exists() and not Path('/tmp/.X%d-lock'%element_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            displej=serje(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert displej.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            mistieden=subprocess.Popen(['python3',str(pprojetta_għerq/'Għodod/eżegwixxa_kmand.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(mistieden);selettur.register(mistieden.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert mistieden.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in selettur.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            serje(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*argument_ARRAY):return subprocess.check_output(['xdotool']+list(argument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;tieqa=None
            while time.monotonic()<마감시각:
                SEARCH_miżura=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SEARCH_miżura.returncode==0:
                    후보=SEARCH_miżura.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Ffokata=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Ffokata.returncode==0:tieqa=후보;break
                time.sleep(.1)
            assert tieqa,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',tieqa,'280','240','click','1')
            time.sleep(1)
            def 글자입력(SMS):가상입력도구('type','--clearmodifiers','--delay','50',SMS)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 tast_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',tieqa,str(miżura_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # attwali_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            tpinġija_VALUE=Image.open(str(miżura_data/'remmina-korean.png')).convert('RGB')
            strixxa_tat_titlu=None
            for Vertikali_pożizzjoni in range(tpinġija_VALUE.height):
                가로들=[가로 for 가로 in range(tpinġija_VALUE.width) if tpinġija_VALUE.getpixel((가로,Vertikali_pożizzjoni))==(32,80,144)]
                if len(가로들)>=500:strixxa_tat_titlu=(min(가로들),Vertikali_pożizzjoni);break
            assert strixxa_tat_titlu,'native terminal title bar not found'
            가로,Vertikali_pożizzjoni=strixxa_tat_titlu[0]+564,strixxa_tat_titlu[1]+356
            가상입력도구('mousemove','--window',tieqa,str(가로),str(Vertikali_pożizzjoni))
            def 화상기다리기(isem,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',tieqa,str(miżura_data/isem)])
                    bitmap_IMAGE=Image.open(str(miżura_data/isem)).convert('RGB')
                    if all(bitmap_IMAGE.getpixel(pożizzjoni)==빛 for pożizzjoni,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+isem
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertikali_pożizzjoni-7),(255,255,255)),((가로+7,Vertikali_pożizzjoni+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',tieqa,str(가로-120),str(Vertikali_pożizzjoni-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',tieqa,'500','45')
            화상기다리기('remmina-resized.png',[
                ((strixxa_tat_titlu[0]+447,strixxa_tat_titlu[1]+279),(39,49,64)),((가로,Vertikali_pożizzjoni),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validazzjoni_rapport.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validazzjoni_rapport['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(miżura_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_pożizzjoni in reversed(실행과정들):
                if data_pożizzjoni.poll() is None:
                    if data_pożizzjoni.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_pożizzjoni.pid,signal.SIGTERM)
                    else:data_pożizzjoni.terminate()
                    try:data_pożizzjoni.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_pożizzjoni.kill();data_pożizzjoni.wait()
            selettur.close()
            for fajl_entrata in 기록들:fajl_entrata.close()
            (miżura_data/'serial.log').write_bytes(직렬입출력)
            (miżura_data/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':serje()
