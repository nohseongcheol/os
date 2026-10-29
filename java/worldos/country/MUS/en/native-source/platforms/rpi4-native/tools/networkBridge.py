"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

machineAddress = bytes.fromhex('525400123456')
gatewayHardwareAddress = bytes.fromhex('52550a000202')
internetAddressValue = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class networkBridge:
    def __init__(selfValue, fileTransferPortNumber=2121, forwardingRules=(), capture=False, guestAddress=None, hostAddress='127.0.0.1'):
        if not 1024 <= fileTransferPortNumber <= 65535 or 50000 <= fileTransferPortNumber <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        selfValue.fileTransferPortNumber = fileTransferPortNumber
        selfValue.ip_config = read_config(Path(__file__).resolve().parents[1])
        guestAddress = guestAddress or selfValue.ip_config['IP']
        qemu_network(selfValue.ip_config, guestAddress)
        address=ipaddress.IPv4Address(guestAddress)
        selfValue.guestAddress=str(address); selfValue.currentAddress=address.packed
        address=ipaddress.IPv4Address(hostAddress)
        if address.is_multicast or str(address)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        selfValue.hostAddress=str(address)
        selfValue.capture = capture; selfValue.traceLog = []
        selfValue.forwardingRules = []
        occupied = {('tcp', fileTransferPortNumber)} | {('tcp', dataPosition) for dataPosition in range(50000,50008)}
        for ruleValue in forwardingRules:
            pathComponent = ruleValue.split(':')
            if len(pathComponent) != 3 or pathComponent[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            NetworkABI, Host, guest = pathComponent[0], int(pathComponent[1]), int(pathComponent[2])
            if not 1024 <= Host <= 65535 or not 1 <= guest <= 65535 or (NetworkABI, Host) in occupied:
                raise ValueError('invalid or duplicate forward: ' + ruleValue)
            occupied.add((NetworkABI, Host)); selfValue.forwardingRules.append((NetworkABI, Host, guest))
        selfValue.receivePorts = []
        for _ in range(2):
            serverValue = socket.socket()
            serverValue.bind(('127.0.0.1', 0)); serverValue.listen(1); serverValue.setblocking(False)
            selfValue.receivePorts.append(serverValue)
        selfValue.clients = [None, None]
        selfValue.isPending = [bytearray(), bytearray()]
        selfValue.ethernet = bytearray(); selfValue.serialDatagram = bytearray(); selfValue.escaped = selfValue.isInvalid = False
        selfValue.pauseEvent = threading.Event(); selfValue.error = None
        selfValue.framesToGuest = selfValue.framesFromGuest = 0
        selfValue.worker = threading.Thread(target=selfValue.cycleValue, daemon=True)
        selfValue.worker.start()

    def forwardedArgument(selfValue):
        serialPortNumber, ethernetPort = [stringData.getsockname()[1] for stringData in selfValue.receivePorts]
        forwardingRule = 'user,id=wan,' + qemu_network(selfValue.ip_config, selfValue.guestAddress) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(selfValue.fileTransferPortNumber, selfValue.guestAddress)
        for portNumber in range(50000, 50008):
            forwardingRule += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(portNumber, selfValue.guestAddress)
        for NetworkABI, Host, guest in selfValue.forwardingRules:
            forwardingRule += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(NetworkABI, Host, selfValue.guestAddress, guest)
        forwardingRule=forwardingRule.replace('127.0.0.1:',selfValue.hostAddress+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(serialPortNumber),
                '-serial', 'chardev:slip', '-netdev', forwardingRule,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(ethernetPort),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def executionFrame(selfValue, packetData):
        selfValue.isPending[1] += struct.pack('!I', len(packetData)) + packetData

    def tracePacket(selfValue, direction, packetData):
        if not selfValue.capture or len(packetData)<20: return
        offsetValue=(packetData[0]&15)*4
        entryValue={'time':time.monotonic(),'direction':direction,'bytes':len(packetData),'protocol':packetData[9]}
        if packetData[9]==6 and len(packetData)>=offsetValue+20:
            originalData,destinationDataAddress,orderNumber,confirmationNumber,configurationBits,window=struct.unpack_from('!HHIIHH',packetData,offsetValue)
            entryValue.update(source=originalData,destination=destinationDataAddress,seq=orderNumber,ack=confirmationNumber,flags=configurationBits&255,window=window,
                        payload=len(packetData)-offsetValue-((packetData[offsetValue+12]>>4)*4))
        selfValue.traceLog.append(entryValue)
        if len(selfValue.traceLog)>2048: del selfValue.traceLog[:1024]

    def slipInput(selfValue, data):
        for characterCode in data:
            if characterCode == 192:
                if selfValue.serialDatagram and not selfValue.isInvalid and not selfValue.escaped:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(selfValue.serialDatagram)>=20 and selfValue.serialDatagram[0]>>4==4:
                        address=bytes(selfValue.serialDatagram[12:16])
                        try:
                            qemu_network(selfValue.ip_config, str(ipaddress.IPv4Address(address)))
                            selfValue.currentAddress=address
                        except ValueError:
                            pass
                    selfValue.tracePacket('from_guest',selfValue.serialDatagram)
                    selfValue.executionFrame(gatewayHardwareAddress + machineAddress + b'\x08\x00' + selfValue.serialDatagram)
                    selfValue.framesFromGuest += 1
                selfValue.serialDatagram.clear(); selfValue.escaped = selfValue.isInvalid = False
            elif characterCode == 219 and not selfValue.escaped:
                selfValue.escaped = True
            else:
                if selfValue.escaped:
                    if characterCode not in (220, 221): selfValue.isInvalid = True
                    characterCode = 192 if characterCode == 220 else 219
                    selfValue.escaped = False
                if len(selfValue.serialDatagram) < 1600: selfValue.serialDatagram.append(characterCode)
                else: selfValue.isInvalid = True

    def ethernetInput(selfValue, data):
        selfValue.ethernet += data
        while len(selfValue.ethernet) >= 4:
            itemCount = struct.unpack_from('!I', selfValue.ethernet)[0]
            if itemCount > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(selfValue.ethernet) < itemCount + 4: return
            executionFrame = bytes(selfValue.ethernet[4:4+itemCount]); del selfValue.ethernet[:4+itemCount]
            if len(executionFrame) < 14: continue
            if executionFrame[12:14] == b'\x08\x06' and len(executionFrame) >= 42:
                addressResolutionPacket = executionFrame[14:42]
                if addressResolutionPacket[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and addressResolutionPacket[24:28] == selfValue.currentAddress:
                    response = addressResolutionPacket[:6] + b'\x00\x02' + machineAddress + selfValue.currentAddress + addressResolutionPacket[8:18]
                    selfValue.executionFrame(executionFrame[6:12] + machineAddress + b'\x08\x06' + response)
            elif executionFrame[12:14] == b'\x08\x00':
                packetData = executionFrame[14:]
                selfValue.tracePacket('to_guest',packetData)
                selfValue.isPending[0] += b'\xc0' + packetData.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                selfValue.framesToGuest += 1

    def cycleValue(selfValue):
        try:
            while not selfValue.pauseEvent.is_set():
                readers = [stringData for ordinalIndex, stringData in enumerate(selfValue.receivePorts) if selfValue.clients[ordinalIndex] is None]
                readers += [stringData for stringData in selfValue.clients if stringData is not None]
                writers = [stringData for ordinalIndex, stringData in enumerate(selfValue.clients) if stringData is not None and selfValue.isPending[ordinalIndex]]
                canRead, writable, _ = select.select(readers, writers, [], .05)
                for stringData in canRead:
                    if stringData in selfValue.receivePorts:
                        ordinalIndex = selfValue.receivePorts.index(stringData); selfValue.clients[ordinalIndex], _ = stringData.accept(); selfValue.clients[ordinalIndex].setblocking(False)
                    else:
                        ordinalIndex = selfValue.clients.index(stringData); data = stringData.recv(16384)
                        if not data: return
                        (selfValue.slipInput if ordinalIndex == 0 else selfValue.ethernetInput)(data)
                for stringData in writable:
                    ordinalIndex = selfValue.clients.index(stringData)
                    try: itemCount = stringData.send(selfValue.isPending[ordinalIndex])
                    except BlockingIOError: continue
                    del selfValue.isPending[ordinalIndex][:itemCount]
                if any(len(secondValue) > 1024 * 1024 for secondValue in selfValue.isPending):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as auxiliaryEntry:
            if not selfValue.pauseEvent.is_set(): selfValue.error = str(auxiliaryEntry)

    def close(selfValue):
        selfValue.pauseEvent.set(); selfValue.worker.join(timeout=2)
        for stringData in selfValue.receivePorts + selfValue.clients:
            if stringData is not None: stringData.close()

    def __enter__(selfValue): return selfValue
    def __exit__(selfValue, *argumentArray): selfValue.close()
