#!/usr/bin/env python3
"""현재 커널과 dearbh_dàta 시험·배포물이 일치할 때에만 통합 dearbh_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

tilg_freumh = Path(__file__).resolve().parents[1]

def hais_faidhle(Slighe):
    계산 = hashlib.sha256()
    with Slighe.open('rb') as faidhle:
        for dàta in iter(lambda: faidhle.read(1048576), b''): 계산.update(dàta)
    return 계산.hexdigest()

def ruith():
    dearbhadh_slighe = tilg_freumh/'build/verification'
    eitean_hais = hais_faidhle(tilg_freumh/'build/kernel8.img')
    기록들 = {}
    for Ainm in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Ainm == 'boot' else Ainm+'/report.json'
        dàta = json.loads((dearbhadh_slighe/상대경로).read_text())
        if not dàta.get('passed') or dàta.get('kernel_sha256') != eitean_hais:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Ainm] = {'passed': True, 'report': 상대경로}
    seic_ainm = json.loads((dearbhadh_slighe/'naming/report.json').read_text())
    if not seic_ainm['passed'] or not seic_ainm['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Slighe, 기대값 in seic_ainm['c_source_sha256'].items():
        if hais_faidhle(tilg_freumh/Slighe) != 기대값: raise SystemExit('명명 검사 Air_ais_VALUE 바뀐 C tùs: '+Slighe)
    자바검사 = json.loads((dearbhadh_slighe/'jvm/report.json').read_text())
    직접화면 = json.loads((dearbhadh_slighe/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 gnìomhaich_àithne 시험 필요')
    seic_baidht_VALUE = json.loads((dearbhadh_slighe/'naming/direct-bytecode.json').read_text())
    if not seic_baidht_VALUE['passed'] or seic_baidht_VALUE['jar_sha256'] != hais_faidhle(tilg_freumh/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 dearbh 필요')
    seic_dùmhlachd_bhreacaidh = json.loads((dearbhadh_slighe/'resolution/report.json').read_text())
    seic_atharraich_am_meud = json.loads((dearbhadh_slighe/'resize/report.json').read_text())
    갱신검사 = json.loads((dearbhadh_slighe/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != eitean_hais:
        raise SystemExit('현재 커널의 부분 ath_nuadhaich 시험 필요')
    for Slighe, 기대값 in 갱신검사['source_sha256'].items():
        if hais_faidhle(tilg_freumh/Slighe) != 기대값: raise SystemExit('부분 ath_nuadhaich 시험 Air_ais_VALUE 바뀐 tùs: '+Slighe)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ruith cur_a_steach_puing 시험 필요')
    예제검사 = json.loads((dearbhadh_slighe/'examples/report.json').read_text())
    if sorted(seic_atharraich_am_meud['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 atharraich_am_meud 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(seic_dùmhlachd_bhreacaidh['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 dearbh_dàta 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hais_faidhle(tilg_freumh/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Air_ais_VALUE 라이브러리가 바뀌었습니다.')
    for Ainm in ('한국어통신시험','한국어예외시험'):
        if not any(cur_a_steach_VALUE['name']==Ainm and cur_a_steach_VALUE.get('openjdk_output_equal') for cur_a_steach_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ainm)
    예외들 = sorted(Slighe.stem for Slighe in (tilg_freumh/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (dearbhadh_slighe/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ainm in 예외들:
        if '\n'+Ainm+'\n' not in 예외기록: raise SystemExit('예외 gin·잡기·설명 시험 필요: '+Ainm)
    명세 = json.loads((tilg_freumh/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hais_faidhle(tilg_freumh/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hais_faidhle 불일치')
    with zipfile.ZipFile(str(tilg_freumh/'dist/jkoros-native-rpi4-boot.zip')) as trusgan:
        if hashlib.sha256(trusgan.read('kernel8.img')).hexdigest() != eitean_hais:
            raise SystemExit('부팅 ZIP eitean_VALUE 불일치')
        부팅설정 = trusgan.read('config.txt')
        for Ainm, atharraich_am_meud in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ainm+'='+str(atharraich_am_meud) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 roghainnean 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(tilg_freumh/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(tilg_freumh/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hais_faidhle(복사본) != eitean_hais: raise SystemExit('SD IMAGE_VALUE eitean_VALUE 불일치')
        ionstans_roghainnean = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(tilg_freumh/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ionstans_roghainnean)])
        if ionstans_roghainnean.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 roghainnean 불일치')
    LOG_ràgh = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': eitean_hais,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(seic_dùmhlachd_bhreacaidh['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ainm:hais_faidhle(tilg_freumh/'dist'/Ainm) for Ainm in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (dearbhadh_slighe/'native-runtime-summary.json').write_text(json.dumps(LOG_ràgh,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_ràgh, 한국어 예외',len(예외들),'clas_deifinisean, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': ruith()
