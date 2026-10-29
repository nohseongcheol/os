#!/usr/bin/env python3
"""thêmCuốiMục Python 패키지 없이 tiếngViệt Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def sốLượngĐiểmMã(giáTrịNộiDung, thưViện, thưMụcLớp):
    kếtQuả = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(thưViện), str(thưMụcLớp)]), 'LệnhVănBản', giáTrịNộiDung],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(kếtQuả.stdout.strip())


if __name__ == '__main__':
    phânTíchCúPhápCácĐốiSố = argparse.ArgumentParser(description=__doc__)
    phânTíchCúPhápCácĐốiSố.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/JavaTiếngViệt.jar'))
    phânTíchCúPhápCácĐốiSố.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    phânTíchCúPhápCácĐốiSố.add_argument('--text', default='한글 😀')
    cácĐốiSố = phânTíchCúPhápCácĐốiSố.parse_args()
    print('Python → tiếngViệt.Java.KýTự.sốLượngĐiểmMã:',
          sốLượngĐiểmMã(cácĐốiSố.text, cácĐốiSố.jar, cácĐốiSố.classes))
