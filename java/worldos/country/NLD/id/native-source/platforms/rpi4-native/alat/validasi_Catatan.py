#!/usr/bin/env python3
"""saat_ini_item 커널과 aktual_data pengujian·배포물이 일치할 때에만 통합 validasi 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Tugas_akar = Path(__file__).resolve().parents[1]

def hash_file(jalur):
    계산 = hashlib.sha256()
    with jalur.open('rb') as berkas:
        for data in iter(lambda: berkas.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def jalankan():
    validasi_jalur = Tugas_akar/'build/verification'
    kernel_hash = hash_file(Tugas_akar/'build/kernel8.img')
    기록들 = {}
    for Nama_2 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Nama_2 == 'boot' else Nama_2+'/report.json'
        data = json.loads((validasi_jalur/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kernel_hash:
            raise SystemExit('saat_ini_item 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Nama_2] = {'passed': True, 'report': 상대경로}
    cek_nama = json.loads((validasi_jalur/'naming/report.json').read_text())
    if not cek_nama['passed'] or not cek_nama['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for jalur, 기대값 in cek_nama['c_source_sha256'].items():
        if hash_file(Tugas_akar/jalur) != 기대값: raise SystemExit('명명 검사 BACK_VALUE 바뀐 C kodeSumber: '+jalur)
    자바검사 = json.loads((validasi_jalur/'jvm/report.json').read_text())
    직접화면 = json.loads((validasi_jalur/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Indonesia 직접 화면 Jalankan_perintah pengujian 필요')
    cek_byte_VALUE = json.loads((validasi_jalur/'naming/direct-bytecode.json').read_text())
    if not cek_byte_VALUE['passed'] or cek_byte_VALUE['jar_sha256'] != hash_file(Tugas_akar/'dist/jkoros-native-korean.jar'):
        raise SystemExit('saat_ini_item Indonesia 라이브러리의 직접 호출 바이트코드 periksa 필요')
    cek_resolusi = json.loads((validasi_jalur/'resolution/report.json').read_text())
    cek_ukuran = json.loads((validasi_jalur/'resize/report.json').read_text())
    갱신검사 = json.loads((validasi_jalur/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('saat_ini_item 커널의 부분 refresh pengujian 필요')
    for jalur, 기대값 in 갱신검사['source_sha256'].items():
        if hash_file(Tugas_akar/jalur) != 기대값: raise SystemExit('부분 refresh pengujian BACK_VALUE 바뀐 kodeSumber: '+jalur)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Indonesia 직접 가닥과 jalankan entri_p pengujian 필요')
    예제검사 = json.loads((validasi_jalur/'examples/report.json').read_text())
    if sorted(cek_ukuran['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ukuran 조절 pengujian 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Indonesia Swing 창을 포함한 예제 13개 pengujian 필요')
    if sorted(cek_resolusi['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 aktual_data 화면 pengujian 필요')
    if 자바검사['korean_library_sha256'] != hash_file(Tugas_akar/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 pengujian BACK_VALUE 라이브러리가 바뀌었습니다.')
    for Nama_2 in ('한국어통신시험','한국어예외시험'):
        if not any(entri_VALUE['name']==Nama_2 and entri_VALUE.get('openjdk_output_equal') for entri_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 pengujian 필요: '+Nama_2)
    pengecualian_Daftar = sorted(jalur.stem for jalur in (Tugas_akar/'한국어자바/Indonesia/Asli').glob('*pengecualian.java'))
    pengecualian_LOG = (validasi_jalur/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nama_2 in pengecualian_Daftar:
        if '\n'+Nama_2+'\n' not in pengecualian_LOG: raise SystemExit('pengecualian buat·잡기·설명 pengujian 필요: '+Nama_2)
    spes = json.loads((Tugas_akar/'dist/manifest.json').read_text())
    if spes['image_sha256'] != hash_file(Tugas_akar/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 foto_VALUE hash_file 불일치')
    with zipfile.ZipFile(str(Tugas_akar/'dist/jkoros-native-rpi4-boot.zip')) as paket:
        if hashlib.sha256(paket.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('awal_mesin ZIP kernel_VALUE 불일치')
        부팅설정 = paket.read('config.txt')
        for Nama_2, Ukuran in zip(('width', 'height'), spes['framebuffer_resolution']):
            if 'framebuffer_'+Nama_2+'='+str(Ukuran) not in 부팅설정.decode().splitlines():
                raise SystemExit('awal_mesin ZIP 화면 Konfigurasi 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Tugas_akar/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Tugas_akar/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_file(복사본) != kernel_hash: raise SystemExit('SD foto_VALUE kernel_VALUE 불일치')
        salin_Pengaturan = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Tugas_akar/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(salin_Pengaturan)])
        if salin_Pengaturan.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Konfigurasi 불일치')
    LOG_baris = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': pengecualian_Daftar, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(cek_resolusi['resolutions']),
            'sd_framebuffer_resolution': spes['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nama_2:hash_file(Tugas_akar/'dist'/Nama_2) for Nama_2 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validasi_jalur/'native-runtime-summary.json').write_text(json.dumps(LOG_baris,ensure_ascii=False,indent=2)+'\n')
    print('PASS: saat_ini_item 커널의',len(기록들),'개 통합 pengujian LOG_baris, Indonesia pengecualian',len(pengecualian_Daftar),'Kelas_Definisi, SD foto_VALUE·ZIP 일치')

if __name__ == '__main__': jalankan()
