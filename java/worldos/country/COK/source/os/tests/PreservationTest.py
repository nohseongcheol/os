#!/usr/bin/env python3
"""fsync, 재부팅, 미동기화 손실, 손상 preservedCopy 회피, 다른 디스크 비변경을 검사한다."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
from testUserNetwork import VirtualMachine

position = Path(__file__).resolve().parents[1]
specification = importlib.util.spec_from_file_location('mediaTool', position / 'tools/createStorageMedia.py')
mediaTool = importlib.util.module_from_spec(specification)
specification.loader.exec_module(mediaTool)

def editValue(machine, contentValue):
    run = len(machine.logRecord)
    machine.serialValue.sendall(('edit note.txt\n' + contentValue + '\n.save\n').encode())
    return machine.waitState('jkoros> ', run)

def executeCommand():
    result = {}
    with tempfile.TemporaryDirectory(prefix='jkoros-store-') as temporaryValue:
        mediaValue = Path(temporaryValue) / 'files.img'
        mediaTool.createEntry(mediaValue)
        machine = VirtualMachine(position / 'build/kernel.elf', storageMedium=mediaValue)
        try:
            machine.command('run posixstore', ['POSIX FSYNC PASS', 'Exit: 0'])
            editValue(machine, 'generation-one')
            machine.command('sync', ['Sync: 0'])
            editValue(machine, 'generation-two')
            machine.command('sync', ['Sync: 0'])
            editValue(machine, 'unsynced-three')
            result['save'] = machine.logRecord.decode('utf-8', 'replace')
        finally:
            machine.close()
        machine = VirtualMachine(position / 'build/kernel.iso', 'iso', storageMedium=mediaValue)
        try:
            Output = machine.command('cat note.txt', ['generation-two'])
            assert 'unsynced-three' not in Output
            machine.command('cat stored.txt', ['saved-from-C'])
            result['restore'] = machine.logRecord.decode('utf-8', 'replace')
        finally:
            machine.close()
        data = bytearray(mediaValue.read_bytes())
        generationsList = [struct.unpack_from('<I', data, (1 + index * 259) * 512 + 4)[0] for index in (0, 1)]
        latestValue = 0 if generationsList[0] > generationsList[1] else 1
        data[(1 + latestValue * 259 + 3) * 512] ^= 1
        mediaValue.write_bytes(data)
        machine = VirtualMachine(position / 'build/kernel.elf', storageMedium=mediaValue)
        try:
            machine.command('cat note.txt', ['generation-one'])
            machine.command('cat stored.txt', ['saved-from-C'])
            result['checksum_fallback'] = machine.logRecord.decode('utf-8', 'replace')
        finally:
            machine.close()
        otherMedia = Path(temporaryValue) / 'foreign.img'
        otherMedia.write_bytes(bytes([0x5a]) * (2048 * 512))
        previousItem = hashlib.sha256(otherMedia.read_bytes()).hexdigest()
        machine = VirtualMachine(position / 'build/kernel.elf', storageMedium=otherMedia)
        try:
            machine.command('sync', ['Sync: -19'])
        finally:
            machine.close()
        assert hashlib.sha256(otherMedia.read_bytes()).hexdigest() == previousItem
        result['foreign_disk_unchanged'] = True
    (position / 'build/PreservationTest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print('PASS: POSIX fsync/IDE storeValue/ISO 재부팅/checksum recoverState/다른 mediaValue 비변경', flush=True)

if __name__ == '__main__':
    executeCommand()
