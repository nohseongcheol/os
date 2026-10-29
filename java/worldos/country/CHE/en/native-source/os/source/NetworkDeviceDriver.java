// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), one transmit buffer and an 8 KiB receive ring. Uses polling instead of interrupts. */
public final class NetworkDeviceDriver {
    static int ioBaseAddress = 0;
    static int receivePosition = 0, transmitSlot = 0;
    static int[] deviceAddress = new int[6];
    static int transmitCount = 0, receiveCount = 0, errorCount = 0;

    static int readSettings(int deviceNumber, int position) {
        deviceValue.writeIoInteger(0xcf8, 0x80000000 | (deviceNumber << 11) | position);
        return deviceValue.readIoInteger(0xcfc);
    }

    static boolean prepare() {
        int deviceNumber = -1;
        for (int index = 0; index < 32; index++) {
            if (readSettings(index, 0) == 0x813910ec) { deviceNumber = index; break; }
        }
        if (deviceNumber < 0) return false;
        int defaultValue = readSettings(deviceNumber, 0x10);
        if ((defaultValue & 1) == 0 || (defaultValue & 0xfffffffc) < 0x100 || (defaultValue & 0xfffffffc) > 65535) return false;
        ioBaseAddress = defaultValue & 0xfffc;
        int command = readSettings(deviceNumber, 4);
        deviceValue.writeIoInteger(0xcf8, 0x80000004 | (deviceNumber << 11));
        deviceValue.writeIoShort(0xcfc, command | 5); // Enable I/O and bus mastering; leave PCI status bits untouched.
        deviceValue.writeIoByte(ioBaseAddress + 0x52, 0);
        if (!resetValue()) { ioBaseAddress = 0; return false; }
        for (int index = 0; index < 6; index++) deviceAddress[index] = deviceValue.readIoByte(ioBaseAddress + index);
        return true;
    }

    static boolean resetValue() {
        deviceValue.writeIoByte(ioBaseAddress + 0x37, 0x10);
        int run = deviceValue.milliseconds();
        while ((deviceValue.readIoByte(ioBaseAddress + 0x37) & 0x10) != 0)
            if (deviceValue.milliseconds() - run > 100) return false;
        receivePosition = 0; transmitSlot = 0;
        deviceValue.writeIoInteger(ioBaseAddress + 0x30, deviceValue.networkMemory());
        for (int index = 0; index < 4; index++) deviceValue.writeIoInteger(ioBaseAddress + 0x20 + index * 4, deviceValue.networkMemory() + 12288);
        deviceValue.writeIoShort(ioBaseAddress + 0x3c, 0);
        deviceValue.writeIoShort(ioBaseAddress + 0x3e, 0xffff);
        deviceValue.writeIoByte(ioBaseAddress + 0x37, 0x0c);
        deviceValue.writeIoInteger(ioBaseAddress + 0x44, 0x0000e78a); // Accept own address and broadcast; contiguous wrap storage, 8 KiB.
        deviceValue.writeIoInteger(ioBaseAddress + 0x40, 0x03000600);
        return true;
    }

    static int send(int[] data, int lengthValue) {
        if (ioBaseAddress == 0) return -19;
        if (lengthValue < 14 || lengthValue > 1514) return -90;
        int statusPort = ioBaseAddress + 0x10 + transmitSlot * 4;
        int run = deviceValue.milliseconds();
        while ((deviceValue.readIoInteger(statusPort) & 0x2000) == 0)
            if (deviceValue.milliseconds() - run > 100) return -110;
        int size = lengthValue < 60 ? 60 : lengthValue;
        for (int index = 0; index < size; index++)
            deviceValue.writeMemory(deviceValue.networkMemory() + 12288 + index, index < lengthValue ? data[index] : 0);
        deviceValue.writeIoInteger(statusPort, size | 0x00080000);
        run = deviceValue.milliseconds();
        while ((deviceValue.readIoInteger(statusPort) & 0xe0008000) == 0)
            if (deviceValue.milliseconds() - run > 100) return -110;
        if ((deviceValue.readIoInteger(statusPort) & 0x8000) == 0) { errorCount++; return -5; }
        transmitSlot = (transmitSlot + 1) & 3;
        transmitCount++;
        return lengthValue;
    }

    static int receive(int[] data) {
        if (ioBaseAddress == 0) return 0;
        if ((deviceValue.readIoByte(ioBaseAddress + 0x3e) & 0x50) != 0) {
            errorCount++;
            if (!resetValue()) ioBaseAddress = 0;
            return 0;
        }
        if ((deviceValue.readIoByte(ioBaseAddress + 0x37) & 1) != 0) return 0;
        int headValue = deviceValue.networkMemory() + receivePosition;
        int stateValue = ExecutionManager.shortValue(headValue), size = ExecutionManager.shortValue(headValue + 2);
        if (size == 0xfff0) return 0; // DMA is in progress.
        if (size < 4 || size > 1518) {
            errorCount++;
            if (!resetValue()) ioBaseAddress = 0;
            return 0;
        }
        int lengthValue = size - 4;
        if ((stateValue & 1) != 0) {
            for (int index = 0; index < lengthValue; index++) data[index] = deviceValue.readMemory(headValue + 4 + index);
            receiveCount++;
        } else { lengthValue = 0; errorCount++; }
        receivePosition = (receivePosition + size + 4 + 3) & ~3;
        receivePosition &= 8191;
        deviceValue.writeIoShort(ioBaseAddress + 0x38, (receivePosition - 16) & 65535);
        deviceValue.writeIoShort(ioBaseAddress + 0x3e, 0x000f);
        return lengthValue;
    }
}
