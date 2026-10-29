#!/usr/bin/env python3
"""명시한 प्रयोक्ता ELF만 वाचन 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def बाइंड_करा_संचारटोक():
    मूल्य_पार्स_करा = argparse.ArgumentParser()
    मूल्य_पार्स_करा.add_argument('-o', required=True)
    मूल्य_पार्स_करा.add_argument('files', nargs='+', help='नाव=ELF경로')
    परिमापन_वितर्क = मूल्य_पार्स_करा.parse_args()
    if len(परिमापन_वितर्क.files) > 32:
        मूल्य_पार्स_करा.error('अनुप्रयोग_f5044b9b कमाल_मूल्य 32개')
    नोंदी_यादी = []
    नावे_यादी = set()
    for प्रविष्टी_मूल्य in परिमापन_वितर्क.files:
        नाव, मार्ग = प्रविष्टी_मूल्य.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', नाव) or नाव in नावे_यादी:
            मूल्य_पार्स_करा.error('आज्ञा_कार्यवाही_करा 이름이 잘못되었거나 중복됨: ' + नाव)
        नावे_यादी.add(नाव)
        डेटा = Path(मार्ग).read_bytes()
        if len(डेटा) > 2 * 1024 * 1024:
            मूल्य_पार्स_करा.error('आज्ञा_कार्यवाही_करा 파일이 너무 큼')
        नोंदी_यादी.append((नाव.encode(), डेटा))
    मोजमाप = bytearray(8 + 24 * len(नोंदी_यादी))
    struct.pack_into('<II', मोजमाप, 0, 0x50414b4a, len(नोंदी_यादी))
    for अनुक्रमणिका, (नाव, डेटा) in enumerate(नोंदी_यादी):
        मोजमाप.extend(bytes((-len(मोजमाप)) % 16))
        struct.pack_into('<16sII', मोजमाप, 8 + अनुक्रमणिका * 24, नाव, len(मोजमाप), len(डेटा))
        मोजमाप.extend(डेटा)
    Path(परिमापन_वितर्क.o).write_bytes(मोजमाप)

if __name__ == '__main__':
    बाइंड_करा_संचारटोक()
