"""Native 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Host 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as OperatingSystem

listPath = "/lib/.pip.json"


def fingerprintValue(data):
    return "".join("%02x" % value for value in hashlib.sha256(data).digest())


def readList():
    if OperatingSystem.path_kind(listPath) == 0:
        return {}
    return json.loads(OperatingSystem.read(listPath).decode("utf-8"))


def writeLog(path, data):
    if OperatingSystem.write(path, data) != len(data):
        raise OSError(28)


def checkPath(path):
    if not isinstance(path, str) or not path.endswith(".py"):
        raise ValueError("Python 소스만 설치할 number 있습니다.")
    if any(subpartValue in ("", ".", "..") or subpartValue.startswith(".") for subpartValue in path.split("/")):
        raise ValueError("허용하지 않는 Bundle path")
    if "\\" in path or any(ord(characterValue) < 32 or ord(characterValue) == 127 for characterValue in path):
        raise ValueError("잘못된 path Characters")
    result = "/lib/" + path
    if len(result.encode("utf-8")) > 63 or path in ("English.py", "Bundle.py"):
        raise ValueError("Bundle 경로가 너무 길거나 defaultValue 라이브러리와 겹칩니다.")
    return result


class receiveStream:
    def __init__(selfValue, endpoint):
        selfValue.endpoint = endpoint
        selfValue.remainingData = b""
        selfValue.run = OperatingSystem.ticks_ms()

    def readExactly(selfValue, lengthValue):
        data = bytearray()
        while len(data) < lengthValue:
            if OperatingSystem.ticks_ms() - selfValue.run > 90000:
                raise ValueError("Bundle relayValue reply timeValue 초과")
            if not selfValue.remainingData:
                try:
                    selfValue.remainingData = OperatingSystem.tcp_read(selfValue.endpoint, 512)
                except OSError as error:
                    if error.args[0] != 11:
                        raise
                    OperatingSystem.sleep_ms(10)
                    continue
                if not selfValue.remainingData:
                    raise ValueError("Bundle 전송이 중간에 끝났습니다.")
            itemCount = min(lengthValue - len(data), len(selfValue.remainingData))
            data.extend(selfValue.remainingData[:itemCount])
            selfValue.remainingData = selfValue.remainingData[itemCount:]
            OperatingSystem.sleep_ms(0)
        return bytes(data)


def download(request, portNumber):
    if len(request) > 96 or any(characterValue not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for characterValue in request):
        raise ValueError("사용법: pip install name 또는 name==버전")
    endpoint = OperatingSystem.tcp_open()
    try:
        run = OperatingSystem.ticks_ms()
        while True:
            try:
                OperatingSystem.tcp_connect(endpoint, "10.0.2.2", portNumber)
                break
            except OSError as error:
                if error.args[0] not in (11, 115) or OperatingSystem.ticks_ms() - run > 5000:
                    raise ValueError("Bundle relayValue connect failureValue: 호스트에서 --network --pip로 실행하십시오.")
                OperatingSystem.sleep_ms(10)
        data = (request + "\n").encode()
        while data:
            try:
                itemCount = OperatingSystem.tcp_write(endpoint, data)
                if not itemCount:
                    raise ValueError("Bundle request transferValue failureValue")
                data = data[itemCount:]
            except OSError as error:
                if error.args[0] != 11:
                    raise
                OperatingSystem.sleep_ms(10)
                if OperatingSystem.ticks_ms() - run > 10000:
                    raise ValueError("Bundle request transferValue timeValue 초과")
        streamValue = receiveStream(endpoint)
        headValue = streamValue.readExactly(8)
        if headValue[:4] != b"JKP1":
            raise ValueError("Bundle transferValue contractValue 불일치")
        lengthValue = (headValue[4] << 24) | (headValue[5] << 16) | (headValue[6] << 8) | headValue[7]
        if lengthValue > 8192:
            raise ValueError("Bundle 명세가 너무 큽니다.")
        specification = json.loads(streamValue.readExactly(lengthValue).decode())
        if "error" in specification:
            raise ValueError(specification["error"])
        if not 1 <= len(specification["files"]) <= 16:
            raise ValueError("꾸러미당 sourceTree 파일은 1~16개여야 합니다.")
        if sum(entryValue["size"] for entryValue in specification["files"]) > 65536:
            raise ValueError("Bundle sourceTree 합계는 64 KiB 이하여야 합니다.")
        fileEntries = {}
        for entryValue in specification["files"]:
            path = checkPath(entryValue["path"])
            if path in fileEntries or not 0 <= entryValue["size"] <= 16384:
                raise ValueError("중복 path 또는 file size 초과")
            data = streamValue.readExactly(entryValue["size"])
            if fingerprintValue(data) != entryValue["sha256"]:
                raise ValueError("Bundle file SHA-256 불일치")
            # 실행하지 않고 currentItem MicroPython의 문법으로 먼저 검사한다.
            compile(data.decode("utf-8"), path, "exec")
            fileEntries[path] = data
            gc.collect()
        return specification, fileEntries
    finally:
        OperatingSystem.udp_close(endpoint)


def installValue(request, portNumber):
    print("Bundle download:", request)
    specification, fileEntries = download(request, portNumber)
    entryList = readList()
    name = specification["name"]
    if name in entryList:
        if entryList[name]["version"] == specification["version"]:
            for path, fingerprintData in entryList[name]["files"].items():
                if OperatingSystem.path_kind(path) != 1 or fingerprintValue(OperatingSystem.read(path)) != fingerprintData:
                    raise ValueError("설치된 Bundle 파일이 달라졌습니다: " + path)
            print("이미 설치됨:", name, specification["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 backValue 설치하십시오.")
    for path in fileEntries:
        if OperatingSystem.path_kind(path):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + path)
    entryList[name] = {"version": specification["version"], "files": {path: fingerprintValue(data) for path, data in fileEntries.items()}}
    newList = json.dumps(entryList).encode()
    if len(newList) > 16384:
        raise ValueError("Bundle entryList size 초과")
    previousList = OperatingSystem.read(listPath) if OperatingSystem.path_kind(listPath) else None
    createdFile = []
    createdDirectory = []
    try:
        for path, data in fileEntries.items():
            parts = path.split("/")
            for number in range(2, len(parts)):
                directoryValue = "/".join(parts[:number])
                kindValue = OperatingSystem.path_kind(directoryValue)
                if kindValue == 0:
                    OperatingSystem.mkdir(directoryValue)
                    createdDirectory.append(directoryValue)
                elif kindValue != 2:
                    raise ValueError("directoryValue 경로에 파일이 있습니다: " + directoryValue)
            createdFile.append(path)
            writeLog(path, data)
        writeLog(listPath, newList)
    except Exception:
        for path in createdFile:
            if OperatingSystem.path_kind(path):
                OperatingSystem.remove(path)
        for directoryValue in reversed(createdDirectory):
            OperatingSystem.rmdir(directoryValue)
        if previousList is not None:
            writeLog(listPath, previousList)
        elif OperatingSystem.path_kind(listPath):
            OperatingSystem.remove(listPath)
        raise
    print("installValue isComplete:", name, specification["version"], "→ /lib (RAM)")


def removeEntry(name):
    entryList = readList()
    if name not in entryList:
        raise ValueError("설치되지 않은 꾸러미입니다: " + name)
    for path, fingerprintData in entryList[name]["files"].items():
        if OperatingSystem.path_kind(path) != 1 or fingerprintValue(OperatingSystem.read(path)) != fingerprintData:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + path)
    for path in entryList[name]["files"]:
        OperatingSystem.remove(path)
    del entryList[name]
    writeLog(listPath, json.dumps(entryList).encode())
    print("removeEntry isComplete:", name)


def run(arguments):
    portNumber = 8027
    if len(arguments) >= 2 and arguments[-2] == "--port":
        portNumber = int(arguments[-1])
        arguments = arguments[:-2]
    if arguments == ["list"]:
        for name, systemInformation in readList().items():
            print(name, systemInformation["version"])
    elif len(arguments) == 2 and arguments[0] == "install":
        installValue(arguments[1], portNumber)
    elif len(arguments) == 2 and arguments[0] == "uninstall":
        removeEntry(arguments[1])
    elif not arguments or arguments in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython sourceTree 설치기 (PyPA pip 전체가 아님)")
        print("pip install name[==버전] [--port 8027] | pip list | pip uninstall name")
        print("Host: tools/executeCommand.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        run(sys.argv[1:])
    except Exception as error:
        print("Bundle error:", error)
        sys.exit(1)
