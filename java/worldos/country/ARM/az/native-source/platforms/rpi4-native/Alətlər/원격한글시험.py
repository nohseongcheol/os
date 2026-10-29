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
from icra_etmək_əmr import Project_kök


def İcra_Et():
    ölçü_verilənlər=Project_kök/'build/verification/remmina';ölçü_verilənlər.mkdir(parents=True,exist_ok=True)
    yoxlama_hesabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];seçici=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            virtual_displey=shutil.which('Xvfb')
            if virtual_displey: server_VALUE=[virtual_displey]
            else:
                뿌리파일계층=Project_kök.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def İcra_Et(arqument_ARRAY,환경=None,**이름붙인인수):
                LOG_yaz=(ölçü_verilənlər/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_yaz)
                verilənlər_yerinə_qoymaq=subprocess.Popen(arqument_ARRAY,env=환경,stdout=LOG_yaz,stderr=subprocess.STDOUT,**이름붙인인수)
                실행과정들.append(verilənlər_yerinə_qoymaq);return verilənlər_yerinə_qoymaq
            환경=dict(os.environ)
            for Ad in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):환경.pop(Ad,None)
            환경.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(element_COUNT for element_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(element_COUNT)).exists() and not Path('/tmp/.X%d-lock'%element_COUNT).exists())
            환경['DISPLAY']=':'+str(수치)
            displey=İcra_Et(server_VALUE+[환경['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],환경=환경)
            마감시각=time.monotonic()+30
            while True:
                assert displey.poll() is None and time.monotonic()<마감시각,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=환경,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            qonaq=subprocess.Popen(['python3',str(Project_kök/'Alətlər/icra_etmək_əmr.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(qonaq);seçici.register(qonaq.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                마감시각=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert qonaq.poll() is None and time.monotonic()<마감시각,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in seçici.select(.1):
                        verilənlər=누름값.fileobj.read(65536)
                        if verilənlər:직렬입출력.extend(verilənlər)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%접속번호)
            İcra_Et(['dbus-run-session','--','remmina','-c',str(Profil)],환경=환경,start_new_session=True)
            def 가상입력도구(*arqument_ARRAY):return subprocess.check_output(['xdotool']+list(arqument_ARRAY),env=환경,stderr=subprocess.STDOUT)
            마감시각=time.monotonic()+60;pəncərə=None
            while time.monotonic()<마감시각:
                SEARCH_ölçü=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=환경,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if SEARCH_ölçü.returncode==0:
                    후보=SEARCH_ölçü.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Fokuslanmış=subprocess.run(['xdotool','windowfocus','--sync',후보],env=환경,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Fokuslanmış.returncode==0:pəncərə=후보;break
                time.sleep(.1)
            assert pəncərə,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',pəncərə,'280','240','click','1')
            time.sleep(1)
            def 글자입력(Mətn):가상입력도구('type','--clearmodifiers','--delay','50',Mətn)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Açar_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',pəncərə,str(ölçü_verilənlər/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # faktiki_verilənlər Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            rəsm_VALUE=Image.open(str(ölçü_verilənlər/'remmina-korean.png')).convert('RGB')
            başlıq_sətri=None
            for Şaquli_yerinə_qoymaq in range(rəsm_VALUE.height):
                가로들=[가로 for 가로 in range(rəsm_VALUE.width) if rəsm_VALUE.getpixel((가로,Şaquli_yerinə_qoymaq))==(32,80,144)]
                if len(가로들)>=500:başlıq_sətri=(min(가로들),Şaquli_yerinə_qoymaq);break
            assert başlıq_sətri,'native terminal title bar not found'
            가로,Şaquli_yerinə_qoymaq=başlıq_sətri[0]+564,başlıq_sətri[1]+356
            가상입력도구('mousemove','--window',pəncərə,str(가로),str(Şaquli_yerinə_qoymaq))
            def 화상기다리기(Ad,점들):
                마감=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',환경['DISPLAY'],'-window',pəncərə,str(ölçü_verilənlər/Ad)])
                    nöqtəli_təsvir_IMAGE=Image.open(str(ölçü_verilənlər/Ad)).convert('RGB')
                    if all(nöqtəli_təsvir_IMAGE.getpixel(yerinə_qoymaq)==빛 for yerinə_qoymaq,빛 in 점들):return
                    assert time.monotonic()<마감,'Remmina framebuffer did not settle: '+Ad
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Şaquli_yerinə_qoymaq-7),(255,255,255)),((가로+7,Şaquli_yerinə_qoymaq+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',pəncərə,str(가로-120),str(Şaquli_yerinə_qoymaq-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',pəncərə,'500','45')
            화상기다리기('remmina-resized.png',[
                ((başlıq_sətri[0]+447,başlıq_sətri[1]+279),(39,49,64)),((가로,Şaquli_yerinə_qoymaq),(24,32,48))])
            if shutil.which('dpkg-query'):
                versiya_nömrəsi=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                versiya_nömrəsi=subprocess.check_output(['remmina','--version'],env=환경,stderr=subprocess.STDOUT).decode('utf-8','replace')
            yoxlama_hesabat.update(passed=True,display=환경['DISPLAY'],remmina_version=versiya_nömrəsi,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not yoxlama_hesabat['passed'] and '환경' in locals() and 환경.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',환경['DISPLAY'],'-window','root',str(ölçü_verilənlər/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for verilənlər_yerinə_qoymaq in reversed(실행과정들):
                if verilənlər_yerinə_qoymaq.poll() is None:
                    if verilənlər_yerinə_qoymaq.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(verilənlər_yerinə_qoymaq.pid,signal.SIGTERM)
                    else:verilənlər_yerinə_qoymaq.terminate()
                    try:verilənlər_yerinə_qoymaq.wait(timeout=5)
                    except subprocess.TimeoutExpired:verilənlər_yerinə_qoymaq.kill();verilənlər_yerinə_qoymaq.wait()
            seçici.close()
            for fayl_daxiletmə in 기록들:fayl_daxiletmə.close()
            (ölçü_verilənlər/'serial.log').write_bytes(직렬입출력)
            (ölçü_verilənlər/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':İcra_Et()
