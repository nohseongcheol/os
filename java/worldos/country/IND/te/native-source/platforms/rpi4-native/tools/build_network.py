#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/బిల్డ్_నెట్_వర్క్.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('బిల్డ్_నెట్_వర్క్', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('బిల్డ్_నెట్_వర్క్')
    대응 = {'obj': 'గమ్యఫైల్', 'objects': 'గమ్యం_ఫైల్_లు', 'library': 'లైబ్రరీ', 'output': '출력결과', 'port': 'పోర్ట్_సంఖ్య', 'root': 'మూలం_ఇమెయిల్', 'files': 'ఫైలు_జాబితా', 'source': '원본자료', 'run': 'అమలు_చేయి_ఆదేశం', 'flags': 'నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ', 'path': 'పాత్', 'build_network': 'క్రియేట్_నెట్_వర్క్', 'cc': '시언어번역기', 'ar': 'ఆర్కైవ్_ఉపకరణం'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
