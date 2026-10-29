// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Static IPv4/ARP/UDP. Stores at most four ports, with one datagram per port. */
public final class networkStack {
    static final int ownAddress = 0xc0a80064; /* ip.conf:IP */
    static final int networkMask = 0xffffff00; /* ip.conf:NETMASK */
    static final int gatewayValue = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] inputFrame = new int[1536], outputFrame = new int[1536];
    static int[] ports = new int[4], receivedLength = new int[4], receivedAddress = new int[4], receivedPortNumber = new int[4];
    static int[] receivedData = new int[4096], foundDevice = new int[6];
    static int addressToFind = 0, foundAddress = 0, identifierValue = 0, discardedCount = 0;

    static int integer16(int[] frameIndex, int position) { return (frameIndex[position] << 8) | frameIndex[position + 1]; }
    static int integer32(int[] frameIndex, int position) { return (integer16(frameIndex, position) << 16) | integer16(frameIndex, position + 2); }
    static void put16(int[] frameIndex, int position, int value) { frameIndex[position] = (value >>> 8) & 255; frameIndex[position + 1] = value & 255; }
    static void put32(int[] frameIndex, int position, int value) { put16(frameIndex, position, value >>> 16); put16(frameIndex, position + 2, value); }
    static int sumValue(int[] frameIndex, int run, int lengthValue, int value) {
        for (int index = 0; index < lengthValue; index += 2)
            value += (frameIndex[run + index] << 8) | (index + 1 < lengthValue ? frameIndex[run + index + 1] : 0);
        while ((value >>> 16) != 0) value = (value & 65535) + (value >>> 16);
        return value;
    }
    static int pseudoHeaderChecksum(int departureValue, int arrivalValue, int lengthValue) {
        return (departureValue >>> 16) + (departureValue & 65535) + (arrivalValue >>> 16) + (arrivalValue & 65535) + 17 + lengthValue;
    }

    static void cleanProcess() {
        for (int index = 0; index < 4; index++) {
            ports[index] = 0; receivedLength[index] = -1; receivedAddress[index] = 0; receivedPortNumber[index] = 0;
        }
        for (int index = 0; index < 64; index++) if (NetworkDeviceDriver.receive(inputFrame) == 0) break;
    }
    static int index(int handleValue) { return handleValue >= 3 && handleValue < 7 && ports[handleValue - 3] != 0 ? handleValue - 3 : -1; }
    static int open(int portNumber) {
        if (NetworkDeviceDriver.ioBaseAddress == 0) return -19;
        if (portNumber < 0 || portNumber > 65535) return -22;
        if (portNumber != 0) for (int index = 0; index < 4; index++) if (ports[index] == portNumber) return -98;
        for (int index = 0; index < 4; index++) if (ports[index] == 0) {
            if (portNumber == 0) {
                portNumber = 49152;
                boolean overlaps = true;
                while (overlaps) {
                    overlaps = false;
                    for (int frontValue = 0; frontValue < 4; frontValue++) if (ports[frontValue] == portNumber) overlaps = true;
                    if (overlaps) portNumber++;
                }
            }
            ports[index] = portNumber; receivedLength[index] = -1;
            return index + 3;
        }
        return -24;
    }
    static int close(int handleValue) {
        int slotEntry = index(handleValue);
        if (slotEntry < 0) return -9;
        ports[slotEntry] = 0; receivedLength[slotEntry] = -1;
        return 0;
    }
    static int peerAddress(int handleValue) { int slotEntry = index(handleValue); return slotEntry < 0 ? -9 : receivedAddress[slotEntry]; }
    static int peerPortNumber(int handleValue) { int slotEntry = index(handleValue); return slotEntry < 0 ? -9 : receivedPortNumber[slotEntry]; }

    static void outerHeader(int kindValue, boolean broadcastValue) {
        for (int index = 0; index < 6; index++) {
            outputFrame[index] = broadcastValue ? 255 : foundDevice[index];
            outputFrame[6 + index] = NetworkDeviceDriver.deviceAddress[index];
        }
        put16(outputFrame, 12, kindValue);
    }
    static void requestAddress(int destinationValue) {
        outerHeader(0x0806, true);
        put16(outputFrame, 14, 1); put16(outputFrame, 16, 0x0800);
        outputFrame[18] = 6; outputFrame[19] = 4; put16(outputFrame, 20, 1);
        for (int index = 0; index < 6; index++) {
            outputFrame[22 + index] = NetworkDeviceDriver.deviceAddress[index]; outputFrame[32 + index] = 0;
        }
        put32(outputFrame, 28, ownAddress); put32(outputFrame, 38, destinationValue);
        NetworkDeviceDriver.send(outputFrame, 42);
    }
    static void processAddress(int lengthValue) {
        if (lengthValue < 42 || integer16(inputFrame, 14) != 1 || integer16(inputFrame, 16) != 0x0800
            || inputFrame[18] != 6 || inputFrame[19] != 4 || integer32(inputFrame, 38) != ownAddress) { discardedCount++; return; }
        int kindValue = integer16(inputFrame, 20), peerValue = integer32(inputFrame, 28);
        if (kindValue == 2 && peerValue == addressToFind) {
            for (int index = 0; index < 6; index++) {
                if (inputFrame[6 + index] != inputFrame[22 + index] || inputFrame[32 + index] != NetworkDeviceDriver.deviceAddress[index]) return;
            }
            for (int index = 0; index < 6; index++) foundDevice[index] = inputFrame[22 + index];
            foundAddress = peerValue;
        } else if (kindValue == 1) {
            outerHeader(0x0806, false);
            put16(outputFrame, 14, 1); put16(outputFrame, 16, 0x0800);
            outputFrame[18] = 6; outputFrame[19] = 4; put16(outputFrame, 20, 2);
            for (int index = 0; index < 6; index++) {
                outputFrame[index] = inputFrame[22 + index]; outputFrame[32 + index] = inputFrame[22 + index];
                outputFrame[22 + index] = NetworkDeviceDriver.deviceAddress[index];
            }
            put32(outputFrame, 28, ownAddress); put32(outputFrame, 38, peerValue);
            NetworkDeviceDriver.send(outputFrame, 42);
        }
    }

    static void processFrame(int lengthValue) {
        if (lengthValue < 14 || lengthValue > inputFrame.length) { discardedCount++; return; }
        boolean selfReference = true, broadcastValue = true;
        for (int index = 0; index < 6; index++) {
            if (inputFrame[index] != NetworkDeviceDriver.deviceAddress[index]) selfReference = false;
            if (inputFrame[index] != 255) broadcastValue = false;
        }
        if (!selfReference && !broadcastValue) return;
        if (integer16(inputFrame, 12) == 0x0806) { processAddress(lengthValue); return; }
        if (integer16(inputFrame, 12) != 0x0800) return;
        if (lengthValue < 34 || (inputFrame[14] >>> 4) != 4) { discardedCount++; return; }
        int headerLength = (inputFrame[14] & 15) * 4, totalLength = integer16(inputFrame, 16);
        if (headerLength < 20 || headerLength > 60 || totalLength < headerLength + 8 || totalLength > lengthValue - 14
            || (integer16(inputFrame, 20) & 0x3fff) != 0 || inputFrame[23] != 17
            || integer32(inputFrame, 30) != ownAddress || sumValue(inputFrame, 14, headerLength, 0) != 65535) { discardedCount++; return; }
        int run = 14 + headerLength, dataLength = integer16(inputFrame, run + 4);
        if (dataLength < 8 || dataLength != totalLength - headerLength || dataLength > 1032) { discardedCount++; return; }
        int departureValue = integer32(inputFrame, 26);
        if (integer16(inputFrame, run + 6) != 0 && sumValue(inputFrame, run, dataLength, pseudoHeaderChecksum(departureValue, ownAddress, dataLength)) != 65535) {
            discardedCount++; return;
        }
        int destinationValue = integer16(inputFrame, run + 2);
        for (int slotEntry = 0; slotEntry < 4; slotEntry++) if (ports[slotEntry] != 0 && ports[slotEntry] == destinationValue) {
            if (receivedLength[slotEntry] >= 0) { discardedCount++; return; }
            receivedLength[slotEntry] = dataLength - 8; receivedAddress[slotEntry] = departureValue; receivedPortNumber[slotEntry] = integer16(inputFrame, run);
            for (int index = 0; index < dataLength - 8; index++) receivedData[slotEntry * 1024 + index] = inputFrame[run + 8 + index];
            return;
        }
    }

    static void verify() {
        for (int index = 0; index < 16; index++) {
            int lengthValue = NetworkDeviceDriver.receive(inputFrame);
            if (lengthValue == 0) return;
            processFrame(lengthValue);
        }
    }
    static int findAddress(int address) {
        if (address == 0 || address == -1 || (address >>> 28) >= 14 || (address >>> 24) == 127 || address == ownAddress) return -101;
        int nextItem = (address & networkMask) == (ownAddress & networkMask) ? address : gatewayValue;
        if (nextItem == foundAddress) return 0;
        addressToFind = nextItem;
        int run = deviceValue.milliseconds(), nextRequest = run;
        while (deviceValue.milliseconds() - run < 1000) {
            if (deviceValue.milliseconds() - nextRequest >= 0) { requestAddress(nextItem); nextRequest += 300; }
            verify();
            if (foundAddress == nextItem) return 0;
            deviceValue.yieldBriefly();
        }
        return -110;
    }
    static int send(int handleValue, int address, int portNumber, int[] data, int lengthValue) {
        int slotEntry = index(handleValue);
        if (slotEntry < 0) return -9;
        if (NetworkDeviceDriver.ioBaseAddress == 0) return -19;
        if (portNumber < 1 || portNumber > 65535 || lengthValue < 0 || lengthValue > 1024) return -22;
        int result = findAddress(address);
        if (result < 0) return result;
        outerHeader(0x0800, false);
        outputFrame[14] = 0x45; outputFrame[15] = 0; put16(outputFrame, 16, 28 + lengthValue);
        put16(outputFrame, 18, identifierValue++); put16(outputFrame, 20, 0x4000);
        outputFrame[22] = 64; outputFrame[23] = 17; put16(outputFrame, 24, 0);
        put32(outputFrame, 26, ownAddress); put32(outputFrame, 30, address);
        put16(outputFrame, 24, ~sumValue(outputFrame, 14, 20, 0));
        put16(outputFrame, 34, ports[slotEntry]); put16(outputFrame, 36, portNumber);
        put16(outputFrame, 38, lengthValue + 8); put16(outputFrame, 40, 0);
        for (int index = 0; index < lengthValue; index++) outputFrame[42 + index] = data[index] & 255;
        int checksum = (~sumValue(outputFrame, 34, lengthValue + 8, pseudoHeaderChecksum(ownAddress, address, lengthValue + 8))) & 65535;
        put16(outputFrame, 40, checksum == 0 ? 65535 : checksum);
        result = NetworkDeviceDriver.send(outputFrame, lengthValue + 42);
        return result < 0 ? result : lengthValue;
    }
    static int receive(int handleValue, int[] data, int capacityValue, int limitValue) {
        int slotEntry = index(handleValue);
        if (slotEntry < 0) return -9;
        int run = deviceValue.milliseconds();
        while (true) {
            verify();
            int lengthValue = receivedLength[slotEntry];
            if (lengthValue >= 0) {
                receivedLength[slotEntry] = -1;
                if (lengthValue > capacityValue) return -90;
                for (int index = 0; index < lengthValue; index++) data[index] = receivedData[slotEntry * 1024 + index];
                return lengthValue;
            }
            if (limitValue == 0) return -11;
            if (deviceValue.milliseconds() - run >= limitValue) return -110;
            deviceValue.yieldBriefly();
        }
    }
    static void stateValue() {
        TextTerminal.write(NetworkDeviceDriver.ioBaseAddress == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        TextTerminal.write("TX: "); TextTerminal.writeNumber(NetworkDeviceDriver.transmitCount);
        TextTerminal.write(" RX: "); TextTerminal.writeNumber(NetworkDeviceDriver.receiveCount);
        TextTerminal.write(" DROP: "); TextTerminal.writeNumber(discardedCount);
        TextTerminal.write("\n");
    }
}
