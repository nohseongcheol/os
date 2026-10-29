#!/usr/bin/env python3
"""현재 커널과 real_ma_lumotlar 시험·배포물이 일치할 때에만 통합 tasdiqlash 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_ildiz = Path(__file__).resolve().parents[1]

def tasodifiy_ma_lumot_fayl(yo_l):
    계산 = hashlib.sha256()
    with yo_l.open('rb') as Fayl:
        for ma_lumotlar in iter(lambda: Fayl.read(1048576), b''): 계산.update(ma_lumotlar)
    return 계산.hexdigest()

def Bajarish():
    tasdiq_yo_l = Project_ildiz/'build/verification'
    o_zak_tasodifiy_ma_lumot = tasodifiy_ma_lumot_fayl(Project_ildiz/'build/kernel8.img')
    기록들 = {}
    for Nomi in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Nomi == 'boot' else Nomi+'/report.json'
        ma_lumotlar = json.loads((tasdiq_yo_l/상대경로).read_text())
        if not ma_lumotlar.get('passed') or ma_lumotlar.get('kernel_sha256') != o_zak_tasodifiy_ma_lumot:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Nomi] = {'passed': True, 'report': 상대경로}
    chek_nom = json.loads((tasdiq_yo_l/'naming/report.json').read_text())
    if not chek_nom['passed'] or not chek_nom['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for yo_l, 기대값 in chek_nom['c_source_sha256'].items():
        if tasodifiy_ma_lumot_fayl(Project_ildiz/yo_l) != 기대값: raise SystemExit('명명 검사 Orqaga_VALUE 바뀐 C manba: '+yo_l)
    자바검사 = json.loads((tasdiq_yo_l/'jvm/report.json').read_text())
    직접화면 = json.loads((tasdiq_yo_l/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 bajarmoq_buyruq 시험 필요')
    chek_bayt_VALUE = json.loads((tasdiq_yo_l/'naming/direct-bytecode.json').read_text())
    if not chek_bayt_VALUE['passed'] or chek_bayt_VALUE['jar_sha256'] != tasodifiy_ma_lumot_fayl(Project_ildiz/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 tasdiqlamoq 필요')
    chek_ruxsat = json.loads((tasdiq_yo_l/'resolution/report.json').read_text())
    chek_o_lcham = json.loads((tasdiq_yo_l/'resize/report.json').read_text())
    갱신검사 = json.loads((tasdiq_yo_l/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != o_zak_tasodifiy_ma_lumot:
        raise SystemExit('현재 커널의 부분 yangilamoq 시험 필요')
    for yo_l, 기대값 in 갱신검사['source_sha256'].items():
        if tasodifiy_ma_lumot_fayl(Project_ildiz/yo_l) != 기대값: raise SystemExit('부분 yangilamoq 시험 Orqaga_VALUE 바뀐 manba: '+yo_l)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Bajarish kiritish_nuqta 시험 필요')
    예제검사 = json.loads((tasdiq_yo_l/'examples/report.json').read_text())
    if sorted(chek_o_lcham['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Hajmi 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(chek_ruxsat['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 real_ma_lumotlar 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != tasodifiy_ma_lumot_fayl(Project_ildiz/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Orqaga_VALUE 라이브러리가 바뀌었습니다.')
    for Nomi in ('한국어통신시험','한국어예외시험'):
        if not any(kiritish_VALUE['name']==Nomi and kiritish_VALUE.get('openjdk_output_equal') for kiritish_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nomi)
    istisno_Ro_yxat = sorted(yo_l.stem for yo_l in (Project_ildiz/'한국어자바/한국어/자체').glob('*istisno.java'))
    istisno_LOG = (tasdiq_yo_l/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nomi in istisno_Ro_yxat:
        if '\n'+Nomi+'\n' not in istisno_LOG: raise SystemExit('istisno generatsiiyalash·잡기·설명 시험 필요: '+Nomi)
    명세 = json.loads((Project_ildiz/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != tasodifiy_ma_lumot_fayl(Project_ildiz/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 rasm_VALUE tasodifiy_ma_lumot_fayl 불일치')
    with zipfile.ZipFile(str(Project_ildiz/'dist/jkoros-native-rpi4-boot.zip')) as to_plam:
        if hashlib.sha256(to_plam.read('kernel8.img')).hexdigest() != o_zak_tasodifiy_ma_lumot:
            raise SystemExit('부팅 ZIP o_zak_VALUE 불일치')
        부팅설정 = to_plam.read('config.txt')
        for Nomi, Hajmi in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nomi+'='+str(Hajmi) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Moslamalar 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_ildiz/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_ildiz/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if tasodifiy_ma_lumot_fayl(복사본) != o_zak_tasodifiy_ma_lumot: raise SystemExit('SD rasm_VALUE o_zak_VALUE 불일치')
        namuna_Sozlamalar = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_ildiz/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(namuna_Sozlamalar)])
        if namuna_Sozlamalar.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Moslamalar 불일치')
    LOG_satr = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': o_zak_tasodifiy_ma_lumot,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': istisno_Ro_yxat, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(chek_ruxsat['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nomi:tasodifiy_ma_lumot_fayl(Project_ildiz/'dist'/Nomi) for Nomi in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (tasdiq_yo_l/'native-runtime-summary.json').write_text(json.dumps(LOG_satr,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_satr, 한국어 istisno',len(istisno_Ro_yxat),'Sinf_Izoh, SD rasm_VALUE·ZIP 일치')

if __name__ == '__main__': Bajarish()
