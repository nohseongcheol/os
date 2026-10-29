#!/usr/bin/env python3
"""제한형 Java의 검증된 javac 바이트코드를 x86 ELF32 네이티브 코드로 변환한다."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


class 컴파일오류(Exception):
    pass


class 자료읽기:
    def __init__(자신, נתונים):
        자신.נתונים = נתונים
        자신.מיקום = 0

    def קרא(자신, 길이):
        if 길이 < 0 or 자신.מיקום + 길이 > len(자신.נתונים):
            raise 컴파일오류('잘린 כיתה_ערך 또는 פקודה נתונים')
        תוצאה = 자신.נתונים[자신.מיקום:자신.מיקום + 길이]
        자신.מיקום += 길이
        return תוצאה

    def 수(자신, לעצב_ערך):
        return struct.unpack('>' + לעצב_ערך, 자신.קרא(struct.calcsize('>' + לעצב_ערך)))[0]


def 수정유티에프해독(נתונים):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    מחרוזת_ערך = נתונים.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return מחרוזת_ערך.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class כיתה_ערך:
    def __init__(자신, נתיב):
        자신.נתיב = נתיב
        קורא_ערך = 자료읽기(נתיב.read_bytes())
        if קורא_ערך.수('I') != 0xcafebabe:
            raise 컴파일오류('Java כיתה_ערך 표식이 아님')
        קורא_ערך.קרא(4)
        개수 = קורא_ערך.수('H')
        자신.קבוע_ערך = [None] * 개수
        מדד = 1
        while מדד < 개수:
            종류 = קורא_ערך.수('B')
            if 종류 == 1:
                ערך = 수정유티에프해독(קורא_ערך.קרא(קורא_ערך.수('H')))
            elif 종류 == 3:
                ערך = קורא_ערך.수('i')
            elif 종류 == 4:
                ערך = קורא_ערך.קרא(4)
            elif 종류 in (5, 6):
                ערך = קורא_ערך.קרא(8)
            elif 종류 in (7, 8, 16):
                ערך = קורא_ערך.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ערך = (קורא_ערך.수('H'), קורא_ערך.수('H'))
            elif 종류 == 15:
                ערך = (קורא_ערך.수('B'), קורא_ערך.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 קבוע_ערך 종류: {}'.format(종류))
            자신.קבוע_ערך[מדד] = (종류, ערך)
            מדד += 2 if 종류 in (5, 6) else 1
        자신.גישה_ערך_68aed533 = קורא_ערך.수('H')
        자신.שם = 자신.שם_מחלקה(קורא_ערך.수('H'))
        אב_ערך = קורא_ערך.수('H')
        if 자신.שם_מחלקה(אב_ערך) != 'java/lang/Object' or קורא_ערך.수('H') != 0:
            raise 컴파일오류(자신.שם + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ערך_שדה = 자신.멤버읽기(קורא_ערך)
        자신.פונקציה_ערך = 자신.멤버읽기(קורא_ערך)
        자신.속성읽기(קורא_ערך)

    def 문자(자신, מדד):
        if 자신.קבוע_ערך[מדד][0] != 1:
            raise 컴파일오류('מחרוזת_ערך קבוע_ערך לעצב_ערך שגיאה')
        return 자신.קבוע_ערך[מדד][1]

    def שם_מחלקה(자신, מדד):
        return 자신.문자(자신.קבוע_ערך[מדד][1])

    def הפנה(자신, מדד):
        בעלים_ערך, שם_לעצב = 자신.קבוע_ערך[מדד][1]
        שם, לעצב_ערך = 자신.קבוע_ערך[שם_לעצב][1]
        return 자신.שם_מחלקה(בעלים_ערך), 자신.문자(שם), 자신.문자(לעצב_ערך)

    def 속성읽기(자신, קורא_ערך):
        תוצאה = {}
        for _ in range(קורא_ערך.수('H')):
            שם = 자신.문자(קורא_ערך.수('H'))
            תוצאה[שם] = קורא_ערך.קרא(קורא_ערך.수('I'))
        return תוצאה

    def 멤버읽기(자신, קורא_ערך):
        תוצאה = []
        for _ in range(קורא_ערך.수('H')):
            גישה_ערך_68aed533 = קורא_ערך.수('H')
            שם = 자신.문자(קורא_ערך.수('H'))
            לעצב_ערך = 자신.문자(קורא_ערך.수('H'))
            תוצאה.append((גישה_ערך_68aed533, שם, לעצב_ערך, 자신.속성읽기(קורא_ערך)))
        return תוצאה


def 형식읽기(מחרוזת_ערך):
    תוצאה = []
    מיקום = 0
    while מיקום < len(מחרוזת_ערך):
        for לעצב_ערך in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if מחרוזת_ערך.startswith(לעצב_ערך, מיקום):
                תוצאה.append(לעצב_ערך)
                מיקום += len(לעצב_ערך)
                break
        else:
            raise 컴파일오류('지원하지 않는 סוג_נתונים: ' + מחרוזת_ערך)
    return תוצאה


def 함수형식(서술):
    ארגומנטים, החזר_תוצאה = 서술[1:].split(')')
    ארגומנטים = 형식읽기(ארגומנטים)
    החזר_כתב = 형식읽기(החזר_תוצאה)
    if 'V' in ארגומנטים or len(החזר_כתב) != 1:
        raise 컴파일오류('פונקציה_ערך 서술 לעצב_ערך שגיאה: ' + 서술)
    return ארגומנטים, החזר_תוצאה


def סימן(종류, *부분):
    קודמקור = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(קודמקור).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 פונקציה_ערך 서술에 대해서만 허용한다.
def לבצע_פקודה(ארגומנטים=None):
    מנתח_48ee4b1b = argparse.ArgumentParser(description='עצמי Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK מקור_עץ בנייה')
    מנתח_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    מנתח_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 צירוף_ערך_b73accca JAR/כיתה_ערך 디렉터리')
    מנתח_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 בנייה JDK 또는 openjdk-build의 부트 JDK נתיב')
    מנתח_48ee4b1b.add_argument('--bundle-runtime', help='לבצע_פקודה 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    מנתח_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK תוכנית_מפעיל/מקור_עץ 빌드의 C מהדר')
    מנתח_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ מהדר')
    מנתח_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 בנייה 작업 수')
    מנתח_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 בנייה יעד (예: aarch64-linux-gnu)')
    מנתח_48ee4b1b.add_argument('--sysroot', help='교차 בנייה 대상의 libc/헤더/ספריה 루트')
    מנתח_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 לעצב_ערך')
    מנתח_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=כיתה_ערך.פונקציה_ערך (עצמי אופרנד_רמז ABI)')
    מנתח_48ee4b1b.add_argument('--entry', help='예: 계산.הפעלה (openjdk-build 이외 대상에서 필수)')
    מנתח_48ee4b1b.add_argument('-o', '--output', required=True, help='לבצע_פקודה ELF/.o פלטטקסט; openjdk-build는 전용 בנייה 디렉터리')
    מנתח_48ee4b1b.add_argument('sources', nargs='+')
    פרמטר_ארגומנט = מנתח_48ee4b1b.parse_args(ארגומנטים)
    if פרמטר_ארגומנט.target == 'openjdk-build':
        if len(פרמטר_ארגומנט.sources) != 1 or not פרמטר_ארגומנט.java_home or פרמטר_ארגומנט.entry or פרמטר_ארגומנט.export or פרמטר_ארגומנט.classpath or פרמטר_ארגומנט.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK מקור_עץ 디렉터리 하나와 --java-home 부트 JDK, -o בנייה 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(פרמטר_ארגומנט.sources[0], פרמטר_ארגומנט.output, פרמטר_ארגומנט.java_home, פרמטר_ארגומנט.jobs, פרמטר_ארגומנט.openjdk_target,
                  פרמטר_ארגומנט.sysroot, None if פרמטר_ארגומנט.cc == 'cc' else פרמטר_ארגומנט.cc, פרמטר_ארגומנט.cxx, פרמטר_ארגומנט.configure_arg)
        except BuildError as שגיאה:
            raise 컴파일오류(str(שגיאה))
        return
    if not פרמטר_ארגומנט.entry:
        מנתח_48ee4b1b.error('--entry is required for this target')
    if פרמטר_ארגומנט.cxx or פרמטר_ארגומנט.openjdk_target or פרמטר_ארגומנט.sysroot or פרמטר_ארגומנט.configure_arg or פרמטר_ארגומנט.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build יעד 전용')
    if פרמטר_ארגומנט.target == 'openjdk':
        sys.modules.setdefault('מהדר', sys.modules[__name__])
        from 실행파일 import ליצור_ערך
        ליצור_ערך(פרמטר_ארגומנט)
        return
    if פרמטר_ארגומנט.classpath or פרמטר_ארגומנט.java_home or פרמטר_ארגומנט.bundle_runtime or פרמטר_ארגומנט.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk יעד 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', פרמטר_ארגומנט.target, '--entry', פרמטר_ארגומנט.entry, '-o', פרמטר_ארגומנט.output]
    for הקצה_ערך in פרמטר_ארגומנט.export: 자바명령.extend(['--export', הקצה_ערך])
    subprocess.run(자바명령+פרמטר_ארגומנט.sources, check=True)
    return


if __name__ == '__main__':
    try:
        לבצע_פקודה()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as שגיאה:
        print('בנה_מקור שגיאה: ' + str(שגיאה), file=sys.stderr)
        sys.exit(1)
