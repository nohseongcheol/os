#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tempfile

position = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='jkoros-packet-test-') as temporaryValue:
    directoryValue = Path(temporaryValue)
    boundaryValue = directoryValue / '시험장치.java'
    boundaryValue.write_text('''
class deviceValue { static int timestampValue; static int milliseconds() { return timestampValue++; } static void yieldBriefly() {} }
class TextTerminal { static void write(String value) {} static void writeNumber(int value) {} }
class NetworkDeviceDriver {
    static int ioBaseAddress = 1, transmitCount, receiveCount;
    static int[] deviceAddress = {0x52,0x54,0,0x12,0x34,0x56}, recentValue;
    static int receive(int[] data) { return 0; }
    static int send(int[] data, int lengthValue) { recentValue = data.clone(); return lengthValue; }
}''', encoding='utf-8')
    subprocess.run(['javac', '-encoding', 'UTF-8', '-d', str(directoryValue), str(boundaryValue),
                    str(position / 'source/networkStack.java'), str(position / 'tests/PacketTest.java')], check=True)
    subprocess.run(['java', '-cp', str(directoryValue), 'PacketTest'], check=True, timeout=10)
