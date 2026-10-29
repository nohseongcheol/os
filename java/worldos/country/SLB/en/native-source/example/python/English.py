"""Native 커널의 file·communication·Screen 호출과 English exception. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as OperatingSystem
import sys as Runtime

def Output(*value, separator=" ", ending="\n", **legacyArguments):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in legacyArguments: legacyArguments["sep"] = separator
    if "end" not in legacyArguments: legacyArguments["end"] = ending
    print(*value, **legacyArguments)

Integer = int
commandArguments = Runtime.argv
TryAgainError = 11

class SystemError(OSError):
    def __init__(selfValue, index, description="OperatingSystem 작업에 실패했습니다."):
        super().__init__(index, description)
        selfValue.index = index
        selfValue.description = description

def invokeSystem(functionValue, *arguments):
    try:
        return functionValue(*arguments)
    except OSError as error:
        index = error.args[0] if error.args else 0
        raise SystemError(index)

def encodeText(text):
    return text.encode("utf-8")

def decodeText(data):
    return data.decode("utf-8")

def readFile(name):
    return invokeSystem(OperatingSystem.read, name)

def writeFile(name, data):
    return invokeSystem(OperatingSystem.write, name, data)

def removeFile(name):
    return invokeSystem(OperatingSystem.remove, name)

def openDatagram(portNumber):
    return invokeSystem(OperatingSystem.udp_open, portNumber)

def sendDatagram(endpoint, portNumber, data):
    return invokeSystem(OperatingSystem.udp_send, endpoint, portNumber, data)

def sendExternalDatagram(endpoint, address, portNumber, data):
    return invokeSystem(OperatingSystem.udp_sendto, endpoint, address, portNumber, data)

def receiveDatagram(endpoint):
    return invokeSystem(OperatingSystem.udp_recv, endpoint)

def closeNetwork(endpoint):
    return invokeSystem(OperatingSystem.udp_close, endpoint)

def drawRectangle(*arguments):
    return invokeSystem(OperatingSystem.rect, *arguments)

def screenSize():
    return invokeSystem(OperatingSystem.screen_size)

def waitForDrawing():
    return invokeSystem(OperatingSystem.wait_key)

milliseconds = OperatingSystem.ticks_ms
