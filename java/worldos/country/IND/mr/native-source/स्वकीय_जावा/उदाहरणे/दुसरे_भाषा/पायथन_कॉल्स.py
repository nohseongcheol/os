#!/usr/bin/env python3
"""शेवटीजोडा_प्रविष्टी Python 패키지 없이 मराठी Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def वर्ण_कोड_संख्या(सामुग्री_मूल्य, लायब्ररी, वर्ग_निर्देशिका):
    मोजमाप = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(लायब्ररी), str(वर्ग_निर्देशिका)]), 'मजकूर_आदेश', सामुग्री_मूल्य],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(मोजमाप.stdout.strip())


if __name__ == '__main__':
    वितर्क_पार्स_करा = argparse.ArgumentParser(description=__doc__)
    वितर्क_पार्स_करा.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/स्वकीय_जावा.jar'))
    वितर्क_पार्स_करा.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    वितर्क_पार्स_करा.add_argument('--text', default='한글 😀')
    बाबी = वितर्क_पार्स_करा.parse_args()
    print('Python → मराठी.जावा.वर्ण.वर्ण_कोड_संख्या:',
          वर्ण_कोड_संख्या(बाबी.text, बाबी.jar, बाबी.classes))
