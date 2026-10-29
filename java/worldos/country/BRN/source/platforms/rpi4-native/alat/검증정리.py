#!/usr/bin/env python3
"""현재 커널과 sebenar_data ujian·배포물이 일치할 때에만 통합 sahkan 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

projek_akar = Path(__file__).resolve().parents[1]

def cincangan_fail(LALUAN):
    계산 = hashlib.sha256()
    with LALUAN.open('rb') as Fail:
        for data in iter(lambda: Fail.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Jalan():
    pensahihan_laluan = projek_akar/'build/verification'
    kernel_cincangan = cincangan_fail(projek_akar/'build/kernel8.img')
    기록들 = {}
    for Nama in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        laluan_relatif = 'report.json' if Nama == 'boot' else Nama+'/report.json'
        data = json.loads((pensahihan_laluan/laluan_relatif).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kernel_cincangan:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+laluan_relatif)
        기록들[Nama] = {'passed': True, 'report': laluan_relatif}
    cek_nama = json.loads((pensahihan_laluan/'naming/report.json').read_text())
    if not cek_nama['passed'] or not cek_nama['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for LALUAN, 기대값 in cek_nama['c_source_sha256'].items():
        if cincangan_fail(projek_akar/LALUAN) != 기대값: raise SystemExit('명명 검사 BACK_VALUE 바뀐 C SUMBER: '+LALUAN)
    자바검사 = json.loads((pensahihan_laluan/'jvm/report.json').read_text())
    직접화면 = json.loads((pensahihan_laluan/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Melayu 직접 화면 laksanakan_perintah ujian 필요')
    cek_bait_VALUE = json.loads((pensahihan_laluan/'naming/direct-bytecode.json').read_text())
    if not cek_bait_VALUE['passed'] or cek_bait_VALUE['jar_sha256'] != cincangan_fail(projek_akar/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Melayu 라이브러리의 직접 호출 바이트코드 tentu_sahkan 필요')
    cek_resolusi = json.loads((pensahihan_laluan/'resolution/report.json').read_text())
    cek_saiz = json.loads((pensahihan_laluan/'resize/report.json').read_text())
    갱신검사 = json.loads((pensahihan_laluan/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_cincangan:
        raise SystemExit('현재 커널의 부분 segar_semula ujian 필요')
    for LALUAN, 기대값 in 갱신검사['source_sha256'].items():
        if cincangan_fail(projek_akar/LALUAN) != 기대값: raise SystemExit('부분 segar_semula ujian BACK_VALUE 바뀐 SUMBER: '+LALUAN)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Melayu 직접 가닥과 Jalan titik_permulaan ujian 필요')
    예제검사 = json.loads((pensahihan_laluan/'examples/report.json').read_text())
    if sorted(cek_saiz['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Saiz 조절 ujian 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Melayu Swing 창을 포함한 예제 13개 ujian 필요')
    if sorted(cek_resolusi['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 sebenar_data 화면 ujian 필요')
    if 자바검사['korean_library_sha256'] != cincangan_fail(projek_akar/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 ujian BACK_VALUE 라이브러리가 바뀌었습니다.')
    for Nama in ('한국어통신시험','한국어예외시험'):
        if not any(pemasukan_VALUE['name']==Nama and pemasukan_VALUE.get('openjdk_output_equal') for pemasukan_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 ujian 필요: '+Nama)
    pengecualian_Senarai = sorted(LALUAN.stem for LALUAN in (projek_akar/'한국어자바/Melayu/Asli').glob('*pengecualian.java'))
    pengecualian_LOG = (pensahihan_laluan/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nama in pengecualian_Senarai:
        if '\n'+Nama+'\n' not in pengecualian_LOG: raise SystemExit('pengecualian jana·잡기·설명 ujian 필요: '+Nama)
    명세 = json.loads((projek_akar/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != cincangan_fail(projek_akar/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 imej_VALUE cincangan_fail 불일치')
    with zipfile.ZipFile(str(projek_akar/'dist/jkoros-native-rpi4-boot.zip')) as pakej:
        if hashlib.sha256(pakej.read('kernel8.img')).hexdigest() != kernel_cincangan:
            raise SystemExit('permulaan_mesin ZIP kernel_VALUE 불일치')
        부팅설정 = pakej.read('config.txt')
        for Nama, Saiz in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nama+'='+str(Saiz) not in 부팅설정.decode().splitlines():
                raise SystemExit('permulaan_mesin ZIP 화면 Tetapan 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(projek_akar/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(projek_akar/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if cincangan_fail(복사본) != kernel_cincangan: raise SystemExit('SD imej_VALUE kernel_VALUE 불일치')
        tika_Seting = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(projek_akar/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(tika_Seting)])
        if tika_Seting.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Tetapan 불일치')
    LOG_baris = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_cincangan,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': pengecualian_Senarai, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(cek_resolusi['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nama:cincangan_fail(projek_akar/'dist'/Nama) for Nama in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (pensahihan_laluan/'native-runtime-summary.json').write_text(json.dumps(LOG_baris,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 ujian LOG_baris, Melayu pengecualian',len(pengecualian_Senarai),'Kelas_Takrif, SD imej_VALUE·ZIP 일치')

if __name__ == '__main__': Jalan()
