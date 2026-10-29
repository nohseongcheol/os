#!/usr/bin/env python3
"""현재 커널과 ulwazi_ngokwenzekile_imininingwane 시험·배포물이 일치할 때에만 통합 qinisekisa 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def i_hash_ifayela(Indlela_2):
    계산 = hashlib.sha256()
    with Indlela_2.open('rb') as Ihele:
        for imininingwane in iter(lambda: Ihele.read(1048576), b''): 계산.update(imininingwane)
    return 계산.hexdigest()

def Sebenzisa():
    ukufakazisa_umzila = 기준/'build/verification'
    ikhenela_i_hash = i_hash_ifayela(기준/'build/kernel8.img')
    기록들 = {}
    for Igama in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Igama == 'boot' else Igama+'/report.json'
        imininingwane = json.loads((ukufakazisa_umzila/상대경로).read_text())
        if not imininingwane.get('passed') or imininingwane.get('kernel_sha256') != ikhenela_i_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Igama] = {'passed': True, 'report': 상대경로}
    hlola_igama = json.loads((ukufakazisa_umzila/'naming/report.json').read_text())
    if not hlola_igama['passed'] or not hlola_igama['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Indlela_2, 기대값 in hlola_igama['c_source_sha256'].items():
        if i_hash_ifayela(기준/Indlela_2) != 기대값: raise SystemExit('명명 검사 Impindamuva_inani 바뀐 C umthombo: '+Indlela_2)
    자바검사 = json.loads((ukufakazisa_umzila/'jvm/report.json').read_text())
    직접화면 = json.loads((ukufakazisa_umzila/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Isi_Zulu 직접 화면 yenza_umyalo 시험 필요')
    hlola_ibhayithi_inani = json.loads((ukufakazisa_umzila/'naming/direct-bytecode.json').read_text())
    if not hlola_ibhayithi_inani['passed'] or hlola_ibhayithi_inani['jar_sha256'] != i_hash_ifayela(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Isi_Zulu 라이브러리의 직접 호출 바이트코드 qiniseka 필요')
    hlola_ukucaca = json.loads((ukufakazisa_umzila/'resolution/report.json').read_text())
    hlola_linganisa = json.loads((ukufakazisa_umzila/'resize/report.json').read_text())
    갱신검사 = json.loads((ukufakazisa_umzila/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ikhenela_i_hash:
        raise SystemExit('현재 커널의 부분 vuselela 시험 필요')
    for Indlela_2, 기대값 in 갱신검사['source_sha256'].items():
        if i_hash_ifayela(기준/Indlela_2) != 기대값: raise SystemExit('부분 vuselela 시험 Impindamuva_inani 바뀐 umthombo: '+Indlela_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Isi_Zulu 직접 가닥과 Sebenzisa okufakwayo_iphoyinti 시험 필요')
    예제검사 = json.loads((ukufakazisa_umzila/'examples/report.json').read_text())
    if sorted(hlola_linganisa['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ubungako 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Isi_Zulu Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(hlola_ukucaca['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ulwazi_ngokwenzekile_imininingwane 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != i_hash_ifayela(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Impindamuva_inani 라이브러리가 바뀌었습니다.')
    for Igama in ('한국어통신시험','한국어예외시험'):
        if not any(okufakwayo_inani['name']==Igama and okufakwayo_inani.get('openjdk_output_equal') for okufakwayo_inani in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Igama)
    예외들 = sorted(Indlela_2.stem for Indlela_2 in (기준/'한국어자바/Isi_Zulu/자체').glob('*예외.java'))
    예외기록 = (ukufakazisa_umzila/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Igama in 예외들:
        if '\n'+Igama+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Igama)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != i_hash_ifayela(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 isithombe_inani i_hash_ifayela 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as isigaxa:
        if hashlib.sha256(isigaxa.read('kernel8.img')).hexdigest() != ikhenela_i_hash:
            raise SystemExit('부팅 ZIP ikhenela_inani 불일치')
        부팅설정 = isigaxa.read('config.txt')
        for Igama, Ubungako in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Igama+'='+str(Ubungako) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Izinhlelo 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if i_hash_ifayela(복사본) != ikhenela_i_hash: raise SystemExit('SD isithombe_inani ikhenela_inani 불일치')
        kopisha_Amasethingi = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopisha_Amasethingi)])
        if kopisha_Amasethingi.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Izinhlelo 불일치')
    loga_umugqa = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ikhenela_i_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(hlola_ukucaca['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Igama:i_hash_ifayela(기준/'dist'/Igama) for Igama in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ukufakazisa_umzila/'native-runtime-summary.json').write_text(json.dumps(loga_umugqa,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 loga_umugqa, Isi_Zulu 예외',len(예외들),'uhlobo_Incazelo, SD isithombe_inani·ZIP 일치')

if __name__ == '__main__': Sebenzisa()
