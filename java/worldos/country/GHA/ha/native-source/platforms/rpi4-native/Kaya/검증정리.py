#!/usr/bin/env python3
"""현재 커널과 Na_hakika_Tarin_bayani 시험·배포물이 일치할 때에만 통합 inganta 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def hash_Fayil(Hanyar_shiga):
    계산 = hashlib.sha256()
    with Hanyar_shiga.open('rb') as Fayil:
        for Tarin_bayani in iter(lambda: Fayil.read(1048576), b''): 계산.update(Tarin_bayani)
    return 계산.hexdigest()

def Tafiyar_da():
    amincewa_Hanyar_shiga = 기준/'build/verification'
    Kwara_hash = hash_Fayil(기준/'build/kernel8.img')
    기록들 = {}
    for Suna in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Suna == 'boot' else Suna+'/report.json'
        Tarin_bayani = json.loads((amincewa_Hanyar_shiga/상대경로).read_text())
        if not Tarin_bayani.get('passed') or Tarin_bayani.get('kernel_sha256') != Kwara_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Suna] = {'passed': True, 'report': 상대경로}
    Bincika_Suna = json.loads((amincewa_Hanyar_shiga/'naming/report.json').read_text())
    if not Bincika_Suna['passed'] or not Bincika_Suna['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Hanyar_shiga, 기대값 in Bincika_Suna['c_source_sha256'].items():
        if hash_Fayil(기준/Hanyar_shiga) != 기대값: raise SystemExit('명명 검사 Baya_Daraja 바뀐 C tushe: '+Hanyar_shiga)
    자바검사 = json.loads((amincewa_Hanyar_shiga/'jvm/report.json').read_text())
    직접화면 = json.loads((amincewa_Hanyar_shiga/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 gudanar_Umarni 시험 필요')
    Bincika_bayit_Daraja = json.loads((amincewa_Hanyar_shiga/'naming/direct-bytecode.json').read_text())
    if not Bincika_bayit_Daraja['passed'] or Bincika_bayit_Daraja['jar_sha256'] != hash_Fayil(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 Tabbatar_da 필요')
    Bincika_Kyawon_tarkacen_hoto = json.loads((amincewa_Hanyar_shiga/'resolution/report.json').read_text())
    Bincika_girma = json.loads((amincewa_Hanyar_shiga/'resize/report.json').read_text())
    갱신검사 = json.loads((amincewa_Hanyar_shiga/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != Kwara_hash:
        raise SystemExit('현재 커널의 부분 Wartsakewa 시험 필요')
    for Hanyar_shiga, 기대값 in 갱신검사['source_sha256'].items():
        if hash_Fayil(기준/Hanyar_shiga) != 기대값: raise SystemExit('부분 Wartsakewa 시험 Baya_Daraja 바뀐 tushe: '+Hanyar_shiga)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Tafiyar_da Mashigar_bayanai_maki 시험 필요')
    예제검사 = json.loads((amincewa_Hanyar_shiga/'examples/report.json').read_text())
    if sorted(Bincika_girma['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Girma 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(Bincika_Kyawon_tarkacen_hoto['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 Na_hakika_Tarin_bayani 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_Fayil(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Baya_Daraja 라이브러리가 바뀌었습니다.')
    for Suna in ('한국어통신시험','한국어예외시험'):
        if not any(Mashigar_bayanai_Daraja['name']==Suna and Mashigar_bayanai_Daraja.get('openjdk_output_equal') for Mashigar_bayanai_Daraja in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Suna)
    banbanchi_Jeri = sorted(Hanyar_shiga.stem for Hanyar_shiga in (기준/'한국어자바/한국어/자체').glob('*banbanchi.java'))
    banbanchi_logu = (amincewa_Hanyar_shiga/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Suna in banbanchi_Jeri:
        if '\n'+Suna+'\n' not in banbanchi_logu: raise SystemExit('banbanchi 생성·잡기·설명 시험 필요: '+Suna)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_Fayil(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 Hoto_Daraja hash_Fayil 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as dami:
        if hashlib.sha256(dami.read('kernel8.img')).hexdigest() != Kwara_hash:
            raise SystemExit('부팅 ZIP Kwara_Daraja 불일치')
        부팅설정 = dami.read('config.txt')
        for Suna, Girma in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Suna+'='+str(Girma) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Saituna 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_Fayil(복사본) != Kwara_hash: raise SystemExit('SD Hoto_Daraja Kwara_Daraja 불일치')
        Kwafi_Saituna = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(Kwafi_Saituna)])
        if Kwafi_Saituna.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Saituna 불일치')
    logu_naɗa = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': Kwara_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': banbanchi_Jeri, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(Bincika_Kyawon_tarkacen_hoto['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Suna:hash_Fayil(기준/'dist'/Suna) for Suna in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (amincewa_Hanyar_shiga/'native-runtime-summary.json').write_text(json.dumps(logu_naɗa,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 logu_naɗa, 한국어 banbanchi',len(banbanchi_Jeri),'Aji_Ma_ana, SD Hoto_Daraja·ZIP 일치')

if __name__ == '__main__': Tafiyar_da()
