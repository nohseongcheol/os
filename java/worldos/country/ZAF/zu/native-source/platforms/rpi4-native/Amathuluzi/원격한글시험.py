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
from yenza_umyalo import 기준


def Sebenzisa():
    결과자료=기준/'build/verification/remmina';결과자료.mkdir(parents=True,exist_ok=True)
    ukufakazisa_umbiko={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];isiqoki=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            utalagu_bonisa=shutil.which('Xvfb')
            if utalagu_bonisa: Iseva_inani=[utalagu_bonisa]
            else:
                뿌리파일계층=기준.parent/'rpi4/build/rootfs'
                Iseva_inani=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def Sebenzisa(i_agumenti_AMALUNGU_AFANAYO,환경=None,**이름붙인인수):
                loga_umugqa=(결과자료/('process-%d.log'%len(기록들))).open('wb');기록들.append(loga_umugqa)
                자료위치=subprocess.Popen(i_agumenti_AMALUNGU_AFANAYO,env=환경,stdout=loga_umugqa,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(자료위치);return 자료위치
            환경=dict(os.environ)
            for Igama in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Igama,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(개수 for 개수 in range(80,200) if not Path('/tmp/.X11-unix/X'+str(개수)).exists() and not Path('/tmp/.X%d-lock'%개수).exists())
            환경['DISPLAY']=':'+str(수치)
            isibonisi=Sebenzisa(Iseva_inani+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert isibonisi.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            isivakashi=subprocess.Popen(['python3',str(기준/'Amathuluzi/yenza_umyalo.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(isivakashi);isiqoki.register(isivakashi.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,I_ofisethi_inani=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[I_ofisethi_inani:]:
                    assert isivakashi.poll() is None and time.monotonic()<마감시각,직렬입출력[I_ofisethi_inani:].decode('utf-8','replace')
                    for 누름값,_ in isiqoki.select(.1):
                        imininingwane=누름값.fileobj.read(65536)
                        if imininingwane:직렬입출력.extend(imininingwane)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Iphrofayili=작업경로/'test.remmina'
            Iphrofayili.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            Sebenzisa(['dbus-run-session','--','remmina','-c',str(Iphrofayili)],환경=환경,start_new_session=True)
            def 가상입력도구(*i_agumenti_AMALUNGU_AFANAYO):return subprocess.check_output(['xdotool']+list(i_agumenti_AMALUNGU_AFANAYO),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;ifasitela=None
            while time.monotonic()<마감시각:
                찾은결과=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if 찾은결과.returncode==0:
                    후보=찾은결과.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Okugxilile=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Okugxilile.returncode==0:ifasitela=후보;break
                time.sleep(.1)
            assert ifasitela,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',ifasitela,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Itekisi):가상입력도구('type','--clearmodifiers','--delay','50',Itekisi)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            I_ofisethi_inani=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),I_ofisethi_inani)
            I_ofisethi_inani=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),I_ofisethi_inani)
            I_ofisethi_inani=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 inkomba_inani, Shift+Space 또는 F9'.encode(),I_ofisethi_inani);기다리기(b'jkoros-native> ',I_ofisethi_inani)
            I_ofisethi_inani=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),I_ofisethi_inani)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ifasitela,str(결과자료/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',I_ofisethi_inani)
            # ulwazi_ngokwenzekile_imininingwane Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            umdwebo_inani=Image.open(str(결과자료/'remmina-korean.png')).convert('RGB')
            indawo_yesihloko=None
            for 세로 in range(umdwebo_inani.height):
                가로들=[가로 for 가로 in range(umdwebo_inani.width) if umdwebo_inani.getpixel((가로,세로))==(32,80,144)]
                if len(가로들)>=500:indawo_yesihloko=(min(가로들),세로);break
            assert indawo_yesihloko,'native terminal title bar not found'
            가로,세로=indawo_yesihloko[0]+564,indawo_yesihloko[1]+356
            가상입력도구('mousemove','--window',ifasitela,str(가로),str(세로))
            def 화상기다리기(Igama,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',ifasitela,str(결과자료/Igama)])
                    isithombe_samabhithi_isithombe=Image.open(str(결과자료/Igama)).convert('RGB')
                    if all(isithombe_samabhithi_isithombe.getpixel(위치)==빛 for 위치,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Igama
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,세로-7),(255,255,255)),((가로+7,세로+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',ifasitela,str(가로-120),str(세로-80),'mouseup','1')
            time.sleep(.4)
            I_ofisethi_inani=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',I_ofisethi_inani)
            가상입력도구('mousemove','--window',ifasitela,'500','45')
            화상기다리기('remmina-resized.png',[
                ((indawo_yesihloko[0]+447,indawo_yesihloko[1]+279),(39,49,64)),((가로,세로),(24,32,48))])
            if shutil.which('dpkg-query'):
                판번호=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                판번호=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            ukufakazisa_umbiko.update(passed=True,display=환경['DISPLAY'],remmina_version=판번호,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not ukufakazisa_umbiko['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(결과자료/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for 자료위치 in reversed(실행과정들):
                if 자료위치.poll() is None:
                    if 자료위치.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(자료위치.pid,signal.SIGTERM)
                    else:자료위치.terminate()
                    try:자료위치.wait(timeout=5)
                    except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            isiqoki.close()
            for ifayela_okufakwayo in 기록들:ifayela_okufakwayo.close()
            (결과자료/'serial.log').write_bytes(직렬입출력)
            (결과자료/'report.json').write_text(json.dumps(ukufakazisa_umbiko,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Sebenzisa()
