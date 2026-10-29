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
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def ਚਲਾਓ_2():
    ਮਾਪ_ਸਮੱਗਰੀ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/remmina';ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True,exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ਚੋਣਕਰਤਾ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ਵਰਚੁਅਲ_ਪ੍ਰਦਰਸ਼ਨ=shutil.which('Xvfb')
            if ਵਰਚੁਅਲ_ਪ੍ਰਦਰਸ਼ਨ: ਸਰਵਰ_ਕੀਮਤ=[ਵਰਚੁਅਲ_ਪ੍ਰਦਰਸ਼ਨ]
            else:
                뿌리파일계층=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parent/'rpi4/build/rootfs'
                ਸਰਵਰ_ਕੀਮਤ=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ਚਲਾਓ_2(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ,환경=None,**이름붙인인수):
                ਲੌਗ_ਕਤਾਰ=(ਮਾਪ_ਸਮੱਗਰੀ/('process-%d.log'%len(기록들))).open('wb');기록들.append(ਲੌਗ_ਕਤਾਰ)
                ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=subprocess.Popen(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ,env=환경,stdout=ਲੌਗ_ਕਤਾਰ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ);return ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ
            환경=dict(os.environ)
            for ਨਾਂ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ਨਾਂ,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ਪ੍ਰਦਰਸ਼ਨ=ਚਲਾਓ_2(ਸਰਵਰ_ਕੀਮਤ+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ਪ੍ਰਦਰਸ਼ਨ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ਗੈਸਟ=subprocess.Popen(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ਗੈਸਟ);ਚੋਣਕਰਤਾ.register(ਗੈਸਟ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ਔਫਸੈਟ_ਕੀਮਤ=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ਔਫਸੈਟ_ਕੀਮਤ:]:
                    assert ਗੈਸਟ.poll() is None and time.monotonic()<마감시각,직렬입출력[ਔਫਸੈਟ_ਕੀਮਤ:].decode('utf-8','replace')
                    for 누름값,_ in ਚੋਣਕਰਤਾ.select(.1):
                        ਸਮੱਗਰੀ=누름값.fileobj.read(65536)
                        if ਸਮੱਗਰੀ:직렬입출력.extend(ਸਮੱਗਰੀ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ਪ੍ਰੋਫਾਈਲ=작업경로/'test.remmina'
            ਪ੍ਰੋਫਾਈਲ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            ਚਲਾਓ_2(['dbus-run-session','--','remmina','-c',str(ਪ੍ਰੋਫਾਈਲ)],환경=환경,start_new_session=True)
            def 가상입력도구(*ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ):return subprocess.check_output(['xdotool']+list(ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ਵਿੰਡੋ=None
            while time.monotonic()<마감시각:
                ਖੋਜ_ਮਾਪ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ਖੋਜ_ਮਾਪ.returncode==0:
                    후보=ਖੋਜ_ਮਾਪ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ਫੋਕਸ_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ਫੋਕਸ_f7e69dab.returncode==0:ਵਿੰਡੋ=후보;break
                time.sleep(.1)
            assert ਵਿੰਡੋ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ਵਿੰਡੋ,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ਟੈਕਸਟ):가상입력도구('type','--clearmodifiers','--delay','50',ਟੈਕਸਟ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ਔਫਸੈਟ_ਕੀਮਤ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ਕੀ_ਕੀਮਤ, Shift+Space 또는 F9'.encode(),ਔਫਸੈਟ_ਕੀਮਤ);기다리기(b'jkoros-native> ',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ਵਿੰਡੋ,str(ਮਾਪ_ਸਮੱਗਰੀ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ਔਫਸੈਟ_ਕੀਮਤ)
            # ਅਸਲ_ਸਮੱਗਰੀ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ=Image.open(str(ਮਾਪ_ਸਮੱਗਰੀ/'remmina-korean.png')).convert('RGB')
            ਸਿਰਲੇਖ_ਪੱਟੀ=None
            for ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ in range(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.height):
                가로들=[가로 for 가로 in range(ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.width) if ਚਿੱਤਰ_ਬਨਾਉਣਾ_ਕੀਮਤ.getpixel((가로,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))==(32,80,144)]
                if len(가로들)>=500:ਸਿਰਲੇਖ_ਪੱਟੀ=(min(가로들),ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ);break
            assert ਸਿਰਲੇਖ_ਪੱਟੀ,'native terminal title bar not found'
            가로,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ=ਸਿਰਲੇਖ_ਪੱਟੀ[0]+564,ਸਿਰਲੇਖ_ਪੱਟੀ[1]+356
            가상입력도구('mousemove','--window',ਵਿੰਡੋ,str(가로),str(ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))
            def 화상기다리기(ਨਾਂ,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ਵਿੰਡੋ,str(ਮਾਪ_ਸਮੱਗਰੀ/ਨਾਂ)])
                    ਬਿਟਮੈਪ_ਤਸਵੀਰ=Image.open(str(ਮਾਪ_ਸਮੱਗਰੀ/ਨਾਂ)).convert('RGB')
                    if all(ਬਿਟਮੈਪ_ਤਸਵੀਰ.getpixel(ਸਥਿਤੀ)==빛 for ਸਥਿਤੀ,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ਨਾਂ
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ-7),(255,255,255)),((가로+7,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ਵਿੰਡੋ,str(가로-120),str(ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ-80),'mouseup','1')
            time.sleep(.4)
            ਔਫਸੈਟ_ਕੀਮਤ=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ਔਫਸੈਟ_ਕੀਮਤ)
            가상입력도구('mousemove','--window',ਵਿੰਡੋ,'500','45')
            화상기다리기('remmina-resized.png',[
                ((ਸਿਰਲੇਖ_ਪੱਟੀ[0]+447,ਸਿਰਲੇਖ_ਪੱਟੀ[1]+279),(39,49,64)),((가로,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ਮਾਨਤਾ_ਵਿਵਰਨ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ਮਾਪ_ਸਮੱਗਰੀ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ in reversed(실행과정들):
                if ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.poll() is None:
                    if ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.pid,signal.SIGTERM)
                    else:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.terminate()
                    try:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.kill();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.wait()
            ਚੋਣਕਰਤਾ.close()
            for ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ in 기록들:ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.close()
            (ਮਾਪ_ਸਮੱਗਰੀ/'serial.log').write_bytes(직렬입출력)
            (ਮਾਪ_ਸਮੱਗਰੀ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ਚਲਾਓ_2()
