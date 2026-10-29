from English import SystemError, TryAgainError, openDatagram, receiveDatagram, closeNetwork, readFile, Output

endpoint = openDatagram(0)
try:
    try:
        receiveDatagram(endpoint)
        raise AssertionError("비어 있는 datagram 대기에서 예외가 필요합니다.")
    except SystemError as error:
        assert error.index == TryAgainError
        assert error.description == "OperatingSystem 작업에 실패했습니다."
        Output("English datagram exception verify")
finally:
    closeNetwork(endpoint)
try:
    readFile("/없는파일")
except SystemError as error:
    assert error.index == 2
    Output("English file exception verify")
else:
    raise AssertionError("file missingMethod 예외가 필요합니다.")
