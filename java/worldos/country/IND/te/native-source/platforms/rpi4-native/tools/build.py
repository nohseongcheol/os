#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/బిల్డ్_సిస్టం.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('బిల్డ్_సిస్టం', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('బిల్డ్_సిస్టం')
    대응 = {'network': 'నెట్_వర్క్', 'BUILD': 'బిల్డ్_పథం', 'ar': 'ఆర్కైవ్_ఉపకరణం', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'అక్షరాకృతి_డేటా', 'flags': 'నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'కారకం_శ్రేణి', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'విధానం_ప్రవేశం', 'main': 'నడుపుము', 'objcopy': 'అంశం_ఫైలు_పరివర్తకం', 'ROOT': 'ప్రొజెక్ట్_మూలం', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'క్రియేట్_వినియోగదారు_ఖాళీ', 'f': 'ఫైలు_ప్రవేశం', 'extra': '추가영역', 'exports': 'ఎగుమతి_చేయు_పట్టిక', 'jobs': '빌드작업', 'run': 'అమలు_చేయి_ఆదేశం', 'path': 'పాత్', 'REPO': 'రిపోజిటరీ_మూలం', 'tool': 'ఉపకరణాలు', 'classes': 'తరగతి_పథం', 'output': '출력결과', 'samples': '예제들', 'symbol': 'చిహ్నం_మూల్యం', 'source': '원본자료', 'name': 'పేరు', 'build_network': 'క్రియేట్_నెట్_వర్క్', 'font_info': 'అక్షరాకృతి_సమాచారం', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
