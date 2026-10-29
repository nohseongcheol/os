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
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def ଚଳାନ୍ତୁ():
    ମାପ_ଡାଟା=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/remmina';ମାପ_ଡାଟା.mkdir(parents=True,exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];ଚୟନକାରୀ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ବାସ୍ତବ_ଦେଖାଇବା=shutil.which('Xvfb')
            if ବାସ୍ତବ_ଦେଖାଇବା: ସର୍ଭର୍_ମୂଲ୍ୟ=[ବାସ୍ତବ_ଦେଖାଇବା]
            else:
                뿌리파일계층=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parent/'rpi4/build/rootfs'
                ସର୍ଭର୍_ମୂଲ୍ୟ=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ଚଳାନ୍ତୁ(ଯୁକ୍ତି_ଆରେ,환경=None,**이름붙인인수):
                ଲଗ୍_ଧାଡ଼ି=(ମାପ_ଡାଟା/('process-%d.log'%len(기록들))).open('wb');기록들.append(ଲଗ୍_ଧାଡ଼ି)
                ଡାଟା_ସ୍ଥିତି=subprocess.Popen(ଯୁକ୍ତି_ଆରେ,env=환경,stdout=ଲଗ୍_ଧାଡ଼ି,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ଡାଟା_ସ୍ଥିତି);return ଡାଟା_ସ୍ଥିତି
            환경=dict(os.environ)
            for ନାମ in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ନାମ,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ଦେଖାଇବା=ଚଳାନ୍ତୁ(ସର୍ଭର୍_ମୂଲ୍ୟ+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ଦେଖାଇବା.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            ଅତିଥି=subprocess.Popen(['python3',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(ଅତିଥି);ଚୟନକାରୀ.register(ଅତିଥି.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:]:
                    assert ଅତିଥି.poll() is None and time.monotonic()<마감시각,직렬입출력[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:].decode('utf-8','replace')
                    for 누름값,_ in ଚୟନକାରୀ.select(.1):
                        ଡାଟା=누름값.fileobj.read(65536)
                        if ଡାଟା:직렬입출력.extend(ଡାଟା)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            ପୋର୍ଟ୍_ନମ୍ଵର୍=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            ପ୍ରୋଫାଇଲ୍=작업경로/'test.remmina'
            ପ୍ରୋଫାଇଲ୍.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%ପୋର୍ଟ୍_ନମ୍ଵର୍)
            ଚଳାନ୍ତୁ(['dbus-run-session','--','remmina','-c',str(ପ୍ରୋଫାଇଲ୍)],환경=환경,start_new_session=True)
            def 가상입력도구(*ଯୁକ୍ତି_ଆରେ):return subprocess.check_output(['xdotool']+list(ଯୁକ୍ତି_ଆରେ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ଓ୍ୱିଣ୍ଡୋ=None
            while time.monotonic()<마감시각:
                ସନ୍ଧାନ_ମାପ=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ସନ୍ଧାନ_ମାପ.returncode==0:
                    후보=ସନ୍ଧାନ_ମାପ.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    କେନ୍ଦ୍ରିକ_f7e69dab=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if କେନ୍ଦ୍ରିକ_f7e69dab.returncode==0:ଓ୍ୱିଣ୍ଡୋ=후보;break
                time.sleep(.1)
            assert ଓ୍ୱିଣ୍ଡୋ,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ଓ୍ୱିଣ୍ଡୋ,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ପାଠ୍ଯ):가상입력도구('type','--clearmodifiers','--delay','50',ପାଠ୍ଯ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 କୀ_ମୂଲ୍ୟ, Shift+Space 또는 F9'.encode(),ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ);기다리기(b'jkoros-native> ',ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ଓ୍ୱିଣ୍ଡୋ,str(ମାପ_ଡାଟା/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            # ପ୍ରକୃତ_ଡାଟା Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ଅଙ୍କନ_ମୂଲ୍ୟ=Image.open(str(ମାପ_ଡାଟା/'remmina-korean.png')).convert('RGB')
            ଟାଇଟେଲ୍_ଦଣ୍ଡିକା=None
            for ଅନୁଲମ୍ବ_ସ୍ଥିତି in range(ଅଙ୍କନ_ମୂଲ୍ୟ.height):
                가로들=[가로 for 가로 in range(ଅଙ୍କନ_ମୂଲ୍ୟ.width) if ଅଙ୍କନ_ମୂଲ୍ୟ.getpixel((가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି))==(32,80,144)]
                if len(가로들)>=500:ଟାଇଟେଲ୍_ଦଣ୍ଡିକା=(min(가로들),ଅନୁଲମ୍ବ_ସ୍ଥିତି);break
            assert ଟାଇଟେଲ୍_ଦଣ୍ଡିକା,'native terminal title bar not found'
            가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି=ଟାଇଟେଲ୍_ଦଣ୍ଡିକା[0]+564,ଟାଇଟେଲ୍_ଦଣ୍ଡିକା[1]+356
            가상입력도구('mousemove','--window',ଓ୍ୱିଣ୍ଡୋ,str(가로),str(ଅନୁଲମ୍ବ_ସ୍ଥିତି))
            def 화상기다리기(ନାମ,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ଓ୍ୱିଣ୍ଡୋ,str(ମାପ_ଡାଟା/ନାମ)])
                    ବିଟ୍_ମ୍ୟାପ୍_ଚିତ୍ର=Image.open(str(ମାପ_ଡାଟା/ନାମ)).convert('RGB')
                    if all(ବିଟ୍_ମ୍ୟାପ୍_ଚିତ୍ର.getpixel(ଅବସ୍ଥାନ)==빛 for ଅବସ୍ଥାନ,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ନାମ
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ଅନୁଲମ୍ବ_ସ୍ଥିତି-7),(255,255,255)),((가로+7,ଅନୁଲମ୍ବ_ସ୍ଥିତି+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ଓ୍ୱିଣ୍ଡୋ,str(가로-120),str(ଅନୁଲମ୍ବ_ସ୍ଥିତି-80),'mouseup','1')
            time.sleep(.4)
            ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
            가상입력도구('mousemove','--window',ଓ୍ୱିଣ୍ଡୋ,'500','45')
            화상기다리기('remmina-resized.png',[
                ((ଟାଇଟେଲ୍_ଦଣ୍ଡିକା[0]+447,ଟାଇଟେଲ୍_ଦଣ୍ଡିକା[1]+279),(39,49,64)),((가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ବୈଧକରଣ_ରିପୋର୍ଟ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ମାପ_ଡାଟା/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ଡାଟା_ସ୍ଥିତି in reversed(실행과정들):
                if ଡାଟା_ସ୍ଥିତି.poll() is None:
                    if ଡାଟା_ସ୍ଥିତି.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ଡାଟା_ସ୍ଥିତି.pid,signal.SIGTERM)
                    else:ଡାଟା_ସ୍ଥିତି.terminate()
                    try:ଡାଟା_ସ୍ଥିତି.wait(timeout=5)
                    except subprocess.TimeoutExpired:ଡାଟା_ସ୍ଥିତି.kill();ଡାଟା_ସ୍ଥିତି.wait()
            ଚୟନକାରୀ.close()
            for ଫାଇଲ୍_ଏଣ୍ଟ୍ରି in 기록들:ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.close()
            (ମାପ_ଡାଟା/'serial.log').write_bytes(직렬입출력)
            (ମାପ_ଡାଟା/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ଚଳାନ୍ତୁ()
