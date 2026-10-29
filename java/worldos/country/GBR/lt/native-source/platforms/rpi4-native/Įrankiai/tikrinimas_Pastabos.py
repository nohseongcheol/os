#!/usr/bin/env python3
"""dabartinis_prekė 커널과 faktinis_duomenys 시험·배포물이 일치할 때에만 통합 tikrinti 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_šaknis = Path(__file__).resolve().parents[1]

def maiša_Failas(KELIAS):
    계산 = hashlib.sha256()
    with KELIAS.open('rb') as Failas:
        for duomenys in iter(lambda: Failas.read(1048576), b''): 계산.update(duomenys)
    return 계산.hexdigest()

def Paleisti():
    tikrinimas_kelias = Project_šaknis/'build/verification'
    branduolys_maiša = maiša_Failas(Project_šaknis/'build/kernel8.img')
    기록들 = {}
    for Pavadinimas_2 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        santykinis_kelias = 'report.json' if Pavadinimas_2 == 'boot' else Pavadinimas_2+'/report.json'
        duomenys = json.loads((tikrinimas_kelias/santykinis_kelias).read_text())
        if not duomenys.get('passed') or duomenys.get('kernel_sha256') != branduolys_maiša:
            raise SystemExit('dabartinis_prekė 커널에 대한 성공 기록이 필요합니다: '+santykinis_kelias)
        기록들[Pavadinimas_2] = {'passed': True, 'report': santykinis_kelias}
    čekis_pavadinimas = json.loads((tikrinimas_kelias/'naming/report.json').read_text())
    if not čekis_pavadinimas['passed'] or not čekis_pavadinimas['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for KELIAS, 기대값 in čekis_pavadinimas['c_source_sha256'].items():
        if maiša_Failas(Project_šaknis/KELIAS) != 기대값: raise SystemExit('명명 검사 ATGAL_VALUE 바뀐 C ŠALTINIS: '+KELIAS)
    자바검사 = json.loads((tikrinimas_kelias/'jvm/report.json').read_text())
    직접화면 = json.loads((tikrinimas_kelias/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Lietuvių 직접 화면 Vykdyti_komanda 시험 필요')
    čekis_baitas_VALUE = json.loads((tikrinimas_kelias/'naming/direct-bytecode.json').read_text())
    if not čekis_baitas_VALUE['passed'] or čekis_baitas_VALUE['jar_sha256'] != maiša_Failas(Project_šaknis/'dist/jkoros-native-korean.jar'):
        raise SystemExit('dabartinis_prekė Lietuvių 라이브러리의 직접 호출 바이트코드 patvirtinti 필요')
    čekis_skiriamoji_geba = json.loads((tikrinimas_kelias/'resolution/report.json').read_text())
    čekis_dydis = json.loads((tikrinimas_kelias/'resize/report.json').read_text())
    갱신검사 = json.loads((tikrinimas_kelias/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != branduolys_maiša:
        raise SystemExit('dabartinis_prekė 커널의 부분 atnaujinti 시험 필요')
    for KELIAS, 기대값 in 갱신검사['source_sha256'].items():
        if maiša_Failas(Project_šaknis/KELIAS) != 기대값: raise SystemExit('부분 atnaujinti 시험 ATGAL_VALUE 바뀐 ŠALTINIS: '+KELIAS)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Lietuvių 직접 가닥과 Paleisti įrašas_p 시험 필요')
    예제검사 = json.loads((tikrinimas_kelias/'examples/report.json').read_text())
    if sorted(čekis_dydis['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Dydis 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Lietuvių Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(čekis_skiriamoji_geba['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 faktinis_duomenys 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != maiša_Failas(Project_šaknis/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ATGAL_VALUE 라이브러리가 바뀌었습니다.')
    for Pavadinimas_2 in ('한국어통신시험','한국어예외시험'):
        if not any(įrašas_VALUE['name']==Pavadinimas_2 and įrašas_VALUE.get('openjdk_output_equal') for įrašas_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Pavadinimas_2)
    išimtis_Sąrašas = sorted(KELIAS.stem for KELIAS in (Project_šaknis/'한국어자바/Lietuvių/savas').glob('*išimtis.java'))
    išimtis_LOG = (tikrinimas_kelias/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Pavadinimas_2 in išimtis_Sąrašas:
        if '\n'+Pavadinimas_2+'\n' not in išimtis_LOG: raise SystemExit('išimtis generuoti·잡기·aprašas 시험 필요: '+Pavadinimas_2)
    명세 = json.loads((Project_šaknis/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != maiša_Failas(Project_šaknis/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('paskirstymas_VALUE IMAGE_VALUE maiša_Failas 불일치')
    with zipfile.ZipFile(str(Project_šaknis/'dist/jkoros-native-rpi4-boot.zip')) as paketas:
        if hashlib.sha256(paketas.read('kernel8.img')).hexdigest() != branduolys_maiša:
            raise SystemExit('부팅 ZIP branduolys_VALUE 불일치')
        부팅설정 = paketas.read('config.txt')
        for Pavadinimas_2, Dydis in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Pavadinimas_2+'='+str(Dydis) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Nustatymai 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_šaknis/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_šaknis/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if maiša_Failas(복사본) != branduolys_maiša: raise SystemExit('SD IMAGE_VALUE branduolys_VALUE 불일치')
        kopijuoti_Parametrai = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_šaknis/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopijuoti_Parametrai)])
        if kopijuoti_Parametrai.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Nustatymai 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': branduolys_maiša,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': išimtis_Sąrašas, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(čekis_skiriamoji_geba['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Pavadinimas_2:maiša_Failas(Project_šaknis/'dist'/Pavadinimas_2) for Pavadinimas_2 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (tikrinimas_kelias/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: dabartinis_prekė 커널의',len(기록들),'개 통합 시험 LOG_RECORD, Lietuvių išimtis',len(išimtis_Sąrašas),'klasė_Apibrėžtis, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Paleisti()
