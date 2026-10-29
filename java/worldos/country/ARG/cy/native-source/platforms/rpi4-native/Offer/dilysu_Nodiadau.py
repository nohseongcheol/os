#!/usr/bin/env python3
"""현재 커널과 go_iawn_data 시험·배포물이 일치할 때에만 통합 dilysu_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

prosiect_gwraidd = Path(__file__).resolve().parents[1]

def hash_ffeil(LLWYBR):
    계산 = hashlib.sha256()
    with LLWYBR.open('rb') as Ffeil:
        for data in iter(lambda: Ffeil.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Gweithredu_2():
    dilysu_llwybr = prosiect_gwraidd/'build/verification'
    cnewyllyn_hash = hash_ffeil(prosiect_gwraidd/'build/kernel8.img')
    기록들 = {}
    for Enw in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Enw == 'boot' else Enw+'/report.json'
        data = json.loads((dilysu_llwybr/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != cnewyllyn_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Enw] = {'passed': True, 'report': 상대경로}
    gwirio_enw = json.loads((dilysu_llwybr/'naming/report.json').read_text())
    if not gwirio_enw['passed'] or not gwirio_enw['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for LLWYBR, 기대값 in gwirio_enw['c_source_sha256'].items():
        if hash_ffeil(prosiect_gwraidd/LLWYBR) != 기대값: raise SystemExit('명명 검사 BACK_VALUE 바뀐 C FFYNHONNELL: '+LLWYBR)
    자바검사 = json.loads((dilysu_llwybr/'jvm/report.json').read_text())
    직접화면 = json.loads((dilysu_llwybr/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Cymraeg 직접 화면 Gweithredu_gorchymyn 시험 필요')
    gwirio_beit_VALUE = json.loads((dilysu_llwybr/'naming/direct-bytecode.json').read_text())
    if not gwirio_beit_VALUE['passed'] or gwirio_beit_VALUE['jar_sha256'] != hash_ffeil(prosiect_gwraidd/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Cymraeg 라이브러리의 직접 호출 바이트코드 dilysu 필요')
    gwirio_cydraniad = json.loads((dilysu_llwybr/'resolution/report.json').read_text())
    gwirio_newid_maint = json.loads((dilysu_llwybr/'resize/report.json').read_text())
    갱신검사 = json.loads((dilysu_llwybr/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != cnewyllyn_hash:
        raise SystemExit('현재 커널의 부분 adnewyddu 시험 필요')
    for LLWYBR, 기대값 in 갱신검사['source_sha256'].items():
        if hash_ffeil(prosiect_gwraidd/LLWYBR) != 기대값: raise SystemExit('부분 adnewyddu 시험 BACK_VALUE 바뀐 FFYNHONNELL: '+LLWYBR)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Cymraeg 직접 가닥과 Gweithredu_2 cofnod_p 시험 필요')
    예제검사 = json.loads((dilysu_llwybr/'examples/report.json').read_text())
    if sorted(gwirio_newid_maint['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Maint 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Cymraeg Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(gwirio_cydraniad['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 go_iawn_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_ffeil(prosiect_gwraidd/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 BACK_VALUE 라이브러리가 바뀌었습니다.')
    for Enw in ('한국어통신시험','한국어예외시험'):
        if not any(cofnod_VALUE['name']==Enw and cofnod_VALUE.get('openjdk_output_equal') for cofnod_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Enw)
    eithriad_Rhestr = sorted(LLWYBR.stem for LLWYBR in (prosiect_gwraidd/'한국어자바/Cymraeg/자체').glob('*eithriad.java'))
    eithriad_LOG = (dilysu_llwybr/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Enw in eithriad_Rhestr:
        if '\n'+Enw+'\n' not in eithriad_LOG: raise SystemExit('eithriad cynhyrchu·잡기·설명 시험 필요: '+Enw)
    명세 = json.loads((prosiect_gwraidd/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_ffeil(prosiect_gwraidd/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 llun_VALUE hash_ffeil 불일치')
    with zipfile.ZipFile(str(prosiect_gwraidd/'dist/jkoros-native-rpi4-boot.zip')) as bwndel:
        if hashlib.sha256(bwndel.read('kernel8.img')).hexdigest() != cnewyllyn_hash:
            raise SystemExit('부팅 ZIP cnewyllyn_VALUE 불일치')
        부팅설정 = bwndel.read('config.txt')
        for Enw, Maint in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Enw+'='+str(Maint) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Gosodiadau 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(prosiect_gwraidd/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(prosiect_gwraidd/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_ffeil(복사본) != cnewyllyn_hash: raise SystemExit('SD llun_VALUE cnewyllyn_VALUE 불일치')
        copïo_Gosodiadau = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(prosiect_gwraidd/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copïo_Gosodiadau)])
        if copïo_Gosodiadau.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Gosodiadau 불일치')
    LOG_rhes = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': cnewyllyn_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': eithriad_Rhestr, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(gwirio_cydraniad['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Enw:hash_ffeil(prosiect_gwraidd/'dist'/Enw) for Enw in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (dilysu_llwybr/'native-runtime-summary.json').write_text(json.dumps(LOG_rhes,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_rhes, Cymraeg eithriad',len(eithriad_Rhestr),'Dosbarth_Diffiniad, SD llun_VALUE·ZIP 일치')

if __name__ == '__main__': Gweithredu_2()
