"""독립된 Asli ABI ELF64와 로더 tolak_VALUE pengujian 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from build_PYTHON import Buat_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Buat_pengguna_SPACE(akar_jalur, repositori_jalur, 시언어번역기, 시플플번역기, 연결편집기, Arsip_alat, konfigurasi_Background_Intelligent_Transfer_Service, Jalankan_perintah):
    konfigurasi_Background_Intelligent_Transfer_Service = [Pengaturan_VALUE for Pengaturan_VALUE in konfigurasi_Background_Intelligent_Transfer_Service if Pengaturan_VALUE != '-mgeneral-regs-only']
    build_jalur = akar_jalur / 'build'
    출력결과 = build_jalur / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = akar_jalur / 'ruang_pengguna'
    포직스경로 = repositori_jalur / 'posix-kor/arm64-native'
    sertakan_jalur = ['-I', 원본자료, '-I', 포직스경로 / 'deklarasi', '-I', 출력결과]
    for 번역기, 추가영역, jalur, Nama_2 in [
            (시언어번역기, [], 원본자료 / 'jalankan.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Jalankan_perintah.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'pengguna_bridge.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ContohBerkas.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Jalankan_perintah([번역기] + konfigurasi_Background_Intelligent_Transfer_Service + 추가영역 + sertakan_jalur + ['-Wall', '-Wextra', '-Werror', '-c', jalur, '-o', 출력결과 / Nama_2])
    Jalankan_perintah([Arsip_alat, 'rcs', build_jalur / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nama_2 in ('demo', 'fault', 'network', 'vi'):
        Jalankan_perintah([연결편집기, '-T', 원본자료 / 'tata_letak_penautan.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nama_2 + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nama_2 + '.o'), build_jalur / 'libposix-kor-user.a'])
    자바라이브러리만들기(akar_jalur, Jalankan_perintah)
    # 기존 Asli Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(build_jalur)) as 작업경로:
        Kelas_jalur = Path(작업경로)
        Jalankan_perintah(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Kelas_jalur, '-sourcepath', Kelas_jalur, '-d', Kelas_jalur] +
            [data_posisi for data_posisi in sorted((repositori_jalur / 'os/ruang_pengguna/자바').glob('*.java')) if data_posisi.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Jalankan_perintah(['sh', repositori_jalur / 'compiler/미리번역.sh', '--entry', 'alat_entri.jalankan',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Kelas_jalur.glob('*.class')))
    압축해제경로 = akar_jalur / 'vendor/uzlib'
    for jalur, Nama_2 in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paket.c', 'jar.o')] + [(압축해제경로 / (Nama_2 + '.c'), Nama_2 + '.o') for Nama_2 in ('tinflate', 'crc32', 'adler32')]:
        Jalankan_perintah([시언어번역기] + konfigurasi_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + sertakan_jalur + ['-c', jalur, '-o', 출력결과 / Nama_2])
    Jalankan_perintah([연결편집기, '-T', 원본자료 / 'tata_letak_penautan.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nama_2 for Nama_2 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Buat_PYTHON(akar_jalur, 시언어번역기, 연결편집기)
    시언어번역기만들기(akar_jalur, repositori_jalur, 시언어번역기, 연결편집기, konfigurasi_Background_Intelligent_Transfer_Service, Jalankan_perintah)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    apl_judul_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    judul_Daftar = [apl_judul_OFFSET + item_COUNT * 56 for item_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [data_posisi for data_posisi in judul_Daftar if struct.unpack_from('<I', 유효함, data_posisi)[0] == 1]
    teks, data = 적재구획[:2]
    perintah_surel = struct.unpack_from('<Q', 유효함, teks + 16)[0]
    data_surel = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', perintah_surel + 1), ('data-entry', 24, 'Q', data_surel),
               ('outside-file', teks + 32, 'Q', len(유효함) + 1), ('short-memory', teks + 40, 'Q', 1),
               ('kernel-address', teks + 16, 'Q', 0x80000), ('memory-overflow', teks + 40, 'Q', 2**64 - 1),
               ('writable-code', teks + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', teks, 'I', 2),
               ('unaligned-load', teks + 16, 'Q', perintah_surel + 8),
               ('overlap', data + 16, 'Q', perintah_surel)]
    for Nama_2, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Nama_2, bytes(바뀐자료)))
    탑재덩이들 = [(Nama_2.replace('-', '_'), 출력결과 / (Nama_2 + '.elf')) for Nama_2 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Nama_2, payload_data) in enumerate(시험사례):
        jalur = 출력결과 / ('invalid-{}.elf'.format(Nama_2)); jalur.write_bytes(payload_data)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), jalur))
    rakitan, judul_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nama_2, jalur in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Nama_2
        크기목록[Nama_2] = jalur.stat().st_size
        # 생성한 serekan_VALUE 경로만 넣어 프로젝트 경로의 공백/Kutipan 영향을 피한다.
        rakitan += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(jalur.relative_to(akar_jalur))]
        judul_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    rakitan.append('.section .note.GNU-stack,"",%progbits')
    judul_VALUE += ['static const apl 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    judul_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    judul_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    judul_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metode_MODE) for metode_MODE in (0, 1)]
    judul_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    judul_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    judul_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    judul_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    judul_VALUE += ['};', 'static const apl 잘못된실행항목들[] = {']
    judul_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(payload_data)) for 순번, (_, payload_data) in enumerate(시험사례)]
    judul_VALUE += ['};']
    (build_jalur / 'programs.S').write_text('\n'.join(rakitan) + '\n')
    (build_jalur / 'programs.h').write_text('\n'.join(judul_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nama_2 for Nama_2, _ in 시험사례) + '\n')
    Jalankan_perintah([시언어번역기] + konfigurasi_Background_Intelligent_Transfer_Service + ['-c', build_jalur / 'programs.S', '-o', build_jalur / 'programs.o'])
