#!/usr/bin/env python3
"""tähtaja_piires_kaup 커널과 tegelik_andmed 시험·배포물이 일치할 때에만 통합 valideerima 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_juur = Path(__file__).resolve().parents[1]

def räsikood_Fail(RADA):
    계산 = hashlib.sha256()
    with RADA.open('rb') as Fail:
        for andmed in iter(lambda: Fail.read(1048576), b''): 계산.update(andmed)
    return 계산.hexdigest()

def Käivita_2():
    kinnitamine_tee = Project_juur/'build/verification'
    tuum_räsikood = räsikood_Fail(Project_juur/'build/kernel8.img')
    기록들 = {}
    for Nimi_2 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        suhteline_tee = 'report.json' if Nimi_2 == 'boot' else Nimi_2+'/report.json'
        andmed = json.loads((kinnitamine_tee/suhteline_tee).read_text())
        if not andmed.get('passed') or andmed.get('kernel_sha256') != tuum_räsikood:
            raise SystemExit('tähtaja_piires_kaup 커널에 대한 성공 기록이 필요합니다: '+suhteline_tee)
        기록들[Nimi_2] = {'passed': True, 'report': suhteline_tee}
    tšekk_nimetus = json.loads((kinnitamine_tee/'naming/report.json').read_text())
    if not tšekk_nimetus['passed'] or not tšekk_nimetus['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for RADA, 기대값 in tšekk_nimetus['c_source_sha256'].items():
        if räsikood_Fail(Project_juur/RADA) != 기대값: raise SystemExit('명명 검사 Tagasi_VALUE 바뀐 C ALLIKAS: '+RADA)
    자바검사 = json.loads((kinnitamine_tee/'jvm/report.json').read_text())
    직접화면 = json.loads((kinnitamine_tee/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Eesti 직접 화면 Täida_käsk 시험 필요')
    tšekk_bait_VALUE = json.loads((kinnitamine_tee/'naming/direct-bytecode.json').read_text())
    if not tšekk_bait_VALUE['passed'] or tšekk_bait_VALUE['jar_sha256'] != räsikood_Fail(Project_juur/'dist/jkoros-native-korean.jar'):
        raise SystemExit('tähtaja_piires_kaup Eesti 라이브러리의 직접 호출 바이트코드 kinnitama 필요')
    tšekk_eraldusvõime = json.loads((kinnitamine_tee/'resolution/report.json').read_text())
    tšekk_suurust_muutma = json.loads((kinnitamine_tee/'resize/report.json').read_text())
    갱신검사 = json.loads((kinnitamine_tee/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != tuum_räsikood:
        raise SystemExit('tähtaja_piires_kaup 커널의 부분 värskendama 시험 필요')
    for RADA, 기대값 in 갱신검사['source_sha256'].items():
        if räsikood_Fail(Project_juur/RADA) != 기대값: raise SystemExit('부분 värskendama 시험 Tagasi_VALUE 바뀐 ALLIKAS: '+RADA)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Eesti 직접 가닥과 Käivita_2 kirje_p 시험 필요')
    예제검사 = json.loads((kinnitamine_tee/'examples/report.json').read_text())
    if sorted(tšekk_suurust_muutma['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Suurus 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Eesti Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(tšekk_eraldusvõime['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 tegelik_andmed 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != räsikood_Fail(Project_juur/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Tagasi_VALUE 라이브러리가 바뀌었습니다.')
    for Nimi_2 in ('한국어통신시험','한국어예외시험'):
        if not any(kirje_VALUE['name']==Nimi_2 and kirje_VALUE.get('openjdk_output_equal') for kirje_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nimi_2)
    erand_Loend = sorted(RADA.stem for RADA in (Project_juur/'한국어자바/Eesti/oma').glob('*erand.java'))
    erand_LOG = (kinnitamine_tee/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nimi_2 in erand_Loend:
        if '\n'+Nimi_2+'\n' not in erand_LOG: raise SystemExit('erand genereerima·잡기·설명 시험 필요: '+Nimi_2)
    명세 = json.loads((Project_juur/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != räsikood_Fail(Project_juur/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('turustus_VALUE pilt_VALUE räsikood_Fail 불일치')
    with zipfile.ZipFile(str(Project_juur/'dist/jkoros-native-rpi4-boot.zip')) as kogum:
        if hashlib.sha256(kogum.read('kernel8.img')).hexdigest() != tuum_räsikood:
            raise SystemExit('부팅 ZIP tuum_VALUE 불일치')
        부팅설정 = kogum.read('config.txt')
        for Nimi_2, Suurus in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nimi_2+'='+str(Suurus) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Seaded 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_juur/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_juur/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if räsikood_Fail(복사본) != tuum_räsikood: raise SystemExit('SD pilt_VALUE tuum_VALUE 불일치')
        eksemplar_Sätted = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_juur/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(eksemplar_Sätted)])
        if eksemplar_Sätted.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Seaded 불일치')
    LOG_kirje = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': tuum_räsikood,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': erand_Loend, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(tšekk_eraldusvõime['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nimi_2:räsikood_Fail(Project_juur/'dist'/Nimi_2) for Nimi_2 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (kinnitamine_tee/'native-runtime-summary.json').write_text(json.dumps(LOG_kirje,ensure_ascii=False,indent=2)+'\n')
    print('PASS: tähtaja_piires_kaup 커널의',len(기록들),'개 통합 시험 LOG_kirje, Eesti erand',len(erand_Loend),'tund_Sõnaseletus, SD pilt_VALUE·ZIP 일치')

if __name__ == '__main__': Käivita_2()
