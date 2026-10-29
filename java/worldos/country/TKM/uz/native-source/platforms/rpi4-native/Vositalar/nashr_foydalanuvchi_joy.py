"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from nashr_PYTHON import Yaratish_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Yaratish_foydalanuvchi_joy(ildiz_yo_l, repozitoriy_yo_l, 시언어번역기, 시플플번역기, 연결편집기, Arxiv_vosita, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, bajarmoq_buyruq):
    tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati = [Sozlamalar_VALUE for Sozlamalar_VALUE in tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati if Sozlamalar_VALUE != '-mgeneral-regs-only']
    nashr_yo_l = ildiz_yo_l / 'build'
    출력결과 = nashr_yo_l / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = ildiz_yo_l / 'foydalanuvchi'
    포직스경로 = repozitoriy_yo_l / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, yo_l, Nomi in [
            (시언어번역기, [], 원본자료 / 'Bajarish.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'bajarmoq_buyruq.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Muharrir.c', 'vi.o')]:
        bajarmoq_buyruq([번역기] + tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', yo_l, '-o', 출력결과 / Nomi])
    bajarmoq_buyruq([Arxiv_vosita, 'rcs', nashr_yo_l / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nomi in ('demo', 'fault', 'network', 'vi'):
        bajarmoq_buyruq([연결편집기, '-T', 원본자료 / 'ulash_Maket.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nomi + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nomi + '.o'), nashr_yo_l / 'libposix-kor-user.a'])
    자바라이브러리만들기(ildiz_yo_l, bajarmoq_buyruq)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(nashr_yo_l)) as 작업경로:
        Sinf_yo_l = Path(작업경로)
        bajarmoq_buyruq(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Sinf_yo_l, '-sourcepath', Sinf_yo_l, '-d', Sinf_yo_l] +
            [ma_lumotlar_holat for ma_lumotlar_holat in sorted((repozitoriy_yo_l / 'os/foydalanuvchi/자바').glob('*.java')) if ma_lumotlar_holat.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        bajarmoq_buyruq(['sh', repozitoriy_yo_l / 'compiler/미리번역.sh', '--entry', 'vosita_kiritish.Bajarish',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Sinf_yo_l.glob('*.class')))
    압축해제경로 = ildiz_yo_l / 'vendor/uzlib'
    for yo_l, Nomi in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'to_plam.c', 'jar.o')] + [(압축해제경로 / (Nomi + '.c'), Nomi + '.o') for Nomi in ('tinflate', 'crc32', 'adler32')]:
        bajarmoq_buyruq([시언어번역기] + tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', yo_l, '-o', 출력결과 / Nomi])
    bajarmoq_buyruq([연결편집기, '-T', 원본자료 / 'ulash_Maket.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nomi for Nomi in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Yaratish_PYTHON(ildiz_yo_l, 시언어번역기, 연결편집기)
    시언어번역기만들기(ildiz_yo_l, repozitoriy_yo_l, 시언어번역기, 연결편집기, tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati, bajarmoq_buyruq)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    ilova_Sarlavha_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Sarlavha_Ro_yxat = [ilova_Sarlavha_OFFSET + element_COUNT * 56 for element_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [ma_lumotlar_holat for ma_lumotlar_holat in Sarlavha_Ro_yxat if struct.unpack_from('<I', 유효함, ma_lumotlar_holat)[0] == 1]
    Matn, ma_lumotlar = 적재구획[:2]
    buyruq_manzil = struct.unpack_from('<Q', 유효함, Matn + 16)[0]
    ma_lumotlar_manzil = struct.unpack_from('<Q', 유효함, ma_lumotlar + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', buyruq_manzil + 1), ('data-entry', 24, 'Q', ma_lumotlar_manzil),
               ('outside-file', Matn + 32, 'Q', len(유효함) + 1), ('short-memory', Matn + 40, 'Q', 1),
               ('kernel-address', Matn + 16, 'Q', 0x80000), ('memory-overflow', Matn + 40, 'Q', 2**64 - 1),
               ('writable-code', Matn + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Matn, 'I', 2),
               ('unaligned-load', Matn + 16, 'Q', buyruq_manzil + 8),
               ('overlap', ma_lumotlar + 16, 'Q', buyruq_manzil)]
    for Nomi, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Nomi, bytes(바뀐자료)))
    탑재덩이들 = [(Nomi.replace('-', '_'), 출력결과 / (Nomi + '.elf')) for Nomi in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Nomi, foydali_yuklanma_ma_lumotlar) in enumerate(시험사례):
        yo_l = 출력결과 / ('invalid-{}.elf'.format(Nomi)); yo_l.write_bytes(foydali_yuklanma_ma_lumotlar)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), yo_l))
    어셈블리자료, Sarlavha_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nomi, yo_l in 탑재덩이들:
        ramz_VALUE = 'user_blob_' + Nomi
        크기목록[Nomi] = yo_l.stat().st_size
        # 생성한 bir_rangli_VALUE 경로만 넣어 프로젝트 경로의 공백/Sitata_kiritish 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + ramz_VALUE, ramz_VALUE + ':', '.incbin "{}"'.format(yo_l.relative_to(ildiz_yo_l))]
        Sarlavha_VALUE.append('extern const unsigned char {}[];'.format(ramz_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Sarlavha_VALUE += ['static const ilova 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Sarlavha_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Sarlavha_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Sarlavha_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], uslub_MODE) for uslub_MODE in (0, 1)]
    Sarlavha_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Sarlavha_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Sarlavha_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Sarlavha_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Sarlavha_VALUE += ['};', 'static const ilova 잘못된실행항목들[] = {']
    Sarlavha_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(foydali_yuklanma_ma_lumotlar)) for 순번, (_, foydali_yuklanma_ma_lumotlar) in enumerate(시험사례)]
    Sarlavha_VALUE += ['};']
    (nashr_yo_l / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (nashr_yo_l / 'programs.h').write_text('\n'.join(Sarlavha_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nomi for Nomi, _ in 시험사례) + '\n')
    bajarmoq_buyruq([시언어번역기] + tarkibiy_tuzilma_fonda_intellektual_uzatish_xizmati + ['-c', nashr_yo_l / 'programs.S', '-o', nashr_yo_l / 'programs.o'])
