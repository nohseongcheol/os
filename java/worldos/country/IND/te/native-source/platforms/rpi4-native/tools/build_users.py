#!/usr/bin/env python3
"""기존 పాత్ 호환 ప్రవేశం_పాయింట్. వాస్తవ_డేటా 구현: ../ఉపకరణాలు/బిల్డ్_వినియోగదారు_ఖాళీ.py"""
import importlib as 가져오기
import sys as నిర్వహణా_వ్యవస్థ_మూల్యం
from pathlib import Path as పాత్
నిర్వహణా_వ్యవస్థ_మూల్యం.path.insert(0, str(పాత్(__file__).resolve().parents[1] / 'ఉపకరణాలు'))
if __name__ == '__main__':
    import runpy as అనువర్తనం_లాంచర్
    అనువర్తనం_లాంచర్.run_module('బిల్డ్_వినియోగదారు_ఖాళీ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('బిల్డ్_వినియోగదారు_ఖాళీ')
    대응 = {'mode': 'విధానం_మోడ్_3f5e5497', 'header': 'శీర్షిక_మూల్యం', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'ఆర్కైవ్_ఉపకరణం', 'posix': '포직스경로', 'payload': 'చెల్లింపుభారం_డేటా', 'flags': 'నిర్మితీకరణ_నేపథ్యంలో_తెలివైన_బదిలీ_సేవ', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'డేటా', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'రిపోజిటరీ_పథం', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'పాఠ్యము', 'headers': 'శీర్షిక_జాబితా', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'బిల్డ్', 'build_users': 'క్రియేట్_వినియోగదారు_ఖాళీ', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'అనువర్తనం_శీర్షిక_ఆఫ్_సెట్', 'offset': 'ఆఫ్_సెట్_మూల్యం', 'text_address': 'ఆదేశం_ఇమెయిల్', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'అమలు_చేయి_ఆదేశం', 'path': 'పాత్', 'p': 'డేటా_స్థాయి', 'changed': '바뀐자료', 'n': '개수', 'flag': 'సెట్టింగ్_లు_మూల్యం', 'index': 'అంశం_శోధన_సూచీ', 'classes': 'తరగతి_పథం', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'డేటా_ఇమెయిల్', 'symbol': 'చిహ్నం_మూల్యం', 'root': 'మూలం_ఇమెయిల్', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'పేరు', 'value': 'మూల్యం', 'fmt': 'ఆకృతి_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
