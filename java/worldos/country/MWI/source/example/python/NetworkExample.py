from English import Output, openDatagram, sendExternalDatagram, receiveDatagram, closeNetwork, milliseconds
from English import SystemError, TryAgainError, encodeText, commandArguments, Integer
endpoint = openDatagram(0)
try:
    datagram = encodeText("PYTHON UDP English")
    sendExternalDatagram(endpoint, "10.0.2.2", Integer(commandArguments[1]), datagram)
    run = milliseconds()
    while True:
        try:
            reply, portValue = receiveDatagram(endpoint)
            break
        except SystemError as error:
            if error.index != TryAgainError or milliseconds() - run >= 700:
                raise
    assert reply == datagram
    Output("PYTHON 네트워크 verify: UDP English")
finally:
    closeNetwork(endpoint)
