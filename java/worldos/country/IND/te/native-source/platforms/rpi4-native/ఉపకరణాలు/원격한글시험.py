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
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def నడుపుము():
    ప్రమాణం_డేటా=ప్రొజెక్ట్_మూలం/'build/verification/remmina';ప్రమాణం_డేటా.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];సెలక్టర్=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            వర్చువల్_ప్రదర్శన=shutil.which('Xvfb')
            if వర్చువల్_ప్రదర్శన: సర్వర్_మూల్యం=[వర్చువల్_ప్రదర్శన]
            else:
                뿌리파일계층=ప్రొజెక్ట్_మూలం.parent/'rpi4/build/rootfs'
                సర్వర్_మూల్యం=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def నడుపుము(కారకం_శ్రేణి,환경=None,**이름붙인인수):
                లాగ్_వరుస=(ప్రమాణం_డేటా/('process-%d.log'%len(기록들))).open('wb');기록들.append(లాగ్_వరుస)
                డేటా_స్థాయి=subprocess.Popen(కారకం_శ్రేణి,env=환경,stdout=లాగ్_వరుస,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(డేటా_స్థాయి);return డేటా_స్థాయి
            환경=dict(os.environ)
            for పేరు in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(పేరు,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ప్రదర్శన=నడుపుము(సర్వర్_మూల్యం+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ప్రదర్శన.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            అతిథి=subprocess.Popen(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(అతిథి);సెలక్టర్.register(అతిథి.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ఆఫ్_సెట్_మూల్యం=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ఆఫ్_సెట్_మూల్యం:]:
                    assert అతిథి.poll() is None and time.monotonic()<마감시각,직렬입출력[ఆఫ్_సెట్_మూల్యం:].decode('utf-8','replace')
                    for 누름값,_ in సెలక్టర్.select(.1):
                        డేటా=누름값.fileobj.read(65536)
                        if డేటా:직렬입출력.extend(డేటా)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            పోర్ట్_సంఖ్య=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ప్రొఫైల్=작업경로/'test.remmina'
            ప్రొఫైల్.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%పోర్ట్_సంఖ్య)
            నడుపుము(['dbus-run-session','--','remmina','-c',str(ప్రొఫైల్)],환경=환경,start_new_session=True)
            def 가상입력도구(*కారకం_శ్రేణి):return subprocess.check_output(['xdotool']+list(కారకం_శ్రేణి),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;విండో=None
            while time.monotonic()<마감시각:
                శోధన_ప్రమాణం=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if శోధన_ప్రమాణం.returncode==0:
                    후보=శోధన_ప్రమాణం.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    కేంద్రీకరించబడింది=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if కేంద్రీకరించబడింది.returncode==0:విండో=후보;break
                time.sleep(.1)
            assert విండో,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',విండో,'280','240','click','1')
            time.sleep(1)
            def 글자입력(పాఠ్యము):가상입력도구('type','--clearmodifiers','--delay','50',పాఠ్యము)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ఆఫ్_సెట్_మూల్యం=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 కీ_మూల్యం, Shift+Space 또는 F9'.encode(),ఆఫ్_సెట్_మూల్యం);기다리기(b'jkoros-native> ',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ఆఫ్_సెట్_మూల్యం)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',విండో,str(ప్రమాణం_డేటా/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ఆఫ్_సెట్_మూల్యం)
            # వాస్తవ_డేటా Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            రేఖాచిత్రణ_మూల్యం=Image.open(str(ప్రమాణం_డేటా/'remmina-korean.png')).convert('RGB')
            శీర్షపట్టీ=None
            for నిలువు_స్థాయి in range(రేఖాచిత్రణ_మూల్యం.height):
                가로들=[가로 for 가로 in range(రేఖాచిత్రణ_మూల్యం.width) if రేఖాచిత్రణ_మూల్యం.getpixel((가로,నిలువు_స్థాయి))==(32,80,144)]
                if len(가로들)>=500:శీర్షపట్టీ=(min(가로들),నిలువు_స్థాయి);break
            assert శీర్షపట్టీ,'native terminal title bar not found'
            가로,నిలువు_స్థాయి=శీర్షపట్టీ[0]+564,శీర్షపట్టీ[1]+356
            가상입력도구('mousemove','--window',విండో,str(가로),str(నిలువు_స్థాయి))
            def 화상기다리기(పేరు,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',విండో,str(ప్రమాణం_డేటా/పేరు)])
                    బిట్_మ్యాప్_చిత్రం=Image.open(str(ప్రమాణం_డేటా/పేరు)).convert('RGB')
                    if all(బిట్_మ్యాప్_చిత్రం.getpixel(స్థానము)==빛 for స్థానము,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+పేరు
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,నిలువు_స్థాయి-7),(255,255,255)),((가로+7,నిలువు_స్థాయి+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',విండో,str(가로-120),str(నిలువు_స్థాయి-80),'mouseup','1')
            time.sleep(.4)
            ఆఫ్_సెట్_మూల్యం=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ఆఫ్_సెట్_మూల్యం)
            가상입력도구('mousemove','--window',విండో,'500','45')
            화상기다리기('remmina-resized.png',[
                ((శీర్షపట్టీ[0]+447,శీర్షపట్టీ[1]+279),(39,49,64)),((가로,నిలువు_స్థాయి),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            నిర్ధారణ_నివేదిక.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not నిర్ధారణ_నివేదిక['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ప్రమాణం_డేటా/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for డేటా_స్థాయి in reversed(실행과정들):
                if డేటా_స్థాయి.poll() is None:
                    if డేటా_స్థాయి.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(డేటా_స్థాయి.pid,signal.SIGTERM)
                    else:డేటా_స్థాయి.terminate()
                    try:డేటా_స్థాయి.wait(timeout=5)
                    except subprocess.TimeoutExpired:డేటా_స్థాయి.kill();డేటా_స్థాయి.wait()
            సెలక్టర్.close()
            for ఫైలు_ప్రవేశం in 기록들:ఫైలు_ప్రవేశం.close()
            (ప్రమాణం_డేటా/'serial.log').write_bytes(직렬입출력)
            (ప్రమాణం_డేటా/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':నడుపుము()
