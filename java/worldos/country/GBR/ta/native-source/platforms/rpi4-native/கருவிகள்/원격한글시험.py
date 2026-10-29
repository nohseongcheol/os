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
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def செயல்படுத்துக():
    அளவிடக்கூடியது_தரவு=திட்டப்பணி_மூலம்/'build/verification/remmina';அளவிடக்கூடியது_தரவு.mkdir(parents=True,exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];தேர்வி=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            தோற்றநிலை_காட்சி=shutil.which('Xvfb')
            if தோற்றநிலை_காட்சி: சேவையகம்_மதிப்பு=[தோற்றநிலை_காட்சி]
            else:
                뿌리파일계층=திட்டப்பணி_மூலம்.parent/'rpi4/build/rootfs'
                சேவையகம்_மதிப்பு=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def செயல்படுத்துக(மதிப்புரு_கோவை,환경=None,**이름붙인인수):
                பதிவு_பதிவு=(அளவிடக்கூடியது_தரவு/('process-%d.log'%len(기록들))).open('wb');기록들.append(பதிவு_பதிவு)
                தரவு_நிலை=subprocess.Popen(மதிப்புரு_கோவை,env=환경,stdout=பதிவு_பதிவு,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(தரவு_நிலை);return தரவு_நிலை
            환경=dict(os.environ)
            for பெயர் in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(பெயர்,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            காட்சி=செயல்படுத்துக(சேவையகம்_மதிப்பு+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert காட்சி.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            விருந்தினர்=subprocess.Popen(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கட்டளை.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(விருந்தினர்);தேர்வி.register(விருந்தினர்.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ஆஃப்செட்_மதிப்பு=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ஆஃப்செட்_மதிப்பு:]:
                    assert விருந்தினர்.poll() is None and time.monotonic()<마감시각,직렬입출력[ஆஃப்செட்_மதிப்பு:].decode('utf-8','replace')
                    for 누름값,_ in தேர்வி.select(.1):
                        தரவு=누름값.fileobj.read(65536)
                        if தரவு:직렬입출력.extend(தரவு)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            முனைய_எண்=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            குறிப்பு=작업경로/'test.remmina'
            குறிப்பு.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%முனைய_எண்)
            செயல்படுத்துக(['dbus-run-session','--','remmina','-c',str(குறிப்பு)],환경=환경,start_new_session=True)
            def 가상입력도구(*மதிப்புரு_கோவை):return subprocess.check_output(['xdotool']+list(மதிப்புரு_கோவை),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;சாளரம்=None
            while time.monotonic()<마감시각:
                தேடு_அளவிடக்கூடியது=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if தேடு_அளவிடக்கூடியது.returncode==0:
                    후보=தேடு_அளவிடக்கூடியது.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ஃபோகஸ்டு=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ஃபோகஸ்டு.returncode==0:சாளரம்=후보;break
                time.sleep(.1)
            assert சாளரம்,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',சாளரம்,'280','240','click','1')
            time.sleep(1)
            def 글자입력(உரை):가상입력도구('type','--clearmodifiers','--delay','50',உரை)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ஆஃப்செட்_மதிப்பு=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 சாவி_மதிப்பு, Shift+Space 또는 F9'.encode(),ஆஃப்செட்_மதிப்பு);기다리기(b'jkoros-native> ',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ஆஃப்செட்_மதிப்பு)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',சாளரம்,str(அளவிடக்கூடியது_தரவு/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ஆஃப்செட்_மதிப்பு)
            # அசல்_தரவு Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            வரைதல்_மதிப்பு=Image.open(str(அளவிடக்கூடியது_தரவு/'remmina-korean.png')).convert('RGB')
            தலைப்புப்_பட்டி=None
            for வெர்டிகல்_நிலை in range(வரைதல்_மதிப்பு.height):
                가로들=[가로 for 가로 in range(வரைதல்_மதிப்பு.width) if வரைதல்_மதிப்பு.getpixel((가로,வெர்டிகல்_நிலை))==(32,80,144)]
                if len(가로들)>=500:தலைப்புப்_பட்டி=(min(가로들),வெர்டிகல்_நிலை);break
            assert தலைப்புப்_பட்டி,'native terminal title bar not found'
            가로,வெர்டிகல்_நிலை=தலைப்புப்_பட்டி[0]+564,தலைப்புப்_பட்டி[1]+356
            가상입력도구('mousemove','--window',சாளரம்,str(가로),str(வெர்டிகல்_நிலை))
            def 화상기다리기(பெயர்,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',சாளரம்,str(அளவிடக்கூடியது_தரவு/பெயர்)])
                    பிட்_வரைபடம்_படம்=Image.open(str(அளவிடக்கூடியது_தரவு/பெயர்)).convert('RGB')
                    if all(பிட்_வரைபடம்_படம்.getpixel(இடம்)==빛 for இடம்,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+பெயர்
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,வெர்டிகல்_நிலை-7),(255,255,255)),((가로+7,வெர்டிகல்_நிலை+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',சாளரம்,str(가로-120),str(வெர்டிகல்_நிலை-80),'mouseup','1')
            time.sleep(.4)
            ஆஃப்செட்_மதிப்பு=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ஆஃப்செட்_மதிப்பு)
            가상입력도구('mousemove','--window',சாளரம்,'500','45')
            화상기다리기('remmina-resized.png',[
                ((தலைப்புப்_பட்டி[0]+447,தலைப்புப்_பட்டி[1]+279),(39,49,64)),((가로,வெர்டிகல்_நிலை),(24,32,48))])
            if shutil.which('dpkg-query'):
                பதிப்புரு_எண்=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                பதிப்புரு_எண்=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            செல்லுபடியாக்கம்_அறிக்கை.update(passed=True,display=환경['DISPLAY'],remmina_version=பதிப்புரு_எண்,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not செல்லுபடியாக்கம்_அறிக்கை['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(அளவிடக்கூடியது_தரவு/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for தரவு_நிலை in reversed(실행과정들):
                if தரவு_நிலை.poll() is None:
                    if தரவு_நிலை.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(தரவு_நிலை.pid,signal.SIGTERM)
                    else:தரவு_நிலை.terminate()
                    try:தரவு_நிலை.wait(timeout=5)
                    except subprocess.TimeoutExpired:தரவு_நிலை.kill();தரவு_நிலை.wait()
            தேர்வி.close()
            for கோப்பு_உள்ளீடு in 기록들:கோப்பு_உள்ளீடு.close()
            (அளவிடக்கூடியது_தரவு/'serial.log').write_bytes(직렬입출력)
            (அளவிடக்கூடியது_தரவு/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':செயல்படுத்துக()
