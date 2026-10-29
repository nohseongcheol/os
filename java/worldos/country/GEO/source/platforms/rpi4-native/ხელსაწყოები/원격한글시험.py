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
from შესრულება_ბრძანება import პროეცირება_ფესვი


def გაშვება():
    გაზომვა_მონაცემები=პროეცირება_ფესვი/'build/verification/remmina';გაზომვა_მონაცემები.mkdir(parents=True,exist_ok=True)
    გადამოწმება_ანგარიში={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];სელექტორი=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ვირტუალური_ჩვენება=shutil.which('Xvfb')
            if ვირტუალური_ჩვენება: სერვერი_მნიშვნელობა=[ვირტუალური_ჩვენება]
            else:
                뿌리파일계층=პროეცირება_ფესვი.parent/'rpi4/build/rootfs'
                სერვერი_მნიშვნელობა=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def გაშვება(არგუმენტი_მასივი,환경=None,**이름붙인인수):
                ჟურნალი_ჩაწერა=(გაზომვა_მონაცემები/('process-%d.log'%len(기록들))).open('wb');기록들.append(ჟურნალი_ჩაწერა)
                მონაცემები_პოზიცია=subprocess.Popen(არგუმენტი_მასივი,env=환경,stdout=ჟურნალი_ჩაწერა,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(მონაცემები_პოზიცია);return მონაცემები_პოზიცია
            환경=dict(os.environ)
            for სახელი in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(სახელი,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            მონიტორი=გაშვება(სერვერი_მნიშვნელობა+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert მონიტორი.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            სტუმარი=subprocess.Popen(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ბრძანება.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(სტუმარი);სელექტორი.register(სტუმარი.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ოფსეტი_მნიშვნელობა=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ოფსეტი_მნიშვნელობა:]:
                    assert სტუმარი.poll() is None and time.monotonic()<마감시각,직렬입출력[ოფსეტი_მნიშვნელობა:].decode('utf-8','replace')
                    for 누름값,_ in სელექტორი.select(.1):
                        მონაცემები=누름값.fileobj.read(65536)
                        if მონაცემები:직렬입출력.extend(მონაცემები)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            პროფილი=작업경로/'test.remmina'
            პროფილი.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            გაშვება(['dbus-run-session','--','remmina','-c',str(პროფილი)],환경=환경,start_new_session=True)
            def 가상입력도구(*არგუმენტი_მასივი):return subprocess.check_output(['xdotool']+list(არგუმენტი_მასივი),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ფანჯარა=None
            while time.monotonic()<마감시각:
                ძებნა_გაზომვა=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ძებნა_გაზომვა.returncode==0:
                    후보=ძებნა_გაზომვა.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ფოკუსირებული=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ფოკუსირებული.returncode==0:ფანჯარა=후보;break
                time.sleep(.1)
            assert ფანჯარა,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ფანჯარა,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ტექსტი):가상입력도구('type','--clearmodifiers','--delay','50',ტექსტი)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ოფსეტი_მნიშვნელობა=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 კლავიში_მნიშვნელობა, Shift+Space 또는 F9'.encode(),ოფსეტი_მნიშვნელობა);기다리기(b'jkoros-native> ',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ოფსეტი_მნიშვნელობა)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ფანჯარა,str(გაზომვა_მონაცემები/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ოფსეტი_მნიშვნელობა)
            # რეალური_მონაცემები Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ნახატი_მნიშვნელობა_c143fe9e=Image.open(str(გაზომვა_მონაცემები/'remmina-korean.png')).convert('RGB')
            სათაურის_ზოლი=None
            for ვერტიკალური_პოზიცია in range(ნახატი_მნიშვნელობა_c143fe9e.height):
                가로들=[가로 for 가로 in range(ნახატი_მნიშვნელობა_c143fe9e.width) if ნახატი_მნიშვნელობა_c143fe9e.getpixel((가로,ვერტიკალური_პოზიცია))==(32,80,144)]
                if len(가로들)>=500:სათაურის_ზოლი=(min(가로들),ვერტიკალური_პოზიცია);break
            assert სათაურის_ზოლი,'native terminal title bar not found'
            가로,ვერტიკალური_პოზიცია=სათაურის_ზოლი[0]+564,სათაურის_ზოლი[1]+356
            가상입력도구('mousemove','--window',ფანჯარა,str(가로),str(ვერტიკალური_პოზიცია))
            def 화상기다리기(სახელი,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ფანჯარა,str(გაზომვა_მონაცემები/სახელი)])
                    რასტერული_გრაფიკა_ნახატი=Image.open(str(გაზომვა_მონაცემები/სახელი)).convert('RGB')
                    if all(რასტერული_გრაფიკა_ნახატი.getpixel(პოზიცია)==빛 for პოზიცია,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+სახელი
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ვერტიკალური_პოზიცია-7),(255,255,255)),((가로+7,ვერტიკალური_პოზიცია+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ფანჯარა,str(가로-120),str(ვერტიკალური_პოზიცია-80),'mouseup','1')
            time.sleep(.4)
            ოფსეტი_მნიშვნელობა=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ოფსეტი_მნიშვნელობა)
            가상입력도구('mousemove','--window',ფანჯარა,'500','45')
            화상기다리기('remmina-resized.png',[
                ((სათაურის_ზოლი[0]+447,სათაურის_ზოლი[1]+279),(39,49,64)),((가로,ვერტიკალური_პოზიცია),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            გადამოწმება_ანგარიში.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not გადამოწმება_ანგარიში['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(გაზომვა_მონაცემები/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for მონაცემები_პოზიცია in reversed(실행과정들):
                if მონაცემები_პოზიცია.poll() is None:
                    if მონაცემები_პოზიცია.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(მონაცემები_პოზიცია.pid,signal.SIGTERM)
                    else:მონაცემები_პოზიცია.terminate()
                    try:მონაცემები_პოზიცია.wait(timeout=5)
                    except subprocess.TimeoutExpired:მონაცემები_პოზიცია.kill();მონაცემები_პოზიცია.wait()
            სელექტორი.close()
            for ფაილი_შენატანი in 기록들:ფაილი_შენატანი.close()
            (გაზომვა_მონაცემები/'serial.log').write_bytes(직렬입출력)
            (გაზომვა_მონაცემები/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':გაშვება()
