#!/usr/bin/env python3
"""Validate packaging independence and compile every localized native header."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    editions=json.loads((ROOT/'editions.json').read_text(encoding='utf-8'))
    generated=json.loads((ROOT/'naming/generated-files.json').read_text(encoding='utf-8'))
    failures=[]
    for name,digest in generated.items():
        path=ROOT/name
        if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:failures.append(name)
    if failures:raise SystemExit('Generated sources changed or missing: '+repr(failures[:20]))
    for edition in editions:
        root=ROOT/edition['path']
        with zipfile.ZipFile(str(root/'build/edition.jar')) as archive:
            prefix=edition['main'].rsplit('.',1)[0].replace('.','/')+'/'
            classes=[name for name in archive.namelist() if name.endswith('.class')]
            if not classes or any(not name.startswith(prefix) for name in classes):raise AssertionError('Foreign or missing classes: '+edition['path'])
            if edition['main'].replace('.','/')+'.class' not in classes:raise AssertionError('Missing main: '+edition['path'])
    with tempfile.TemporaryDirectory(prefix='worldos-headers-') as temporary:
        filesystem=ROOT/'build/rootfs'
        cc1=next((filesystem/'usr/libexec/gcc').glob('*/*/cc1'))
        compiler_include=next((filesystem/'usr/lib/gcc').glob('*/*/include'))
        command=[str(filesystem/'lib/ld-musl-x86_64.so.1'),'--library-path',str(filesystem/'lib')+':'+str(filesystem/'usr/lib'),str(cc1),
                 '-std=c11','-quiet','-nostdinc','-isystem',str(compiler_include),'-isystem',str(filesystem/'usr/include'),
                 '-Werror=implicit-function-declaration','-fsyntax-only']
        for start in range(0,len(editions),100):
            lines=[]
            for index,edition in enumerate(editions[start:start+100]):
                root=ROOT/edition['path'];names=edition['identifiers']
                # Inline separate headers for this aggregate syntax check:
                # GCC can coalesce byte-identical #pragma once headers.
                lines.append((root/edition['posix']).read_text().replace('#pragma once',''))
                lines.append('int native_check_'+str(index)+'(void) { return '+names['open']+'("/tmp/worldos", O_RDONLY); }')
                for line in (root/edition['posix']).read_text().splitlines():
                    if line.startswith('#define '):lines.append('#undef '+line.split()[1])
            source=Path(temporary)/'headers.c';source.write_text('\n'.join(lines)+'\n',encoding='utf-8')
            subprocess.run(command+[str(source)],check=True)
    report={'countries':len({e['country'] for e in editions}),'editions':len(editions),'isolated_jars':len(editions),'native_headers_compiled':len(editions),'generated_files_verified':len(generated)}
    (ROOT/'build/edition-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
