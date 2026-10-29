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
from ፈጽም_ትእዛዝ import አሳይ_ስር


def ማስኬጃ():
    ልኬት_ውሂብ=አሳይ_ስር/'build/verification/remmina';ልኬት_ውሂብ.mkdir(parents=True,exist_ok=True)
    ማረጋገጥ_ዘገባ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];መራጭ=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            ምናባዊ_ማሳያ=shutil.which('Xvfb')
            if ምናባዊ_ማሳያ: አገልጋይ_እሴት=[ምናባዊ_ማሳያ]
            else:
                뿌리파일계층=አሳይ_ስር.parent/'rpi4/build/rootfs'
                አገልጋይ_እሴት=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def ማስኬጃ(ነጋሪ_እሴት_ድርድር,환경=None,**이름붙인인수):
                መዝግብ_ረድፍ=(ልኬት_ውሂብ/('process-%d.log'%len(기록들))).open('wb');기록들.append(መዝግብ_ረድፍ)
                ውሂብ_በቦታ_አስቀመጠ=subprocess.Popen(ነጋሪ_እሴት_ድርድር,env=환경,stdout=መዝግብ_ረድፍ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ውሂብ_በቦታ_አስቀመጠ);return ውሂብ_በቦታ_አስቀመጠ
            환경=dict(os.environ)
            for ስም in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(ስም,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            ማሳያ=ማስኬጃ(አገልጋይ_እሴት+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert ማሳያ.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            እንግዳ=subprocess.Popen(['python3',str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ትእዛዝ.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(እንግዳ);መራጭ.register(እንግዳ.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ዝንፍ_እሴት=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ዝንፍ_እሴት:]:
                    assert እንግዳ.poll() is None and time.monotonic()<마감시각,직렬입출력[ዝንፍ_እሴት:].decode('utf-8','replace')
                    for 누름값,_ in መራጭ.select(.1):
                        ውሂብ=누름값.fileobj.read(65536)
                        if ውሂብ:직렬입출력.extend(ውሂብ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            የወደብ_ቁጥር=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            መገለጫ=작업경로/'test.remmina'
            መገለጫ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%የወደብ_ቁጥር)
            ማስኬጃ(['dbus-run-session','--','remmina','-c',str(መገለጫ)],환경=환경,start_new_session=True)
            def 가상입력도구(*ነጋሪ_እሴት_ድርድር):return subprocess.check_output(['xdotool']+list(ነጋሪ_እሴት_ድርድር),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;መስኮት=None
            while time.monotonic()<마감시각:
                ፈልግ_ልኬት=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if ፈልግ_ልኬት.returncode==0:
                    후보=ፈልግ_ልኬት.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    የተተኮረ=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if የተተኮረ.returncode==0:መስኮት=후보;break
                time.sleep(.1)
            assert መስኮት,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',መስኮት,'280','240','click','1')
            time.sleep(1)
            def 글자입력(ጽሁፍ):가상입력도구('type','--clearmodifiers','--delay','50',ጽሁፍ)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ዝንፍ_እሴት=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ዝንፍ_እሴት)
            ዝንፍ_እሴት=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ዝንፍ_እሴት)
            ዝንፍ_እሴት=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 ቁልፍ_እሴት, Shift+Space 또는 F9'.encode(),ዝንፍ_እሴት);기다리기(b'jkoros-native> ',ዝንፍ_እሴት)
            ዝንፍ_እሴት=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ዝንፍ_እሴት)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',መስኮት,str(ልኬት_ውሂብ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ዝንፍ_እሴት)
            # ትክክለኛ_ውሂብ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ስዕል_እሴት=Image.open(str(ልኬት_ውሂብ/'remmina-korean.png')).convert('RGB')
            የርእስ_አሞሌ=None
            for ቋሚ_በቦታ_አስቀመጠ in range(ስዕል_እሴት.height):
                가로들=[가로 for 가로 in range(ስዕል_እሴት.width) if ስዕል_እሴት.getpixel((가로,ቋሚ_በቦታ_አስቀመጠ))==(32,80,144)]
                if len(가로들)>=500:የርእስ_አሞሌ=(min(가로들),ቋሚ_በቦታ_አስቀመጠ);break
            assert የርእስ_አሞሌ,'native terminal title bar not found'
            가로,ቋሚ_በቦታ_አስቀመጠ=የርእስ_አሞሌ[0]+564,የርእስ_አሞሌ[1]+356
            가상입력도구('mousemove','--window',መስኮት,str(가로),str(ቋሚ_በቦታ_አስቀመጠ))
            def 화상기다리기(ስም,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',መስኮት,str(ልኬት_ውሂብ/ስም)])
                    ቢትማፕ_ምስል=Image.open(str(ልኬት_ውሂብ/ስም)).convert('RGB')
                    if all(ቢትማፕ_ምስል.getpixel(አካባቢ)==빛 for አካባቢ,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+ስም
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ቋሚ_በቦታ_አስቀመጠ-7),(255,255,255)),((가로+7,ቋሚ_በቦታ_አስቀመጠ+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',መስኮት,str(가로-120),str(ቋሚ_በቦታ_አስቀመጠ-80),'mouseup','1')
            time.sleep(.4)
            ዝንፍ_እሴት=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ዝንፍ_እሴት)
            가상입력도구('mousemove','--window',መስኮት,'500','45')
            화상기다리기('remmina-resized.png',[
                ((የርእስ_አሞሌ[0]+447,የርእስ_አሞሌ[1]+279),(39,49,64)),((가로,ቋሚ_በቦታ_አስቀመጠ),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ማረጋገጥ_ዘገባ.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ማረጋገጥ_ዘገባ['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ልኬት_ውሂብ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ውሂብ_በቦታ_አስቀመጠ in reversed(실행과정들):
                if ውሂብ_በቦታ_አስቀመጠ.poll() is None:
                    if ውሂብ_በቦታ_አስቀመጠ.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ውሂብ_በቦታ_አስቀመጠ.pid,signal.SIGTERM)
                    else:ውሂብ_በቦታ_አስቀመጠ.terminate()
                    try:ውሂብ_በቦታ_አስቀመጠ.wait(timeout=5)
                    except subprocess.TimeoutExpired:ውሂብ_በቦታ_አስቀመጠ.kill();ውሂብ_በቦታ_አስቀመጠ.wait()
            መራጭ.close()
            for ፋይል_ምዝግብ in 기록들:ፋይል_ምዝግብ.close()
            (ልኬት_ውሂብ/'serial.log').write_bytes(직렬입출력)
            (ልኬት_ውሂብ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ማስኬጃ()
