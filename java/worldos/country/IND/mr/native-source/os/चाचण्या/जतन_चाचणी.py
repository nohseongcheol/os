#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 जतनकेलेले_इन्स्टन्स 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from प्रयोक्ता_संचारजाळे_चाचणी import व्हर्च्युअल_मशीन

जागा = Path(__file__).resolve().parents[1]
विनिर्देश = importlib.util.spec_from_file_location('माध्यमे_साधन', जागा / 'साधने/संग्रह_माध्यमे_तयार_करा.py')
माध्यमे_साधन = importlib.util.module_from_spec(विनिर्देश)
विनिर्देश.loader.exec_module(माध्यमे_साधन)

def संपादन_मूल्य(मशीन, सामुग्री_मूल्य):
    सुरू_करा = len(मशीन.लॉग_नोंद)
    मशीन.अनुक्रमिक_मूल्य.sendall(('edit note.txt\n' + सामुग्री_मूल्य + '\n.save\n').encode())
    return मशीन.प्रतीक्षा_करा_राज्य('jkoros> ', सुरू_करा)

def आज्ञा_कार्यवाही_करा():
    मोजमाप = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as तात्पुरते_मूल्य:
        माध्यमे_मूल्य = Path(तात्पुरते_मूल्य) / 'files.img'
        माध्यमे_साधन.प्रविष्टी_तयार_करा(माध्यमे_मूल्य)
        मशीन = व्हर्च्युअल_मशीन(जागा / 'build/kernel.elf', संग्रह_माध्यम=माध्यमे_मूल्य)
        try:
            मशीन.आदेश('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            संपादन_मूल्य(मशीन, 'generation-one')
            मशीन.आदेश('sync', ['Sync: 0'])
            संपादन_मूल्य(मशीन, 'generation-two')
            मशीन.आदेश('sync', ['Sync: 0'])
            संपादन_मूल्य(मशीन, 'unsynced-three')
            मोजमाप['save'] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        finally:
            मशीन.बंद_करा()
        मशीन = व्हर्च्युअल_मशीन(जागा / 'build/kernel.iso', 'iso', संग्रह_माध्यम=माध्यमे_मूल्य)
        try:
            आउटपुट = मशीन.आदेश('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in आउटपुट
            मशीन.आदेश('cat stored.txt', ['saved-from-C'])
            मोजमाप['restore'] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        finally:
            मशीन.बंद_करा()
        डेटा = bytearray(माध्यमे_मूल्य.read_bytes())
        पिढ्या_यादी = [struct.unpack_from('<I', डेटा, (1 + अनुक्रमणिका * 259) * 512 + 4)[0] for अनुक्रमणिका in (0, 1)]
        नवीनतम_मूल्य = 0 if पिढ्या_यादी[0] > पिढ्या_यादी[1] else 1
        डेटा[(1 + नवीनतम_मूल्य * 259 + 3) * 512] ^= 1
        माध्यमे_मूल्य.write_bytes(डेटा)
        मशीन = व्हर्च्युअल_मशीन(जागा / 'build/kernel.elf', संग्रह_माध्यम=माध्यमे_मूल्य)
        try:
            मशीन.आदेश('cat note.txt', ['generation-one'])
            मशीन.आदेश('cat stored.txt', ['saved-from-C'])
            मोजमाप['checksum_fallback'] = मशीन.लॉग_नोंद.decode('utf-8', 'replace')
        finally:
            मशीन.बंद_करा()
        दुसरे_माध्यमे = Path(तात्पुरते_मूल्य) / 'foreign.img'
        दुसरे_माध्यमे.write_bytes(bytes([0x5a]) * (2048 * 512))
        मागील_आयटम = hashlib.sha256(दुसरे_माध्यमे.read_bytes()).hexdigest()
        मशीन = व्हर्च्युअल_मशीन(जागा / 'build/kernel.elf', संग्रह_माध्यम=दुसरे_माध्यमे)
        try:
            मशीन.आदेश('sync', ['Sync: -19'])
        finally:
            मशीन.बंद_करा()
        assert hashlib.sha256(दुसरे_माध्यमे.read_bytes()).hexdigest() == मागील_आयटम
        मोजमाप['foreign_disk_unchanged'] = True
    (जागा / 'build/जतन_चाचणी.json').write_text(json.dumps(मोजमाप, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE साठवणे_मूल्य/ISO 재부팅/चेकसम पुनर्प्राप्त_करा_राज्य/다른 माध्यमे_मूल्य 비변경', flush=True)

if __name__ == '__main__':
    आज्ञा_कार्यवाही_करा()
