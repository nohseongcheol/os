#!/usr/bin/env python3
"""현재 커널과 aktuell_Daten 시험·배포물이 일치할 때에만 통합 validéieren 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

projezéieren_Racinn = Path(__file__).resolve().parents[1]

def Hash_Fichier(Wee):
    계산 = hashlib.sha256()
    with Wee.open('rb') as Fichier:
        for Daten in iter(lambda: Fichier.read(1048576), b''): 계산.update(Daten)
    return 계산.hexdigest()

def Laf():
    Validatioun_Wee = projezéieren_Racinn/'build/verification'
    Kernel_Hash = Hash_Fichier(projezéieren_Racinn/'build/kernel8.img')
    기록들 = {}
    for Numm in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Numm == 'boot' else Numm+'/report.json'
        Daten = json.loads((Validatioun_Wee/상대경로).read_text())
        if not Daten.get('passed') or Daten.get('kernel_sha256') != Kernel_Hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Numm] = {'passed': True, 'report': 상대경로}
    Scheck_Numm = json.loads((Validatioun_Wee/'naming/report.json').read_text())
    if not Scheck_Numm['passed'] or not Scheck_Numm['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Wee, 기대값 in Scheck_Numm['c_source_sha256'].items():
        if Hash_Fichier(projezéieren_Racinn/Wee) != 기대값: raise SystemExit('명명 검사 Zeréck_VALUE 바뀐 C Quell: '+Wee)
    자바검사 = json.loads((Validatioun_Wee/'jvm/report.json').read_text())
    직접화면 = json.loads((Validatioun_Wee/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ausféieren_Befeel 시험 필요')
    Scheck_Byte_VALUE = json.loads((Validatioun_Wee/'naming/direct-bytecode.json').read_text())
    if not Scheck_Byte_VALUE['passed'] or Scheck_Byte_VALUE['jar_sha256'] != Hash_Fichier(projezéieren_Racinn/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 verifizéieren 필요')
    Scheck_Opléisung = json.loads((Validatioun_Wee/'resolution/report.json').read_text())
    Scheck_d_Gréisst_veränneren = json.loads((Validatioun_Wee/'resize/report.json').read_text())
    갱신검사 = json.loads((Validatioun_Wee/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != Kernel_Hash:
        raise SystemExit('현재 커널의 부분 aktualiséieren 시험 필요')
    for Wee, 기대값 in 갱신검사['source_sha256'].items():
        if Hash_Fichier(projezéieren_Racinn/Wee) != 기대값: raise SystemExit('부분 aktualiséieren 시험 Zeréck_VALUE 바뀐 Quell: '+Wee)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Laf Agab_Punkt 시험 필요')
    예제검사 = json.loads((Validatioun_Wee/'examples/report.json').read_text())
    if sorted(Scheck_d_Gréisst_veränneren['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 d_Gréisst_veränneren 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(Scheck_Opléisung['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 aktuell_Daten 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != Hash_Fichier(projezéieren_Racinn/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Zeréck_VALUE 라이브러리가 바뀌었습니다.')
    for Numm in ('한국어통신시험','한국어예외시험'):
        if not any(Agab_VALUE['name']==Numm and Agab_VALUE.get('openjdk_output_equal') for Agab_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Numm)
    예외들 = sorted(Wee.stem for Wee in (projezéieren_Racinn/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (Validatioun_Wee/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Numm in 예외들:
        if '\n'+Numm+'\n' not in 예외기록: raise SystemExit('예외 generéieren·잡기·설명 시험 필요: '+Numm)
    명세 = json.loads((projezéieren_Racinn/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != Hash_Fichier(projezéieren_Racinn/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 Bild_VALUE Hash_Fichier 불일치')
    with zipfile.ZipFile(str(projezéieren_Racinn/'dist/jkoros-native-rpi4-boot.zip')) as Bëndel:
        if hashlib.sha256(Bëndel.read('kernel8.img')).hexdigest() != Kernel_Hash:
            raise SystemExit('부팅 ZIP Kernel_VALUE 불일치')
        부팅설정 = Bëndel.read('config.txt')
        for Numm, d_Gréisst_veränneren in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Numm+'='+str(d_Gréisst_veränneren) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Astellungen 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(projezéieren_Racinn/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(projezéieren_Racinn/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if Hash_Fichier(복사본) != Kernel_Hash: raise SystemExit('SD Bild_VALUE Kernel_VALUE 불일치')
        Instanz_Astellungen = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(projezéieren_Racinn/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(Instanz_Astellungen)])
        if Instanz_Astellungen.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Astellungen 불일치')
    LOG_Rei = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': Kernel_Hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(Scheck_Opléisung['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Numm:Hash_Fichier(projezéieren_Racinn/'dist'/Numm) for Numm in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (Validatioun_Wee/'native-runtime-summary.json').write_text(json.dumps(LOG_Rei,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_Rei, 한국어 예외',len(예외들),'Klass_Definitioun, SD Bild_VALUE·ZIP 일치')

if __name__ == '__main__': Laf()
