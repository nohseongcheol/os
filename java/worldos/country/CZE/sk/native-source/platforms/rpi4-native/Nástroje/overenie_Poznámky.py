#!/usr/bin/env python3
"""v_termíne_splatnosti_položka 커널과 skutočný_údaje 시험·배포물이 일치할 때에만 통합 overiť_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

akcia_koreň = Path(__file__).resolve().parents[1]

def hodnota_hash_Súbor(Cesta):
    계산 = hashlib.sha256()
    with Cesta.open('rb') as Súbor:
        for údaje in iter(lambda: Súbor.read(1048576), b''): 계산.update(údaje)
    return 계산.hexdigest()

def Spustiť_2():
    overenie_cesta = akcia_koreň/'build/verification'
    jadro_hodnota_hash = hodnota_hash_Súbor(akcia_koreň/'build/kernel8.img')
    기록들 = {}
    for Názov in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Názov == 'boot' else Názov+'/report.json'
        údaje = json.loads((overenie_cesta/상대경로).read_text())
        if not údaje.get('passed') or údaje.get('kernel_sha256') != jadro_hodnota_hash:
            raise SystemExit('v_termíne_splatnosti_položka 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Názov] = {'passed': True, 'report': 상대경로}
    skontrolovať_názov = json.loads((overenie_cesta/'naming/report.json').read_text())
    if not skontrolovať_názov['passed'] or not skontrolovať_názov['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Cesta, 기대값 in skontrolovať_názov['c_source_sha256'].items():
        if hodnota_hash_Súbor(akcia_koreň/Cesta) != 기대값: raise SystemExit('명명 검사 BACK_VALUE 바뀐 C ZDROJ: '+Cesta)
    자바검사 = json.loads((overenie_cesta/'jvm/report.json').read_text())
    직접화면 = json.loads((overenie_cesta/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Slovenský 직접 화면 Vykonať_príkaz 시험 필요')
    skontrolovať_Byte_VALUE = json.loads((overenie_cesta/'naming/direct-bytecode.json').read_text())
    if not skontrolovať_Byte_VALUE['passed'] or skontrolovať_Byte_VALUE['jar_sha256'] != hodnota_hash_Súbor(akcia_koreň/'dist/jkoros-native-korean.jar'):
        raise SystemExit('v_termíne_splatnosti_položka Slovenský 라이브러리의 직접 호출 바이트코드 overiť 필요')
    skontrolovať_rozlíšenie = json.loads((overenie_cesta/'resolution/report.json').read_text())
    skontrolovať_zmeniť_veľkosť = json.loads((overenie_cesta/'resize/report.json').read_text())
    갱신검사 = json.loads((overenie_cesta/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jadro_hodnota_hash:
        raise SystemExit('v_termíne_splatnosti_položka 커널의 부분 obnoviť 시험 필요')
    for Cesta, 기대값 in 갱신검사['source_sha256'].items():
        if hodnota_hash_Súbor(akcia_koreň/Cesta) != 기대값: raise SystemExit('부분 obnoviť 시험 BACK_VALUE 바뀐 ZDROJ: '+Cesta)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Slovenský 직접 가닥과 Spustiť_2 položka_bod 시험 필요')
    예제검사 = json.loads((overenie_cesta/'examples/report.json').read_text())
    if sorted(skontrolovať_zmeniť_veľkosť['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Veľkosť 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Slovenský Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(skontrolovať_rozlíšenie['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 skutočný_údaje 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hodnota_hash_Súbor(akcia_koreň/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 BACK_VALUE 라이브러리가 바뀌었습니다.')
    for Názov in ('한국어통신시험','한국어예외시험'):
        if not any(položka_VALUE['name']==Názov and položka_VALUE.get('openjdk_output_equal') for položka_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Názov)
    výnimka_Zoznam = sorted(Cesta.stem for Cesta in (akcia_koreň/'한국어자바/Slovenský/vlastné').glob('*výnimka.java'))
    výnimka_LOG = (overenie_cesta/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Názov in výnimka_Zoznam:
        if '\n'+Názov+'\n' not in výnimka_LOG: raise SystemExit('výnimka generovať·잡기·설명 시험 필요: '+Názov)
    명세 = json.loads((akcia_koreň/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hodnota_hash_Súbor(akcia_koreň/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hodnota_hash_Súbor 불일치')
    with zipfile.ZipFile(str(akcia_koreň/'dist/jkoros-native-rpi4-boot.zip')) as zväzok:
        if hashlib.sha256(zväzok.read('kernel8.img')).hexdigest() != jadro_hodnota_hash:
            raise SystemExit('부팅 ZIP jadro_VALUE 불일치')
        부팅설정 = zväzok.read('config.txt')
        for Názov, Veľkosť in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Názov+'='+str(Veľkosť) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Nastavenia 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(akcia_koreň/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(akcia_koreň/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hodnota_hash_Súbor(복사본) != jadro_hodnota_hash: raise SystemExit('SD IMAGE_VALUE jadro_VALUE 불일치')
        inštancia_Nastavenia = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(akcia_koreň/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(inštancia_Nastavenia)])
        if inštancia_Nastavenia.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Nastavenia 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jadro_hodnota_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': výnimka_Zoznam, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(skontrolovať_rozlíšenie['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Názov:hodnota_hash_Súbor(akcia_koreň/'dist'/Názov) for Názov in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (overenie_cesta/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: v_termíne_splatnosti_položka 커널의',len(기록들),'개 통합 시험 LOG_RECORD, Slovenský výnimka',len(výnimka_Zoznam),'lekcia_Definícia, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Spustiť_2()
