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
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def നടപ്പിലാക്കുക():
    അളവ്_ഡാറ്റാ=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/remmina';അളവ്_ഡാറ്റാ.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];సెలక్టర్=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            അയഥാര്_ഥ_പ്രദര്_ശനം=shutil.which('Xvfb')
            if അയഥാര്_ഥ_പ്രദര്_ശനം: സെര്_വര്_മൂല്യം=[അയഥാര്_ഥ_പ്രദര്_ശനം]
            else:
                뿌리파일계층=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parent/'rpi4/build/rootfs'
                സെര്_വര്_മൂല്യം=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def നടപ്പിലാക്കുക(ആര്_ഗ്യുമെന്_റ്_അരേ,환경=None,**이름붙인인수):
                ലോഗ്_രേഖ=(അളവ്_ഡാറ്റാ/('process-%d.log'%len(기록들))).open('wb');기록들.append(ലോഗ്_രേഖ)
                ഡാറ്റാ_പദവി=subprocess.Popen(ആര്_ഗ്യുമെന്_റ്_അരേ,env=환경,stdout=ലോഗ്_രേഖ,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(ഡാറ്റാ_പദവി);return ഡാറ്റാ_പദവി
            환경=dict(os.environ)
            for പേരു് in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(പേരു്,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            പ്രദര്_ശനം=നടപ്പിലാക്കുക(സെര്_വര്_മൂല്യം+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert പ്രദര്_ശനം.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            അതിഥി=subprocess.Popen(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(അതിഥി);సెలక్టర్.register(അതിഥി.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,ഓഫ്_സെറ്റ്_മൂല്യം=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[ഓഫ്_സെറ്റ്_മൂല്യം:]:
                    assert അതിഥി.poll() is None and time.monotonic()<마감시각,직렬입출력[ഓഫ്_സെറ്റ്_മൂല്യം:].decode('utf-8','replace')
                    for 누름값,_ in సెలక్టర్.select(.1):
                        ഡാറ്റാ=누름값.fileobj.read(65536)
                        if ഡാറ്റാ:직렬입출력.extend(ഡാറ്റാ)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            പോര്_ട്ട്_നമ്പര്=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            പ്രൊഫൈൽ=작업경로/'test.remmina'
            പ്രൊഫൈൽ.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%പോര്_ട്ട്_നമ്പര്)
            നടപ്പിലാക്കുക(['dbus-run-session','--','remmina','-c',str(പ്രൊഫൈൽ)],환경=환경,start_new_session=True)
            def 가상입력도구(*ആര്_ഗ്യുമെന്_റ്_അരേ):return subprocess.check_output(['xdotool']+list(ആര്_ഗ്യുമെന്_റ്_അരേ),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ജാലകം=None
            while time.monotonic()<마감시각:
                തിരയൽ_അളവ്=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if തിരയൽ_അളവ്.returncode==0:
                    후보=തിരയൽ_അളവ്.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    ഫോക്കസ്_ഡ്=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if ഫോക്കസ്_ഡ്.returncode==0:ജാലകം=후보;break
                time.sleep(.1)
            assert ജാലകം,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ജാലകം,'280','240','click','1')
            time.sleep(1)
            def 글자입력(പദാവലി):가상입력도구('type','--clearmodifiers','--delay','50',പദാവലി)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 കീ_മൂല്യം, Shift+Space 또는 F9'.encode(),ഓഫ്_സെറ്റ്_മൂല്യം);기다리기(b'jkoros-native> ',ഓഫ്_സെറ്റ്_മൂല്യം)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),ഓഫ്_സെറ്റ്_മൂല്യം)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ജാലകം,str(അളവ്_ഡാറ്റാ/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',ഓഫ്_സെറ്റ്_മൂല്യം)
            # വാസ്തവമായ_ഡാറ്റാ Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            ഡ്രോയിംഗ്_മൂല്യം=Image.open(str(അളവ്_ഡാറ്റാ/'remmina-korean.png')).convert('RGB')
            ശീര്_ഷക_ബാര്=None
            for ലംബം_പദവി in range(ഡ്രോയിംഗ്_മൂല്യം.height):
                가로들=[가로 for 가로 in range(ഡ്രോയിംഗ്_മൂല്യം.width) if ഡ്രോയിംഗ്_മൂല്യം.getpixel((가로,ലംബം_പദവി))==(32,80,144)]
                if len(가로들)>=500:ശീര്_ഷക_ബാര്=(min(가로들),ലംബം_പദവി);break
            assert ശീര്_ഷക_ബാര്,'native terminal title bar not found'
            가로,ലംബം_പദവി=ശീര്_ഷക_ബാര്[0]+564,ശീര്_ഷക_ബാര്[1]+356
            가상입력도구('mousemove','--window',ജാലകം,str(가로),str(ലംബം_പദവി))
            def 화상기다리기(പേരു്,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ജാലകം,str(അളവ്_ഡാറ്റാ/പേരു്)])
                    ബിറ്റ്മാപ്പ്_ഇമേജ്=Image.open(str(അളവ്_ഡാറ്റാ/പേരു്)).convert('RGB')
                    if all(ബിറ്റ്മാപ്പ്_ഇമേജ്.getpixel(സ്ഥാനം)==빛 for സ്ഥാനം,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+പേരു്
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,ലംബം_പദവി-7),(255,255,255)),((가로+7,ലംബം_പദവി+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ജാലകം,str(가로-120),str(ലംബം_പദവി-80),'mouseup','1')
            time.sleep(.4)
            ഓഫ്_സെറ്റ്_മൂല്യം=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',ഓഫ്_സെറ്റ്_മൂല്യം)
            가상입력도구('mousemove','--window',ജാലകം,'500','45')
            화상기다리기('remmina-resized.png',[
                ((ശീര്_ഷക_ബാര്[0]+447,ശീര്_ഷക_ബാര്[1]+279),(39,49,64)),((가로,ലംബം_പദവി),(24,32,48))])
            if shutil.which('dpkg-query'):
                പതിപ്പ്_സംഖ്യ=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                പതിപ്പ്_സംഖ്യ=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            నిర్ధారణ_నివేదిక.update(passed=True,display=환경['DISPLAY'],remmina_version=പതിപ്പ്_സംഖ്യ,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not నిర్ధారణ_నివేదిక['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(അളവ്_ഡാറ്റാ/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for ഡാറ്റാ_പദവി in reversed(실행과정들):
                if ഡാറ്റാ_പദവി.poll() is None:
                    if ഡാറ്റാ_പദവി.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(ഡാറ്റാ_പദവി.pid,signal.SIGTERM)
                    else:ഡാറ്റാ_പദവി.terminate()
                    try:ഡാറ്റാ_പദവി.wait(timeout=5)
                    except subprocess.TimeoutExpired:ഡാറ്റാ_പദവി.kill();ഡാറ്റാ_പദവി.wait()
            సెలక్టర్.close()
            for ഫയല്_എന്_ട്രി in 기록들:ഫയല്_എന്_ട്രി.close()
            (അളവ്_ഡാറ്റാ/'serial.log').write_bytes(직렬입출력)
            (അളവ്_ഡാറ്റാ/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':നടപ്പിലാക്കുക()
