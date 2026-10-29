#!/usr/bin/env python3
"""새 파일에만 JKSTORE1 전용 साठवणे_मूल्य 매체를 만든다. 기존 फाइल/장치는 덮어쓰지 않는다."""
import argparse
from pathlib import Path
import struct

def प्रविष्टी_तयार_करा(मार्ग):
    with Path(मार्ग).open('xb') as आउटपुट:
        शीर्ष_मूल्य = bytearray(512)
        struct.pack_into('<8sII', शीर्ष_मूल्य, 0, b'JKSTORE1', 2048, 0x3153464a)
        आउटपुट.write(शीर्ष_मूल्य)
        आउटपुट.truncate(2048 * 512)

if __name__ == '__main__':
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('मार्ग')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    प्रविष्टी_तयार_करा(बाबी.मार्ग)
