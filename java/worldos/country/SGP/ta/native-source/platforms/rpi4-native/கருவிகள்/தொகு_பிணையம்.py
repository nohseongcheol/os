from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def உருவாக்கு_பிணையம்(மூலம்_பாதை, 시언어번역기, காப்பகம்_கருவி, உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை, இயக்கு_கட்டளை):
    원본자료 = மூலம்_பாதை / 'vendor/lwip/src'
    முனைய_எண் = மூலம்_பாதை / 'பிணையம்_அடுக்கு_49fba3da'
    출력결과 = மூலம்_பாதை / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(மூலம்_பாதை, 출력결과 / 'ip_config.h')
    கோப்பு_பட்டியல் = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    கோப்பு_பட்டியல் += [원본자료 / 'netif/ethernet.c']
    கோப்பு_பட்டியல் += sorted(முனைய_எண்.glob('*.c'))
    இலக்கு_கோப்புகள் = []
    for பாதை_2 in கோப்பு_பட்டியல்:
        இலக்குக்_கோப்பு = 출력결과 / (பாதை_2.stem + '.o')
        இயக்கு_கட்டளை([시언어번역기] + உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', முனைய_எண், '-I', 원본자료 / 'include',
             '-I', மூலம்_பாதை.parents[1] / 'posix-kor/arm64-native/포함', '-c', பாதை_2, '-o', இலக்குக்_கோப்பு])
        இலக்கு_கோப்புகள்.append(இலக்குக்_கோப்பு)
    நூலகம் = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        இயக்கு_கட்டளை([காப்பகம்_கருவி, 'rcs', 새라이브러리] + இலக்கு_கோப்புகள்)
        새라이브러리.replace(நூலகம்)
    return நூலகம்
