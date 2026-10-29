"""독립된 Asli ABI ELF64와 로더 tolak_VALUE ujian 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from bina_PYTHON import cipta_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def cipta_pengguna_SPACE(akar_laluan, repositori_laluan, 시언어번역기, 시플플번역기, pemaut_alat, Arkib_alat, konfigurasi_Background_Intelligent_Transfer_Service, laksanakan_perintah):
    konfigurasi_Background_Intelligent_Transfer_Service = [Seting_VALUE for Seting_VALUE in konfigurasi_Background_Intelligent_Transfer_Service if Seting_VALUE != '-mgeneral-regs-only']
    bina_laluan = akar_laluan / 'build'
    출력결과 = bina_laluan / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = akar_laluan / 'ruang_pengguna'
    포직스경로 = repositori_laluan / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / 'pengisytiharan', '-I', 출력결과]
    for 번역기, 추가영역, LALUAN, Nama in [
            (시언어번역기, [], 원본자료 / 'Jalan.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'laksanakan_perintah.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'pengguna_penghubung.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ContohFail.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Perlindungan_ujian.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        laksanakan_perintah([번역기] + konfigurasi_Background_Intelligent_Transfer_Service + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', LALUAN, '-o', 출력결과 / Nama])
    laksanakan_perintah([Arkib_alat, 'rcs', bina_laluan / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nama in ('demo', 'fault', 'network', 'vi'):
        laksanakan_perintah([pemaut_alat, '-T', 원본자료 / 'susun_atur_pautan.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nama + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nama + '.o'), bina_laluan / 'libposix-kor-user.a'])
    자바라이브러리만들기(akar_laluan, laksanakan_perintah)
    # 기존 Asli Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(bina_laluan)) as 작업경로:
        Kelas_laluan = Path(작업경로)
        laksanakan_perintah(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Kelas_laluan, '-sourcepath', Kelas_laluan, '-d', Kelas_laluan] +
            [data_jawatan for data_jawatan in sorted((repositori_laluan / 'os/ruang_pengguna/자바').glob('*.java')) if data_jawatan.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        laksanakan_perintah(['sh', repositori_laluan / 'compiler/미리번역.sh', '--entry', 'alat_pemasukan.Jalan',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Kelas_laluan.glob('*.class')))
    압축해제경로 = akar_laluan / 'vendor/uzlib'
    for LALUAN, Nama in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'pakej.c', 'jar.o')] + [(압축해제경로 / (Nama + '.c'), Nama + '.o') for Nama in ('tinflate', 'crc32', 'adler32')]:
        laksanakan_perintah([시언어번역기] + konfigurasi_Background_Intelligent_Transfer_Service + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', LALUAN, '-o', 출력결과 / Nama])
    laksanakan_perintah([pemaut_alat, '-T', 원본자료 / 'susun_atur_pautan.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nama for Nama in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    cipta_PYTHON(akar_laluan, 시언어번역기, pemaut_alat)
    시언어번역기만들기(akar_laluan, repositori_laluan, 시언어번역기, pemaut_alat, konfigurasi_Background_Intelligent_Transfer_Service, laksanakan_perintah)
    sah = (출력결과 / 'demo.elf').read_bytes()
    aplikasi_Pengepala_Ofset = struct.unpack_from('<Q', sah, 32)[0]
    Pengepala_Senarai = [aplikasi_Pengepala_Ofset + item_COUNT * 56 for item_COUNT in range(struct.unpack_from('<H', sah, 56)[0])]
    적재구획 = [data_jawatan for data_jawatan in Pengepala_Senarai if struct.unpack_from('<I', sah, data_jawatan)[0] == 1]
    Teks, data = 적재구획[:2]
    perintah_e_mel = struct.unpack_from('<Q', sah, Teks + 16)[0]
    data_e_mel = struct.unpack_from('<Q', sah, data + 16)[0]
    호출규약 = sah.index(b'JKOROS\0')
    kes_ujian = [('empty', b''), ('short', sah[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', perintah_e_mel + 1), ('data-entry', 24, 'Q', data_e_mel),
               ('outside-file', Teks + 32, 'Q', len(sah) + 1), ('short-memory', Teks + 40, 'Q', 1),
               ('kernel-address', Teks + 16, 'Q', 0x80000), ('memory-overflow', Teks + 40, 'Q', 2**64 - 1),
               ('writable-code', Teks + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Teks, 'I', 2),
               ('unaligned-load', Teks + 16, 'Q', perintah_e_mel + 8),
               ('overlap', data + 16, 'Q', perintah_e_mel)]
    for Nama, Ofset_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(sah); struct.pack_into('<' + format_932e03c8, 바뀐자료, Ofset_VALUE, VALUE)
        kes_ujian.append((Nama, bytes(바뀐자료)))
    탑재덩이들 = [(Nama.replace('-', '_'), 출력결과 / (Nama + '.elf')) for Nama in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Carian_INDEX, (Nama, muat_beban_data) in enumerate(kes_ujian):
        LALUAN = 출력결과 / ('invalid-{}.elf'.format(Nama)); LALUAN.write_bytes(muat_beban_data)
        탑재덩이들.append(('invalid_{}'.format(Carian_INDEX), LALUAN))
    himpunan, Pengepala_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nama, LALUAN in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Nama
        크기목록[Nama] = LALUAN.stat().st_size
        # 생성한 rakan_VALUE 경로만 넣어 프로젝트 경로의 공백/Petikan 영향을 피한다.
        himpunan += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(LALUAN.relative_to(akar_laluan))]
        Pengepala_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    himpunan.append('.section .note.GNU-stack,"",%progbits')
    Pengepala_VALUE += ['static const aplikasi 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Pengepala_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Pengepala_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Pengepala_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], kaedah_mod) for kaedah_mod in (0, 1)]
    Pengepala_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Pengepala_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Pengepala_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Pengepala_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Pengepala_VALUE += ['};', 'static const aplikasi 잘못된실행항목들[] = {']
    Pengepala_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(muat_beban_data)) for 순번, (_, muat_beban_data) in enumerate(kes_ujian)]
    Pengepala_VALUE += ['};']
    (bina_laluan / 'programs.S').write_text('\n'.join(himpunan) + '\n')
    (bina_laluan / 'programs.h').write_text('\n'.join(Pengepala_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nama for Nama, _ in kes_ujian) + '\n')
    laksanakan_perintah([시언어번역기] + konfigurasi_Background_Intelligent_Transfer_Service + ['-c', bina_laluan / 'programs.S', '-o', bina_laluan / 'programs.o'])
