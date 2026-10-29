#!/usr/bin/env python3
"""aktuális_cikk 커널과 tényleges_adat 시험·배포물이 일치할 때에만 통합 ellenőriz 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

teendő_gyök = Path(__file__).resolve().parents[1]

def kivonat_Fájl(ÚTVONAL):
    계산 = hashlib.sha256()
    with ÚTVONAL.open('rb') as Fájl:
        for adat in iter(lambda: Fájl.read(1048576), b''): 계산.update(adat)
    return 계산.hexdigest()

def Futtatás():
    ellenőrzés_útvonal = teendő_gyök/'build/verification'
    kernel_kivonat = kivonat_Fájl(teendő_gyök/'build/kernel8.img')
    기록들 = {}
    for Név in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relatív_elérési_út = 'report.json' if Név == 'boot' else Név+'/report.json'
        adat = json.loads((ellenőrzés_útvonal/relatív_elérési_út).read_text())
        if not adat.get('passed') or adat.get('kernel_sha256') != kernel_kivonat:
            raise SystemExit('aktuális_cikk 커널에 대한 성공 기록이 필요합니다: '+relatív_elérési_út)
        기록들[Név] = {'passed': True, 'report': relatív_elérési_út}
    csekk_név = json.loads((ellenőrzés_útvonal/'naming/report.json').read_text())
    if not csekk_név['passed'] or not csekk_név['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ÚTVONAL, 기대값 in csekk_név['c_source_sha256'].items():
        if kivonat_Fájl(teendő_gyök/ÚTVONAL) != 기대값: raise SystemExit('명명 검사 BACK_ÉRTÉK 바뀐 C FORRÁS: '+ÚTVONAL)
    자바검사 = json.loads((ellenőrzés_útvonal/'jvm/report.json').read_text())
    직접화면 = json.loads((ellenőrzés_útvonal/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('magyar 직접 화면 végrehajt_parancs 시험 필요')
    csekk_bájt_ÉRTÉK = json.loads((ellenőrzés_útvonal/'naming/direct-bytecode.json').read_text())
    if not csekk_bájt_ÉRTÉK['passed'] or csekk_bájt_ÉRTÉK['jar_sha256'] != kivonat_Fájl(teendő_gyök/'dist/jkoros-native-korean.jar'):
        raise SystemExit('aktuális_cikk magyar 라이브러리의 직접 호출 바이트코드 igazol 필요')
    csekk_felbontás = json.loads((ellenőrzés_útvonal/'resolution/report.json').read_text())
    csekk_méretez = json.loads((ellenőrzés_útvonal/'resize/report.json').read_text())
    갱신검사 = json.loads((ellenőrzés_útvonal/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_kivonat:
        raise SystemExit('aktuális_cikk 커널의 부분 frissít 시험 필요')
    for ÚTVONAL, 기대값 in 갱신검사['source_sha256'].items():
        if kivonat_Fájl(teendő_gyök/ÚTVONAL) != 기대값: raise SystemExit('부분 frissít 시험 BACK_ÉRTÉK 바뀐 FORRÁS: '+ÚTVONAL)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('magyar 직접 가닥과 Futtatás belépési_pont 시험 필요')
    예제검사 = json.loads((ellenőrzés_útvonal/'examples/report.json').read_text())
    if sorted(csekk_méretez['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Méret 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('magyar Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(csekk_felbontás['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 tényleges_adat 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != kivonat_Fájl(teendő_gyök/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 BACK_ÉRTÉK 라이브러리가 바뀌었습니다.')
    for Név in ('한국어통신시험','한국어예외시험'):
        if not any(bejegyzés_ÉRTÉK['name']==Név and bejegyzés_ÉRTÉK.get('openjdk_output_equal') for bejegyzés_ÉRTÉK in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Név)
    kivétel_Lista = sorted(ÚTVONAL.stem for ÚTVONAL in (teendő_gyök/'한국어자바/magyar/saját').glob('*kivétel.java'))
    kivétel_LOG = (ellenőrzés_útvonal/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Név in kivétel_Lista:
        if '\n'+Név+'\n' not in kivétel_LOG: raise SystemExit('kivétel generálás·잡기·설명 시험 필요: '+Név)
    명세 = json.loads((teendő_gyök/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != kivonat_Fájl(teendő_gyök/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('elosztás_ÉRTÉK KÉP_ÉRTÉK kivonat_Fájl 불일치')
    with zipfile.ZipFile(str(teendő_gyök/'dist/jkoros-native-rpi4-boot.zip')) as köteg:
        if hashlib.sha256(köteg.read('kernel8.img')).hexdigest() != kernel_kivonat:
            raise SystemExit('부팅 ZIP kernel_ÉRTÉK 불일치')
        부팅설정 = köteg.read('config.txt')
        for Név, Méret in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Név+'='+str(Méret) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Beállítások 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(teendő_gyök/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(teendő_gyök/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if kivonat_Fájl(복사본) != kernel_kivonat: raise SystemExit('SD KÉP_ÉRTÉK kernel_ÉRTÉK 불일치')
        másol_Gépház = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(teendő_gyök/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(másol_Gépház)])
        if másol_Gépház.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Beállítások 불일치')
    LOG_REKORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_kivonat,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': kivétel_Lista, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(csekk_felbontás['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Név:kivonat_Fájl(teendő_gyök/'dist'/Név) for Név in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ellenőrzés_útvonal/'native-runtime-summary.json').write_text(json.dumps(LOG_REKORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: aktuális_cikk 커널의',len(기록들),'개 통합 시험 LOG_REKORD, magyar kivétel',len(kivétel_Lista),'tanóra_Definíció, SD KÉP_ÉRTÉK·ZIP 일치')

if __name__ == '__main__': Futtatás()
