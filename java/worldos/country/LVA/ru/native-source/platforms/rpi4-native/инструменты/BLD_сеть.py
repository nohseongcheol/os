from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def Create_сеть(корень_путь, C_компилятор, Архив_средство, настройки_BITS, 실행):
    원본자료 = корень_путь / 'vendor/lwip/src'
    номер_порта = корень_путь / 'сеть_стек'
    выход = корень_путь / 'build/network'
    выход.mkdir(exist_ok=True)
    write_header(корень_путь, выход / 'ip_config.h')
    список_файлов = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    список_файлов += [원본자료 / 'netif/ethernet.c']
    список_файлов += sorted(номер_порта.glob('*.c'))
    цель_Файлы = []
    for путь in список_файлов:
        конечный_файл = выход / (путь.stem + '.o')
        실행([C_компилятор] + настройки_BITS + ['-include', выход / 'ip_config.h', '-std=c11', '-I', номер_порта, '-I', 원본자료 / 'include',
             '-I', корень_путь.parents[1] / 'posix-kor/arm64-native/объявления', '-c', путь, '-o', конечный_файл])
        цель_Файлы.append(конечный_файл)
    библиотека = выход / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(выход)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        실행([Архив_средство, 'rcs', 새라이브러리] + цель_Файлы)
        새라이브러리.replace(библиотека)
    return библиотека
