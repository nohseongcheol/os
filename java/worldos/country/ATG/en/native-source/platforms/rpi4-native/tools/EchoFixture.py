"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class EchoFixture:
    def __enter__(selfValue):
        selfValue.connectionControl = socket.socket(); selfValue.connectionControl.bind(('127.0.0.1', 0)); selfValue.connectionControl.listen(1)
        selfValue.datagramControl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); selfValue.datagramControl.bind(('127.0.0.1', 0))
        selfValue.connectionControl.settimeout(30); selfValue.datagramControl.settimeout(30)
        selfValue.tcpPort = selfValue.connectionControl.getsockname()[1]; selfValue.udpPort = selfValue.datagramControl.getsockname()[1]
        selfValue.errors = []; selfValue.hasReceived = {}
        def connectionControl():
            try:
                connection, _ = selfValue.connectionControl.accept()
                with connection:
                    connection.settimeout(5); data = bytearray()
                    while b'\n' not in data:
                        fragmentValue = connection.recv(512)
                        if not fragmentValue: raise RuntimeError('TCP EOF before request')
                        data.extend(fragmentValue)
                    selfValue.hasReceived['tcp'] = bytes(data); connection.sendall(data)
            except Exception as auxiliaryEntry: selfValue.errors.append(str(auxiliaryEntry))
        def datagramControl():
            try:
                data, peerValue = selfValue.datagramControl.recvfrom(512); selfValue.hasReceived['udp'] = data; selfValue.datagramControl.sendto(data, peerValue)
            except Exception as auxiliaryEntry: selfValue.errors.append(str(auxiliaryEntry))
        selfValue.threads = [threading.Thread(target=fileEntry, daemon=True) for fileEntry in (connectionControl, datagramControl)]
        for terminalEntry in selfValue.threads: terminalEntry.start()
        return selfValue

    def __exit__(selfValue, *argumentArray):
        selfValue.connectionControl.close(); selfValue.datagramControl.close()
        for terminalEntry in selfValue.threads: terminalEntry.join(timeout=1)
