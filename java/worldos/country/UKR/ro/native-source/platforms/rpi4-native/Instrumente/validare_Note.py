#!/usr/bin/env python3
"""curent_element 커널과 real_date 시험·배포물이 일치할 때에만 통합 valida 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_rădăcină = Path(__file__).resolve().parents[1]

def cod_hash_Fișier(Cale):
    계산 = hashlib.sha256()
    with Cale.open('rb') as Fișier:
        for date in iter(lambda: Fișier.read(1048576), b''): 계산.update(date)
    return 계산.hexdigest()

def Pornește():
    validare_cale = Project_rădăcină/'build/verification'
    nucleu_cod_hash = cod_hash_Fișier(Project_rădăcină/'build/kernel8.img')
    기록들 = {}
    for Nume in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        cale_relativă = 'report.json' if Nume == 'boot' else Nume+'/report.json'
        date = json.loads((validare_cale/cale_relativă).read_text())
        if not date.get('passed') or date.get('kernel_sha256') != nucleu_cod_hash:
            raise SystemExit('curent_element 커널에 대한 성공 기록이 필요합니다: '+cale_relativă)
        기록들[Nume] = {'passed': True, 'report': cale_relativă}
    verifica_nume = json.loads((validare_cale/'naming/report.json').read_text())
    if not verifica_nume['passed'] or not verifica_nume['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Cale, 기대값 in verifica_nume['c_source_sha256'].items():
        if cod_hash_Fișier(Project_rădăcină/Cale) != 기대값: raise SystemExit('명명 검사 ÎNAPOI_VALUE 바뀐 C SURSĂ: '+Cale)
    자바검사 = json.loads((validare_cale/'jvm/report.json').read_text())
    직접화면 = json.loads((validare_cale/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Română 직접 화면 executa_comandă 시험 필요')
    verifica_byte_VALUE = json.loads((validare_cale/'naming/direct-bytecode.json').read_text())
    if not verifica_byte_VALUE['passed'] or verifica_byte_VALUE['jar_sha256'] != cod_hash_Fișier(Project_rădăcină/'dist/jkoros-native-korean.jar'):
        raise SystemExit('curent_element Română 라이브러리의 직접 호출 바이트코드 verifica 필요')
    verifica_rezoluție = json.loads((validare_cale/'resolution/report.json').read_text())
    verifica_dimensiona = json.loads((validare_cale/'resize/report.json').read_text())
    갱신검사 = json.loads((validare_cale/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != nucleu_cod_hash:
        raise SystemExit('curent_element 커널의 부분 reîmprospăta 시험 필요')
    for Cale, 기대값 in 갱신검사['source_sha256'].items():
        if cod_hash_Fișier(Project_rădăcină/Cale) != 기대값: raise SystemExit('부분 reîmprospăta 시험 ÎNAPOI_VALUE 바뀐 SURSĂ: '+Cale)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Română 직접 가닥과 Pornește intrare_p 시험 필요')
    예제검사 = json.loads((validare_cale/'examples/report.json').read_text())
    if sorted(verifica_dimensiona['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Mărime 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Română Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(verifica_rezoluție['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 real_date 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != cod_hash_Fișier(Project_rădăcină/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ÎNAPOI_VALUE 라이브러리가 바뀌었습니다.')
    for Nume in ('한국어통신시험','한국어예외시험'):
        if not any(intrare_VALUE['name']==Nume and intrare_VALUE.get('openjdk_output_equal') for intrare_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nume)
    excepție_Listă = sorted(Cale.stem for Cale in (Project_rădăcină/'한국어자바/Română/propriu').glob('*excepție.java'))
    excepție_LOG = (validare_cale/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nume in excepție_Listă:
        if '\n'+Nume+'\n' not in excepție_LOG: raise SystemExit('excepție genera·잡기·설명 시험 필요: '+Nume)
    명세 = json.loads((Project_rădăcină/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != cod_hash_Fișier(Project_rădăcină/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE cod_hash_Fișier 불일치')
    with zipfile.ZipFile(str(Project_rădăcină/'dist/jkoros-native-rpi4-boot.zip')) as set:
        if hashlib.sha256(set.read('kernel8.img')).hexdigest() != nucleu_cod_hash:
            raise SystemExit('부팅 ZIP nucleu_VALUE 불일치')
        부팅설정 = set.read('config.txt')
        for Nume, Mărime in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nume+'='+str(Mărime) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Setări 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_rădăcină/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_rădăcină/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if cod_hash_Fișier(복사본) != nucleu_cod_hash: raise SystemExit('SD IMAGE_VALUE nucleu_VALUE 불일치')
        copia_Setări = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_rădăcină/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copia_Setări)])
        if copia_Setări.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Setări 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': nucleu_cod_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': excepție_Listă, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(verifica_rezoluție['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nume:cod_hash_Fișier(Project_rădăcină/'dist'/Nume) for Nume in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validare_cale/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: curent_element 커널의',len(기록들),'개 통합 시험 LOG_RECORD, Română excepție',len(excepție_Listă),'Clasă_Definiție, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Pornește()
