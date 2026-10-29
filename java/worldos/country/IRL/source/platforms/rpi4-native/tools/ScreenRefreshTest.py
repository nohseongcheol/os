#!/usr/bin/env python3
"""actualData kernelValue paintScreen 코드를 Host memoryData 화면에 연결해 subpartValue 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

projectRoot = Path(__file__).resolve().parents[1]

def run():
    sourceFiles = ['tests/refreshScreen.c', 'machine/screenDrawing.c', 'machine/terminal.c', 'machine/Widget.c']
    validationSources = sourceFiles + ['source/FramebufferComposer.java', 'source/Board.java', '../../compiler/JavaTools/AheadOfTimeCompiler.java']
    destinationValue = projectRoot/'build/verification/redraw'; destinationValue.mkdir(parents=True, exist_ok=True)
    logRecord = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {name: hashlib.sha256((projectRoot/name).read_bytes()).hexdigest() for name in validationSources}}
    try:
        classPath = destinationValue/'classes'; classPath.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(classPath),
            str(projectRoot/'source/FramebufferComposer.java'), str(projectRoot/'source/Board.java')])
        exportTable = {'jdraw_prepare': 'prepare', 'jdraw_width': 'getWidth', 'jdraw_height': 'getHeight',
            'jdraw_count_low': 'getCounterLow', 'jdraw_count_high': 'getCounterHigh', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clipValue', 'jdraw_begin': 'run', 'jdraw_end': 'finish',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'rectangleFill', 'jdraw_pointer': 'pointer'}
        compilationCommand = ['sh', str(projectRoot.parents[1]/'compiler/aheadOfTime.sh'), '--entry', 'FramebufferComposer.getWidth', '-o', str(destinationValue/'drawingValue.c')]
        for connect, functionValue in exportTable.items(): compilationCommand.extend(['--export', connect+'=FramebufferComposer.'+functionValue])
        subprocess.check_call(compilationCommand+[str(path) for path in sorted(classPath.glob('*.class'))])
        command = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + sourceFiles
        drawingDestination = destinationValue/'drawingValue.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destinationValue/'drawingValue.c'), '-o', str(drawingDestination)])
        subprocess.check_call(command+[str(drawingDestination), 'build/terminal-font.S', '-o', str(destinationValue/'ScreenRefreshTest')], cwd=str(projectRoot))
        result = subprocess.check_output([str(destinationValue/'ScreenRefreshTest')], timeout=30).decode()
        (destinationValue/'validate.log').write_text(result)
        isMatched = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', result)
        assert isMatched and 'PASS:' in result, result
        logRecord.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(isMatched[1]), mean_framebuffer_writes_per_move=int(isMatched[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(result, end='')
    finally:
        (destinationValue/'report.json').write_text(json.dumps(logRecord, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': run()
