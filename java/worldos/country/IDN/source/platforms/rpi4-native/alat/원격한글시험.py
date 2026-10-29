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
from Jalankan_perintah import Tugas_akar


def jalankan():
    KR_data=Tugas_akar/'build/verification/remmina';KR_data.mkdir(parents=True,exist_ok=True)
    validasi_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix='jkoros-remmina-') as 작업경로:
        작업경로=Path(작업경로);실행과정들=[];pemilih=selectors.DefaultSelector();직렬입출력=bytearray()
        기록들=[]
        try:
            maya_tampilan=shutil.which('Xvfb')
            if maya_tampilan: server_VALUE=[maya_tampilan]
            else:
                뿌리파일계층=Tugas_akar.parent/'rpi4/build/rootfs'
                server_VALUE=['qemu-aarch64','-L',str(뿌리파일계층),str(뿌리파일계층/'usr/bin/Xvfb')]
            def jalankan(argumen_ARRAY,lingkungan=None,**argumen_bernama):
                LOG_baris=(KR_data/('process-%d.log'%len(기록들))).open('wb');기록들.append(LOG_baris)
                data_posisi=subprocess.Popen(argumen_ARRAY,env=lingkungan,stdout=LOG_baris,stderr=subprocess.STDOUT,**argumen_bernama)
                실행과정들.append(data_posisi);return data_posisi
            lingkungan=dict(os.environ)
            for Nama_2 in ('DISPLAY','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS','XAUTHORITY'):lingkungan.pop(Nama_2,None)
            lingkungan.update(GTK_IM_MODULE='gtk-im-context-simple',NO_AT_BRIDGE='1',
                XDG_CONFIG_HOME=str(작업경로/'config'),XDG_DATA_HOME=str(작업경로/'data'),XDG_CACHE_HOME=str(작업경로/'cache'))
            수치=next(item_COUNT for item_COUNT in range(80,200) if not Path('/tmp/.X11-unix/X'+str(item_COUNT)).exists() and not Path('/tmp/.X%d-lock'%item_COUNT).exists())
            lingkungan['DISPLAY']=':'+str(수치)
            tampilan=jalankan(server_VALUE+[lingkungan['DISPLAY'],'-screen','0','1024x768x24','-nolisten','tcp','-ac','-noreset','-extension','GLX'],lingkungan=lingkungan)
            tenggat_waktu_TIME=time.monotonic()+30
            while True:
                assert tampilan.poll() is None and time.monotonic()<tenggat_waktu_TIME,'Xvfb failed; see process-0.log'
                준비완료=subprocess.run(['xdotool','getdisplaygeometry'],env=lingkungan,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                if 준비완료.returncode==0:break
                time.sleep(.1)
            tamu=subprocess.Popen(['python3',str(Tugas_akar/'alat/Jalankan_perintah.py'),'--desktop','--port','0'],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            실행과정들.append(tamu);pemilih.register(tamu.stdout,selectors.EVENT_READ)
            def 기다리기(확인표시,OFFSET_VALUE=0):
                tenggat_waktu_TIME=time.monotonic()+45
                while 확인표시 not in 직렬입출력[OFFSET_VALUE:]:
                    assert tamu.poll() is None and time.monotonic()<tenggat_waktu_TIME,직렬입출력[OFFSET_VALUE:].decode('utf-8','replace')
                    for 누름값,_ in pemilih.select(.1):
                        data=누름값.fileobj.read(65536)
                        if data:직렬입출력.extend(data)
            기다리기(b'TERMINAL READY');기다리기(b'jkoros-native> ',직렬입출력.rfind(b'TERMINAL READY'))
            nomor_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',직렬입출력).group(1))
            Profil=작업경로/'test.remmina'
            Profil.write_text('[remmina]\nname=JKOROS_KOREAN_TEST\nprotocol=VNC\nserver=127.0.0.1:%d\nviewmode=1\nquality=9\ncolordepth=32\nscale=0\nviewonly=0\n'%nomor_port)
            jalankan(['dbus-run-session','--','remmina','-c',str(Profil)],lingkungan=lingkungan,start_new_session=True)
            def 가상입력도구(*argumen_ARRAY):return subprocess.check_output(['xdotool']+list(argumen_ARRAY),env=lingkungan,stderr=subprocess.STDOUT)
            tenggat_waktu_TIME=time.monotonic()+60;Jendela=None
            while time.monotonic()<tenggat_waktu_TIME:
                Cari_KR=subprocess.run(['xdotool','search','--onlyvisible','--name','JKOROS_KOREAN_TEST'],env=lingkungan,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
                if Cari_KR.returncode==0:
                    후보=Cari_KR.stdout.splitlines()[-1].decode()
                    time.sleep(.5)
                    Prioritas=subprocess.run(['xdotool','windowfocus','--sync',후보],env=lingkungan,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                    if Prioritas.returncode==0:Jendela=후보;break
                time.sleep(.1)
            assert Jendela,'Remmina window not found'
            # Click the VNC surface, away from its toolbar and title bar.
            가상입력도구('mousemove','--window',Jendela,'280','240','click','1')
            time.sleep(1)
            def 글자입력(teks):가상입력도구('type','--clearmodifiers','--delay','50',teks)
            def 누름값(*누름열):가상입력도구('key','--clearmodifiers',*누름열)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('dkssudgktpdy gksrmf');누름값('F9','Return')
            기다리기('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('shift+space');글자입력('rhk rkqtk');누름값('shift+space','Return')
            기다리기('\r\n과 갑사\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('help ko');누름값('Return')
            기다리기('한/영 Kunci_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE);기다리기(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(직렬입출력);글자입력('echo ');누름값('F9');글자입력('gksrmf dlfr')
            기다리기('읽'.encode(),OFFSET_VALUE)
            subprocess.check_call(['import','-display',lingkungan['DISPLAY'],'-window',Jendela,str(KR_data/'remmina-korean.png')])
            누름값('F9','Return')
            기다리기(b'jkoros-native> ',OFFSET_VALUE)
            # aktual_data Remmina의 화면 여백을 찾아 게스트 모서리를 왼쪽으로 끈다.
            from PIL import Image
            gambar_VALUE=Image.open(str(KR_data/'remmina-korean.png')).convert('RGB')
            bilah_judul=None
            for Vertikal_posisi in range(gambar_VALUE.height):
                가로들=[가로 for 가로 in range(gambar_VALUE.width) if gambar_VALUE.getpixel((가로,Vertikal_posisi))==(32,80,144)]
                if len(가로들)>=500:bilah_judul=(min(가로들),Vertikal_posisi);break
            assert bilah_judul,'native terminal title bar not found'
            가로,Vertikal_posisi=bilah_judul[0]+564,bilah_judul[1]+356
            가상입력도구('mousemove','--window',Jendela,str(가로),str(Vertikal_posisi))
            def 화상기다리기(Nama_2,점들):
                tenggat_waktu_VALUE=time.monotonic()+15
                while True:
                    subprocess.check_call(['import','-display',lingkungan['DISPLAY'],'-window',Jendela,str(KR_data/Nama_2)])
                    bitmap_foto=Image.open(str(KR_data/Nama_2)).convert('RGB')
                    if all(bitmap_foto.getpixel(posisi)==빛 for posisi,빛 in 점들):return
                    assert time.monotonic()<tenggat_waktu_VALUE,'Remmina framebuffer did not settle: '+Nama_2
                    time.sleep(.1)
            화상기다리기('remmina-resize-cursor.png',[
                ((가로-7,Vertikal_posisi-7),(255,255,255)),((가로+7,Vertikal_posisi+7),(255,255,255))])
            가상입력도구('mousedown','1','mousemove','--window',Jendela,str(가로-120),str(Vertikal_posisi-80),'mouseup','1')
            time.sleep(.4)
            OFFSET_VALUE=len(직렬입출력);글자입력('terminal size');누름값('Return')
            기다리기(b'TERMINAL SIZE 53x14\r\n',OFFSET_VALUE)
            가상입력도구('mousemove','--window',Jendela,'500','45')
            화상기다리기('remmina-resized.png',[
                ((bilah_judul[0]+447,bilah_judul[1]+279),(39,49,64)),((가로,Vertikal_posisi),(24,32,48))])
            if shutil.which('dpkg-query'):
                nomor_versi=subprocess.check_output(['dpkg-query','-W','-f','${Version}','remmina']).decode().strip()
            else:
                nomor_versi=subprocess.check_output(['remmina','--version'],env=lingkungan,stderr=subprocess.STDOUT).decode('utf-8','replace')
            validasi_lapor.update(passed=True,display=lingkungan['DISPLAY'],remmina_version=nomor_versi,
                checks=['actual Remmina VNC client, isolated X display and D-Bus',
                        'English ASCII keys -> F9 -> Korean composition -> English',
                        'Shift+Space toggles with compound vowels/final splitting',
                        'guest help ko advertises implemented shortcuts','KO title and Korean guest text screenshot',
                        'actual Remmina left-button corner resize changes grid to 53x14'])
            print('PASS: actual Remmina F9/Shift+Space Korean input and help',flush=True)
        finally:
            if not validasi_lapor['passed'] and 'lingkungan' in locals() and lingkungan.get('DISPLAY','').startswith(':'):
                try:
                    subprocess.run(['import','-display',lingkungan['DISPLAY'],'-window','root',str(KR_data/'failure.png')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
                except (OSError,subprocess.TimeoutExpired):pass
            for data_posisi in reversed(실행과정들):
                if data_posisi.poll() is None:
                    if data_posisi.args[0]=='dbus-run-session':
                        import signal
                        os.killpg(data_posisi.pid,signal.SIGTERM)
                    else:data_posisi.terminate()
                    try:data_posisi.wait(timeout=5)
                    except subprocess.TimeoutExpired:data_posisi.kill();data_posisi.wait()
            pemilih.close()
            for file_entri in 기록들:file_entri.close()
            (KR_data/'serial.log').write_bytes(직렬입출력)
            (KR_data/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':jalankan()
