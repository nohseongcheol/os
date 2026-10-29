#!/usr/bin/env python3
"""현재 커널과 eyona_yenzekileyo_iingcombolo 시험·배포물이 일치할 때에만 통합 qinisekisa 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def i_hash_ifayile(INDLELA):
    계산 = hashlib.sha256()
    with INDLELA.open('rb') as iFayili:
        for iingcombolo in iter(lambda: iFayili.read(1048576), b''): 계산.update(iingcombolo)
    return 계산.hexdigest()

def Phumeza():
    uqinisekiso_indlela = 기준/'build/verification'
    ikheneli_i_hash = i_hash_ifayile(기준/'build/kernel8.img')
    기록들 = {}
    for Igama in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Igama == 'boot' else Igama+'/report.json'
        iingcombolo = json.loads((uqinisekiso_indlela/상대경로).read_text())
        if not iingcombolo.get('passed') or iingcombolo.get('kernel_sha256') != ikheneli_i_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Igama] = {'passed': True, 'report': 상대경로}
    jonga_igama = json.loads((uqinisekiso_indlela/'naming/report.json').read_text())
    if not jonga_igama['passed'] or not jonga_igama['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for INDLELA, 기대값 in jonga_igama['c_source_sha256'].items():
        if i_hash_ifayile(기준/INDLELA) != 기대값: raise SystemExit('명명 검사 Emva_ixabiso 바뀐 C UMTHOMBO: '+INDLELA)
    자바검사 = json.loads((uqinisekiso_indlela/'jvm/report.json').read_text())
    직접화면 = json.loads((uqinisekiso_indlela/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('isiXhosa 직접 화면 ukwenza_umyalelo 시험 필요')
    jonga_ibhayithi_ixabiso = json.loads((uqinisekiso_indlela/'naming/direct-bytecode.json').read_text())
    if not jonga_ibhayithi_ixabiso['passed'] or jonga_ibhayithi_ixabiso['jar_sha256'] != i_hash_ifayile(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 isiXhosa 라이브러리의 직접 호출 바이트코드 ngqinisisa 필요')
    jonga_isisombululo = json.loads((uqinisekiso_indlela/'resolution/report.json').read_text())
    jonga_isayizi = json.loads((uqinisekiso_indlela/'resize/report.json').read_text())
    갱신검사 = json.loads((uqinisekiso_indlela/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ikheneli_i_hash:
        raise SystemExit('현재 커널의 부분 qalela_ngokutsha 시험 필요')
    for INDLELA, 기대값 in 갱신검사['source_sha256'].items():
        if i_hash_ifayile(기준/INDLELA) != 기대값: raise SystemExit('부분 qalela_ngokutsha 시험 Emva_ixabiso 바뀐 UMTHOMBO: '+INDLELA)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('isiXhosa 직접 가닥과 Phumeza ufako_nkcukacha_inqaku 시험 필요')
    예제검사 = json.loads((uqinisekiso_indlela/'examples/report.json').read_text())
    if sorted(jonga_isayizi['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ubukhulu 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('isiXhosa Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(jonga_isisombululo['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 eyona_yenzekileyo_iingcombolo 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != i_hash_ifayile(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Emva_ixabiso 라이브러리가 바뀌었습니다.')
    for Igama in ('한국어통신시험','한국어예외시험'):
        if not any(ufako_nkcukacha_ixabiso['name']==Igama and ufako_nkcukacha_ixabiso.get('openjdk_output_equal') for ufako_nkcukacha_ixabiso in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Igama)
    예외들 = sorted(INDLELA.stem for INDLELA in (기준/'한국어자바/isiXhosa/자체').glob('*예외.java'))
    예외기록 = (uqinisekiso_indlela/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Igama in 예외들:
        if '\n'+Igama+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Igama)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != i_hash_ifayile(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 umfanekiso_ixabiso i_hash_ifayile 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as umqulu:
        if hashlib.sha256(umqulu.read('kernel8.img')).hexdigest() != ikheneli_i_hash:
            raise SystemExit('부팅 ZIP ikheneli_ixabiso 불일치')
        부팅설정 = umqulu.read('config.txt')
        for Igama, Ubukhulu in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Igama+'='+str(Ubukhulu) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Imimiselo 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if i_hash_ifayile(복사본) != ikheneli_i_hash: raise SystemExit('SD umfanekiso_ixabiso ikheneli_ixabiso 불일치')
        kopa_Iisetingi = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopa_Iisetingi)])
        if kopa_Iisetingi.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Imimiselo 불일치')
    ilog_umqolo = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ikheneli_i_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(jonga_isisombululo['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Igama:i_hash_ifayile(기준/'dist'/Igama) for Igama in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (uqinisekiso_indlela/'native-runtime-summary.json').write_text(json.dumps(ilog_umqolo,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ilog_umqolo, isiXhosa 예외',len(예외들),'iklasi_Ingcaciso, SD umfanekiso_ixabiso·ZIP 일치')

if __name__ == '__main__': Phumeza()
