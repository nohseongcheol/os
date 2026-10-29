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
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಡೇಟಾ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/remmina';ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True,exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ಸೆಲೆಕ್ಟರ್=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ಅಗೋಚರ_ಪ್ರದರ್ಶನ=shutil.which('Xvfb')
            if ಅಗೋಚರ_ಪ್ರದರ್ಶನ: ಸರ್ವರ್_ಮೌಲ್ಯ=[ಅಗೋಚರ_ಪ್ರದರ್ಶನ]
            else:
                뿌리파일계층=ಬಿಂಬಿಸು_ಮೂಲ.parent/'rpi4/build/rootfs'
                ಸರ್ವರ್_ಮೌಲ್ಯ=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ಚಲಾಯಿಸು_2(ವಾದ_ಅರೇ,환경=None,**이름붙인인수):
                ಲಾಗ್_ದಾಖಲೆ=(ಮಾಪನ_ಡೇಟಾ/('process-%d.log'%len(기록들))).open('wb');기록들.append(ಲಾಗ್_ದಾಖಲೆ)
                ಡೇಟಾ_ಹುದ್ದೆ=subprocess.Popen(ವಾದ_ಅರೇ,env=환경,stdout=ಲಾಗ್_ದಾಖಲೆ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ಡೇಟಾ_ಹುದ್ದೆ);return ಡೇಟಾ_ಹುದ್ದೆ
            환경=dict(os.environ)
            for ಹೆಸರು in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ಹೆಸರು,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ಪ್ರದರ್ಶನ=ಚಲಾಯಿಸು_2(ಸರ್ವರ್_ಮೌಲ್ಯ+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ಪ್ರದರ್ಶನ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ಅತಿಥಿ=subprocess.Popen(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ಅತಿಥಿ);ಸೆಲೆಕ್ಟರ್.register(ಅತಿಥಿ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:]:
                    assert ಅತಿಥಿ.poll() is None and time.monotonic()<마감시각,직렬입출력[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:].decode('utf-8','replace')
                    for 누름값,_ in ಸೆಲೆಕ್ಟರ್.select(.1):
                        ಡೇಟಾ=누름값.fileobj.read(65536)
                        if ಡೇಟಾ:직렬입출력.extend(ಡೇಟಾ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ಪ್ರೊಫೈಲ್=작업경로/'test.remmina'
            ಪ್ರೊಫೈಲ್.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%ಪೋರ್ಟ್_ಸಂಖ್ಯೆ)
            ಚಲಾಯಿಸು_2(['dbus-run-session','--','remmina','-c',str(ಪ್ರೊಫೈಲ್)],환경=환경,start_new_session=True)
            def 가상입력도구(*ವಾದ_ಅರೇ):return subprocess.check_output(['xdotool']+list(ವಾದ_ಅರೇ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ವಿಂಡೋ=None
            while time.monotonic()<마감시각:
                ಶೋಧ_ಮಾಪನ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ಶೋಧ_ಮಾಪನ.returncode==0:
                    후보=ಶೋಧ_ಮಾಪನ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ಕೇಂದ್ರೀಕೃತ=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ಕೇಂದ್ರೀಕೃತ.returncode==0:ವಿಂಡೋ=후보;break
                time.sleep(.1)
            assert ವಿಂಡೋ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ವಿಂಡೋ,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ಪಠ್ಯ):가상입력도구('type','--clearmodifiers','--delay','50',ಪಠ್ಯ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ಕೀ_ಮೌಲ್ಯ, Shift+Space 또는 F9'.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ);기다리기(b'jkoros-native> ',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ವಿಂಡೋ,str(ಮಾಪನ_ಡೇಟಾ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            # ನಿಜವಾದ_ಡೇಟಾ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ=Image.open(str(ಮಾಪನ_ಡೇಟಾ/'remmina-korean.png')).convert('RGB')
            ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ=None
            for ಲಂಬ_ಹುದ್ದೆ in range(ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.height):
                가로들=[가로 for 가로 in range(ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.width) if ಚಿತ್ರರಚನೆ_ಮೌಲ್ಯ.getpixel((가로,ಲಂಬ_ಹುದ್ದೆ))==(32,80,144)]
                if len(가로들)>=500:ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ=(min(가로들),ಲಂಬ_ಹುದ್ದೆ);break
            assert ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ,'native terminal title bar not found'
            가로,ಲಂಬ_ಹುದ್ದೆ=ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ[0]+564,ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ[1]+356
            가상입력도구('mousemove','--window',ವಿಂಡೋ,str(가로),str(ಲಂಬ_ಹುದ್ದೆ))
            def 화상기다리기(ಹೆಸರು,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ವಿಂಡೋ,str(ಮಾಪನ_ಡೇಟಾ/ಹೆಸರು)])
                    ಬಿಟ್_ಮ್ಯಾಪ್_ಇಮೇಜ್=Image.open(str(ಮಾಪನ_ಡೇಟಾ/ಹೆಸರು)).convert('RGB')
                    if all(ಬಿಟ್_ಮ್ಯಾಪ್_ಇಮೇಜ್.getpixel(ಸ್ಥಾನ)==빛 for ಸ್ಥಾನ,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ಹೆಸರು
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ಲಂಬ_ಹುದ್ದೆ-7),(255,255,255)),((가로+7,ಲಂಬ_ಹುದ್ದೆ+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ವಿಂಡೋ,str(가로-120),str(ಲಂಬ_ಹುದ್ದೆ-80),'mouseup','1')
            time.sleep(.4)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            가상입력도구('mousemove','--window',ವಿಂಡೋ,'500','45')
            화상기다리기('remmina-resized.png',[
                ((ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ[0]+447,ಶೀರ್ಷಿಕೆ_ಪಟ್ಟಿ[1]+279),(39,49,64)),((가로,ಲಂಬ_ಹುದ್ದೆ),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ದೃಢೀಕರಣ_ವರದಿ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ದೃಢೀಕರಣ_ವರದಿ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ಮಾಪನ_ಡೇಟಾ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ಡೇಟಾ_ಹುದ್ದೆ in reversed(실행과정들):
                if ಡೇಟಾ_ಹುದ್ದೆ.poll() is None:
                    if ಡೇಟಾ_ಹುದ್ದೆ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ಡೇಟಾ_ಹುದ್ದೆ.pid,signal.SIGTERM)
                    else:ಡೇಟಾ_ಹುದ್ದೆ.terminate()
                    try:ಡೇಟಾ_ಹುದ್ದೆ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ಡೇಟಾ_ಹುದ್ದೆ.kill();ಡೇಟಾ_ಹುದ್ದೆ.wait()
            ಸೆಲೆಕ್ಟರ್.close()
            for ಫೈಲ್_ನಮೂದು in 기록들:ಫೈಲ್_ನಮೂದು.close()
            (ಮಾಪನ_ಡೇಟಾ/'serial.log').write_bytes(직렬입출력)
            (ಮಾಪನ_ಡೇಟಾ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ಚಲಾಯಿಸು_2()
