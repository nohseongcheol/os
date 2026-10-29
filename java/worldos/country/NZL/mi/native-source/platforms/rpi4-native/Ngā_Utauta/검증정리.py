#!/usr/bin/env python3
"""현재 커널과 tūturu_raraunga 시험·배포물이 일치할 때에만 통합 whakamana 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

whakaatu_pūtake = Path(__file__).resolve().parents[1]

def hash_kōnae(ara):
    계산 = hashlib.sha256()
    with ara.open('rb') as Kōnae:
        for raraunga in iter(lambda: Kōnae.read(1048576), b''): 계산.update(raraunga)
    return 계산.hexdigest()

def whakahaere():
    whakamana_ara = whakaatu_pūtake/'build/verification'
    kākano_hash = hash_kōnae(whakaatu_pūtake/'build/kernel8.img')
    기록들 = {}
    for Ingoa in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Ingoa == 'boot' else Ingoa+'/report.json'
        raraunga = json.loads((whakamana_ara/상대경로).read_text())
        if not raraunga.get('passed') or raraunga.get('kernel_sha256') != kākano_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Ingoa] = {'passed': True, 'report': 상대경로}
    taki_ingoa = json.loads((whakamana_ara/'naming/report.json').read_text())
    if not taki_ingoa['passed'] or not taki_ingoa['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ara, 기대값 in taki_ingoa['c_source_sha256'].items():
        if hash_kōnae(whakaatu_pūtake/ara) != 기대값: raise SystemExit('명명 검사 Hoki_uara 바뀐 C pūtake: '+ara)
    자바검사 = json.loads((whakamana_ara/'jvm/report.json').read_text())
    직접화면 = json.loads((whakamana_ara/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Reo_Māori 직접 화면 kawe_tono 시험 필요')
    taki_paita_uara = json.loads((whakamana_ara/'naming/direct-bytecode.json').read_text())
    if not taki_paita_uara['passed'] or taki_paita_uara['jar_sha256'] != hash_kōnae(whakaatu_pūtake/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Reo_Māori 라이브러리의 직접 호출 바이트코드 manatoko 필요')
    taki_taumira = json.loads((whakamana_ara/'resolution/report.json').read_text())
    taki_rahi = json.loads((whakamana_ara/'resize/report.json').read_text())
    갱신검사 = json.loads((whakamana_ara/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kākano_hash:
        raise SystemExit('현재 커널의 부분 tāmata 시험 필요')
    for ara, 기대값 in 갱신검사['source_sha256'].items():
        if hash_kōnae(whakaatu_pūtake/ara) != 기대값: raise SystemExit('부분 tāmata 시험 Hoki_uara 바뀐 pūtake: '+ara)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Reo_Māori 직접 가닥과 whakahaere tāurunga_ira 시험 필요')
    예제검사 = json.loads((whakamana_ara/'examples/report.json').read_text())
    if sorted(taki_rahi['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 rahi 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Reo_Māori Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(taki_taumira['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 tūturu_raraunga 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_kōnae(whakaatu_pūtake/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Hoki_uara 라이브러리가 바뀌었습니다.')
    for Ingoa in ('한국어통신시험','한국어예외시험'):
        if not any(tāurunga_uara['name']==Ingoa and tāurunga_uara.get('openjdk_output_equal') for tāurunga_uara in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ingoa)
    예외들 = sorted(ara.stem for ara in (whakaatu_pūtake/'한국어자바/Reo_Māori/자체').glob('*예외.java'))
    예외기록 = (whakamana_ara/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ingoa in 예외들:
        if '\n'+Ingoa+'\n' not in 예외기록: raise SystemExit('예외 waihanga·잡기·설명 시험 필요: '+Ingoa)
    명세 = json.loads((whakaatu_pūtake/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_kōnae(whakaatu_pūtake/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_uara hash_kōnae 불일치')
    with zipfile.ZipFile(str(whakaatu_pūtake/'dist/jkoros-native-rpi4-boot.zip')) as pūpū:
        if hashlib.sha256(pūpū.read('kernel8.img')).hexdigest() != kākano_hash:
            raise SystemExit('부팅 ZIP kākano_uara_0611a8a8 불일치')
        부팅설정 = pūpū.read('config.txt')
        for Ingoa, rahi in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ingoa+'='+str(rahi) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Ngā_Tautuhinga 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(whakaatu_pūtake/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(whakaatu_pūtake/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_kōnae(복사본) != kākano_hash: raise SystemExit('SD IMAGE_uara kākano_uara_0611a8a8 불일치')
        tārua_Ngā_Tautuhinga = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(whakaatu_pūtake/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(tārua_Ngā_Tautuhinga)])
        if tārua_Ngā_Tautuhinga.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Ngā_Tautuhinga 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kākano_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(taki_taumira['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ingoa:hash_kōnae(whakaatu_pūtake/'dist'/Ingoa) for Ingoa in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (whakamana_ara/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_RECORD, Reo_Māori 예외',len(예외들),'tauaha_Whakamāramatanga, SD IMAGE_uara·ZIP 일치')

if __name__ == '__main__': whakahaere()
