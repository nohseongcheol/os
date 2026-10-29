#!/usr/bin/env python3
"""명시한 Java स्रोत_ट्री/वर्ग_मूल्य 파일을 प्रणालीप्रारंभ 시 RAM 파일체계로 가져온다."""
import argparse
from pathlib import Path
import re
import struct


def बाइंड_करा_संचारटोक(नोंदी_यादी):
    संचिका_नोंदी = []
    नावे_यादी = {'Hello.java'}
    स्पष्ट_नावे = set()
    for प्रविष्टी_मूल्य in नोंदी_यादी:
        if '=' not in प्रविष्टी_मूल्य:
            raise ValueError('expected NAME=PATH: ' + प्रविष्टी_मूल्य)
        नाव, मार्ग = प्रविष्टी_मूल्य.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9_.-]{0,62}', नाव) or नाव in स्पष्ट_नावे:
            raise ValueError('invalid or duplicate file name: ' + नाव)
        स्पष्ट_नावे.add(नाव)
        नावे_यादी.add(नाव)
        डेटा = Path(मार्ग).read_bytes()
        if len(डेटा) > 16384:
            raise ValueError('file exceeds 16384 bytes: ' + नाव)
        संचिका_नोंदी.append((नाव.encode('ascii'), डेटा))
    if len(नावे_यादी) > 8:
        raise ValueError('RAM file limit: 8 files including the default Hello.java')
    मोजमाप = bytearray(struct.pack('<4sI', b'JKJF', len(संचिका_नोंदी)))
    मोजमाप.extend(bytes(72 * len(संचिका_नोंदी)))
    for संख्या, (नाव, डेटा) in enumerate(संचिका_नोंदी):
        struct.pack_into('<64sII', मोजमाप, 8 + संख्या * 72, नाव, len(मोजमाप), len(डेटा))
        मोजमाप.extend(डेटा)
    return bytes(मोजमाप)


if __name__ == '__main__':
    मूल्य_पार्स_करा = argparse.ArgumentParser(description=__doc__)
    मूल्य_पार्स_करा.add_argument('-o', required=True)
    मूल्य_पार्स_करा.add_argument('files', nargs='*', help='NAME=PATH')
    बाबी = मूल्य_पार्स_करा.parse_args()
    try:
        डेटा = बाइंड_करा_संचारटोक(बाबी.files)
        गंतव्यस्थान_मूल्य = Path(बाबी.o)
        if not गंतव्यस्थान_मूल्य.exists() or गंतव्यस्थान_मूल्य.read_bytes() != डेटा:
            तात्पुरते_मूल्य = गंतव्यस्थान_मूल्य.with_name(गंतव्यस्थान_मूल्य.name + '.tmp')
            तात्पुरते_मूल्य.write_bytes(डेटा)
            तात्पुरते_मूल्य.replace(गंतव्यस्थान_मूल्य)
    except (ValueError, OSError) as त्रुटी:
        मूल्य_पार्स_करा.error(str(त्रुटी))
