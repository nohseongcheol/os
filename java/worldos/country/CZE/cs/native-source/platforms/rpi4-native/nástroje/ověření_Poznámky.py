#!/usr/bin/env python3
"""dobrá_zboží 커널과 skutečný_data zkoušky·배포물이 일치할 때에만 통합 ověřit_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

akce_kořen = Path(__file__).resolve().parents[1]

def hodnota_hash_Soubor(cesta_2):
    계산 = hashlib.sha256()
    with cesta_2.open('rb') as název_souboru:
        for data in iter(lambda: název_souboru.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Spustit_2():
    ověření_cesta = akce_kořen/'build/verification'
    jádro_hodnota_hash = hodnota_hash_Soubor(akce_kořen/'build/kernel8.img')
    기록들 = {}
    for Název in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativní_cesta = 'report.json' if Název == 'boot' else Název+'/report.json'
        data = json.loads((ověření_cesta/relativní_cesta).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != jádro_hodnota_hash:
            raise SystemExit('dobrá_zboží 커널에 대한 성공 기록이 필요합니다: '+relativní_cesta)
        기록들[Název] = {'passed': True, 'report': relativní_cesta}
    šek_název = json.loads((ověření_cesta/'naming/report.json').read_text())
    if not šek_název['passed'] or not šek_název['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for cesta_2, 기대값 in šek_název['c_source_sha256'].items():
        if hodnota_hash_Soubor(akce_kořen/cesta_2) != 기대값: raise SystemExit('명명 검사 BACK_HODNOTA 바뀐 C zdrojový_soubor: '+cesta_2)
    자바검사 = json.loads((ověření_cesta/'jvm/report.json').read_text())
    직접화면 = json.loads((ověření_cesta/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('čeština 직접 화면 Provést_příkaz zkoušky 필요')
    šek_bajt_HODNOTA = json.loads((ověření_cesta/'naming/direct-bytecode.json').read_text())
    if not šek_bajt_HODNOTA['passed'] or šek_bajt_HODNOTA['jar_sha256'] != hodnota_hash_Soubor(akce_kořen/'dist/jkoros-native-korean.jar'):
        raise SystemExit('dobrá_zboží čeština 라이브러리의 직접 호출 바이트코드 ověřit 필요')
    šek_řešení = json.loads((ověření_cesta/'resolution/report.json').read_text())
    šek_změnit_velikost = json.loads((ověření_cesta/'resize/report.json').read_text())
    갱신검사 = json.loads((ověření_cesta/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jádro_hodnota_hash:
        raise SystemExit('dobrá_zboží 커널의 부분 aktualizovat zkoušky 필요')
    for cesta_2, 기대값 in 갱신검사['source_sha256'].items():
        if hodnota_hash_Soubor(akce_kořen/cesta_2) != 기대값: raise SystemExit('부분 aktualizovat zkoušky BACK_HODNOTA 바뀐 zdrojový_soubor: '+cesta_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('čeština 직접 가닥과 Spustit_2 vstupní_bod zkoušky 필요')
    예제검사 = json.loads((ověření_cesta/'examples/report.json').read_text())
    if sorted(šek_změnit_velikost['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Velikost 조절 zkoušky 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('čeština Swing 창을 포함한 예제 13개 zkoušky 필요')
    if sorted(šek_řešení['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 skutečný_data 화면 zkoušky 필요')
    if 자바검사['korean_library_sha256'] != hodnota_hash_Soubor(akce_kořen/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 zkoušky BACK_HODNOTA 라이브러리가 바뀌었습니다.')
    for Název in ('한국어통신시험','한국어예외시험'):
        if not any(položka_HODNOTA['name']==Název and položka_HODNOTA.get('openjdk_output_equal') for položka_HODNOTA in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 zkoušky 필요: '+Název)
    výjimka_Seznam = sorted(cesta_2.stem for cesta_2 in (akce_kořen/'한국어자바/čeština/vlastní').glob('*výjimka.java'))
    výjimka_LOGZ = (ověření_cesta/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Název in výjimka_Seznam:
        if '\n'+Název+'\n' not in výjimka_LOGZ: raise SystemExit('výjimka generovat·잡기·설명 zkoušky 필요: '+Název)
    명세 = json.loads((akce_kořen/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hodnota_hash_Soubor(akce_kořen/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distribuce_HODNOTA image_HODNOTA hodnota_hash_Soubor 불일치')
    with zipfile.ZipFile(str(akce_kořen/'dist/jkoros-native-rpi4-boot.zip')) as sada:
        if hashlib.sha256(sada.read('kernel8.img')).hexdigest() != jádro_hodnota_hash:
            raise SystemExit('spuštění_stroje ZIP jádro_HODNOTA 불일치')
        부팅설정 = sada.read('config.txt')
        for Název, Velikost in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Název+'='+str(Velikost) not in 부팅설정.decode().splitlines():
                raise SystemExit('spuštění_stroje ZIP 화면 Nastavení 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(akce_kořen/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(akce_kořen/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hodnota_hash_Soubor(복사본) != jádro_hodnota_hash: raise SystemExit('SD image_HODNOTA jádro_HODNOTA 불일치')
        instance_Nastavení = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(akce_kořen/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(instance_Nastavení)])
        if instance_Nastavení.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Nastavení 불일치')
    LOGZ_ZÁZNAM = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jádro_hodnota_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': výjimka_Seznam, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(šek_řešení['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Název:hodnota_hash_Soubor(akce_kořen/'dist'/Název) for Název in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ověření_cesta/'native-runtime-summary.json').write_text(json.dumps(LOGZ_ZÁZNAM,ensure_ascii=False,indent=2)+'\n')
    print('PASS: dobrá_zboží 커널의',len(기록들),'개 통합 zkoušky LOGZ_ZÁZNAM, čeština výjimka',len(výjimka_Seznam),'Třída_Definice, SD image_HODNOTA·ZIP 일치')

if __name__ == '__main__': Spustit_2()
