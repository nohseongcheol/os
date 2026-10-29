"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from 자바라이브러리빌드 import 자바라이브러리만들기


def 예제만들기(기준경로, 저장소경로, ක්_රියාත්මක_කරන්න_විධානය):
    원본자료=저장소경로/'example';결과자료=기준경로/'build/examples';결과자료.mkdir(parents=True,exist_ok=True)
    පන්තිය_පෙත=결과자료/'classes';පන්තිය_පෙත.mkdir(exist_ok=True)
    자바라이브러리만들기(기준경로,ක්_රියාත්මක_කරන්න_විධානය)
    ip_settings = read_config(기준경로)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = 결과자료/'java-source'; java_sources.mkdir(exist_ok=True)
    자바실행=[]
    for path in sorted((원본자료/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); 자바실행.append(target)
    ක්_රියාත්මක_කරන්න_විධානය(['javac','--release','8','-encoding','UTF-8','-cp',기준경로/'build/java-library/classes','-d',පන්තිය_පෙත]+자바실행)
    උපදෙස_අනුක්_රමය=['public final class 예제꾸러미 { public static int ස්ථාපනය_කරන්න_අගය(int භාෂාව) { int 처리값;',
          '처리값=명령해석기.예제폴더("/example"); if(처리값<0)return 처리값;']
    꾸러미명세={}
    README_ගොනුව=guest_bytes(원본자료/'README.md')
    if len(README_ගොනුව)>16384: raise ValueError('example README exceeds native VFS limit')
    උපදෙස_අනුක්_රමය.append('처리값=명령해석기.예제파일("/example/README.md","%s"); if(처리값<0)return 처리값;'%README_ගොනුව.hex())
    꾸러미명세['/example/README.md']={'bytes':len(README_ගොනුව),'sha256':hashlib.sha256(README_ගොනුව).hexdigest()}
    උපදෙස_අනුක්_රමය.append('if(භාෂාව==0){처리값=명령해석기.예제폴더("/lib"); if(처리값<0)return 처리값;')
    for මාර්_ගය in [원본자료/'python/한국어.py'] + sorted((기준경로/'파이썬연결/ලේඛාගාරය').glob('*.py')):
        අන්තර්ගතය_අගය=guest_bytes(මාර්_ගය);ඉලක්කය='/lib/'+මාර්_ගය.name
        if len(අන්තර්ගතය_අගය)>16384: raise ValueError('Python library exceeds native VFS limit: '+ඉලක්කය)
        උපදෙස_අනුක්_රමය.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ඉලක්කය,ensure_ascii=True),අන්තර්ගතය_අගය.hex()))
        꾸러미명세[ඉලක්කය]={'bytes':len(අන්තර්ගතය_අගය),'sha256':hashlib.sha256(අන්තර්ගතය_අගය).hexdigest()}
    උපදෙස_අනුක්_රමය.append('}')
    for 색인,භාෂාව in enumerate(('java','c','python')):
        ගොනුව_ලැයිස්තුව=[(자료위치.name,자료위치) for 자료위치 in sorted((원본자료/භාෂාව).iterdir()) if 자료위치.is_file()]
        if භාෂාව=='java':ගොනුව_ලැයිස්තුව += [(자료위치.stem+'.class',පන්තිය_පෙත/(자료위치.stem+'.class')) for 자료위치 in 자바실행]
        උපදෙස_අනුක්_රමය += ['if(භාෂාව==%d){'%색인,'처리값=명령해석기.예제폴더("/example/%s"); if(처리값<0)return 처리값;'%භාෂාව]
        for නම,මාර්_ගය in ගොනුව_ලැයිස්තුව:
            අන්තර්ගතය_අගය=guest_bytes(මාර්_ගය);ඉලක්කය='/example/'+භාෂාව+'/'+නම
            if len(අන්තර්ගතය_අගය)>16384 or len(ඉලක්කය.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+ඉලක්කය)
            උපදෙස_අනුක්_රමය.append('처리값=명령해석기.예제파일(%s,"%s"); if(처리값<0)return 처리값;'%(json.dumps(ඉලක්කය,ensure_ascii=True),අන්තර්ගතය_අගය.hex()))
            꾸러미명세[ඉලක්කය]={'bytes':len(අන්තර්ගතය_අගය),'sha256':hashlib.sha256(අන්තර්ගතය_අගය).hexdigest()}
        උපදෙස_අනුක්_රමය += ['return 0;}']
    උපදෙස_අනුක්_රමය += ['return -22;}}']
    (기준경로/'build/예제꾸러미.java').write_text('\n'.join(උපදෙස_අනුක්_රමය)+'\n')
    (결과자료/'manifest.json').write_text(json.dumps(꾸러미명세,ensure_ascii=False,indent=2)+'\n')
