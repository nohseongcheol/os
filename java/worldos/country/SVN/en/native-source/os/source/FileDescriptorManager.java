// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Separates a single user process's file descriptors from open-file descriptions. Call numbers are documented in the POSIX ABI. */
public final class FileDescriptorManager {
    static final int descriptorLimit = 32;
    static final int readWriteFlag = 2, createEntry = 64, createExclusively = 128, clearContents = 512;
    static final int appendContinuation = 1024, doNotWait = 2048, closeOnExec = 524288;
    static int[] openHandle = new int[descriptorLimit], setDescriptor = new int[descriptorLimit];
    static int[] kindValue = new int[descriptorLimit], targetValue = new int[descriptorLimit];
    static int[] filePosition = new int[descriptorLimit], openSettings = new int[descriptorLimit], referenceCount = new int[descriptorLimit];
    static int[] networkHandle = new int[descriptorLimit], receiveTimeoutMilliseconds = new int[descriptorLimit];
    static int[] pathName = new int[64], transferData = new int[1024];

    static int findDescriptor(int fileDescriptor) {
        if (fileDescriptor < 0 || fileDescriptor >= descriptorLimit) return -9;
        return openHandle[fileDescriptor] - 1;
    }
    static int emptyDescriptor(int run) {
        for (int index = run; index < descriptorLimit; index++) if (openHandle[index] == 0) return index;
        return -24;
    }
    static int emptyHandle() {
        for (int index = 0; index < descriptorLimit; index++) if (referenceCount[index] == 0) return index;
        return -24;
    }
    static int connect(int descriptorEntry, int descriptorValue, int fileKind, int fileTargetValue, int settings) {
        openHandle[descriptorEntry] = descriptorValue + 1; setDescriptor[descriptorEntry] = (settings & closeOnExec) != 0 ? 1 : 0;
        kindValue[descriptorValue] = fileKind; targetValue[descriptorValue] = fileTargetValue; referenceCount[descriptorValue] = 1;
        openSettings[descriptorValue] = settings & (3 | appendContinuation | doNotWait); filePosition[descriptorValue] = 0;
        networkHandle[descriptorValue] = 0; receiveTimeoutMilliseconds[descriptorValue] = 0;
        return descriptorEntry;
    }
    static void startProcess() {
        cleanProcess();
        for (int index = 0; index < 3; index++) connect(index, index, 1, index, index == 0 ? 0 : 1);
    }
    static void cleanProcess() {
        for (int index = 0; index < descriptorLimit; index++) if (openHandle[index] != 0) closeFile(index);
    }
    static int closeFile(int descriptorEntry) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        openHandle[descriptorEntry] = 0; setDescriptor[descriptorEntry] = 0;
        referenceCount[descriptorValue]--;
        if (referenceCount[descriptorValue] == 0) {
            if (kindValue[descriptorValue] == 2) MemoryFileSystem.openCount[targetValue[descriptorValue]]--;
            if (kindValue[descriptorValue] == 3 && networkHandle[descriptorValue] != 0) networkStack.close(networkHandle[descriptorValue]);
            kindValue[descriptorValue] = 0;
        }
        return 0;
    }
    // C paths are NUL-terminated byte strings. Only one name directly under the root is supported.
    static int readPath(int address) {
        if (!ExecutionManager.clip(address, 1)) return -14;
        int position = deviceValue.readMemory(address) == '/' ? 1 : 0;
        for (int lengthValue = 0; lengthValue < 64; lengthValue++) {
            if (!ExecutionManager.clip(address + position + lengthValue, 1)) return -14;
            int value = deviceValue.readMemory(address + position + lengthValue);
            pathName[lengthValue] = value;
            if (value == 0) return lengthValue == 0 ? -2 : (MemoryFileSystem.checkName(pathName, lengthValue) ? lengthValue : -22);
            if (value == '/') return -20;
        }
        return -36;
    }
    static int openFile(int nameAddress, int settings, int grantPermission) {
        int lengthValue = readPath(nameAddress);
        if (lengthValue < 0) return lengthValue;
        if ((settings & ~(3 | createEntry | createExclusively | clearContents | appendContinuation | doNotWait | closeOnExec)) != 0) return -95;
        if ((settings & 3) == 3 || ((settings & clearContents) != 0 && (settings & 3) == 0)) return -22;
        int file = MemoryFileSystem.findEntry(pathName, lengthValue);
        if (file >= 0 && (settings & (createEntry | createExclusively)) == (createEntry | createExclusively)) return -17;
        if (file == -2 && (settings & createEntry) == 0) return -2;
        int descriptorEntry = emptyDescriptor(0), descriptorValue = emptyHandle();
        if (descriptorEntry < 0 || descriptorValue < 0) return -24;
        if (file == -2) {
            int result = MemoryFileSystem.storeValue(pathName, lengthValue, pathName, 0);
            if (result < 0) return result;
            file = MemoryFileSystem.findEntry(pathName, lengthValue);
            MemoryFileSystem.permissionGrants[file] = grantPermission & 511;
        }
        if (file < 0) return file;
        if ((settings & clearContents) != 0) MemoryFileSystem.sizeList[file] = 0;
        MemoryFileSystem.openCount[file]++;
        return connect(descriptorEntry, descriptorValue, 2, file, settings);
    }
    static int readFile(int descriptorEntry, int dataAddress, int lengthValue) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0 || (openSettings[descriptorValue] & 3) == 1) return -9;
        if (lengthValue < 0) return -22;
        if (lengthValue == 0) return 0;
        if (!ExecutionManager.clip(dataAddress, lengthValue)) return -14;
        if (kindValue[descriptorValue] == 3) return receiveDatagramData(descriptorEntry, dataAddress, lengthValue, 0, 0);
        if (kindValue[descriptorValue] == 1) {
            int receivedCount = 0;
            while (receivedCount < lengthValue) {
                int value = TextTerminal.readSerial();
                if (value < 0) value = Keyboard.read();
                if (value < 0) {
                    if (receivedCount > 0) return receivedCount;
                    if ((openSettings[descriptorValue] & doNotWait) != 0) return -11;
                    if (deviceValue.userRemainingMilliseconds() <= 10) return -11;
                    networkStack.verify(); deviceValue.yieldBriefly();
                } else {
                    deviceValue.writeMemory(dataAddress + receivedCount, value); receivedCount++;
                }
            }
            return receivedCount;
        }
        int file = targetValue[descriptorValue], position = filePosition[descriptorValue];
        if (position >= MemoryFileSystem.sizeList[file]) return 0;
        if (lengthValue > MemoryFileSystem.sizeList[file] - position) lengthValue = MemoryFileSystem.sizeList[file] - position;
        int originalAddress = deviceValue.fileMemory() + file * MemoryFileSystem.maximumSize + position;
        for (int index = 0; index < lengthValue; index++) deviceValue.writeMemory(dataAddress + index, deviceValue.readMemory(originalAddress + index));
        filePosition[descriptorValue] += lengthValue;
        return lengthValue;
    }
    static int writeFile(int descriptorEntry, int dataAddress, int lengthValue) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0 || (openSettings[descriptorValue] & 3) == 0) return -9;
        if (lengthValue < 0) return -22;
        if (lengthValue == 0) return 0;
        if (!ExecutionManager.clip(dataAddress, lengthValue)) return -14;
        if (kindValue[descriptorValue] == 3) return -89; // An unconnected datagram endpoint needs a destination address.
        if (kindValue[descriptorValue] == 1) {
            if (lengthValue > 16384) lengthValue = 16384;
            for (int index = 0; index < lengthValue; index++) {
                int value = deviceValue.readMemory(dataAddress + index);
                TextTerminal.serialByte(value); TextTerminal.screenCharacter(value);
            }
            return lengthValue;
        }
        int file = targetValue[descriptorValue], size = MemoryFileSystem.sizeList[file];
        int position = (openSettings[descriptorValue] & appendContinuation) != 0 ? size : filePosition[descriptorValue];
        if (position >= MemoryFileSystem.maximumSize) return -27;
        if (lengthValue > MemoryFileSystem.maximumSize - position) lengthValue = MemoryFileSystem.maximumSize - position;
        int destinationAddress = deviceValue.fileMemory() + file * MemoryFileSystem.maximumSize;
        for (int index = size; index < position; index++) deviceValue.writeMemory(destinationAddress + index, 0);
        for (int index = 0; index < lengthValue; index++) deviceValue.writeMemory(destinationAddress + position + index, deviceValue.readMemory(dataAddress + index));
        filePosition[descriptorValue] = position + lengthValue;
        if (position + lengthValue > size) MemoryFileSystem.sizeList[file] = position + lengthValue;
        return lengthValue;
    }
    static int seekFile(int descriptorEntry, int offsetValue, int projectRoot) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        if (kindValue[descriptorValue] != 2) return -29;
        if (projectRoot < 0 || projectRoot > 2) return -22;
        int backgroundValue = projectRoot == 0 ? 0 : (projectRoot == 1 ? filePosition[descriptorValue] : MemoryFileSystem.sizeList[targetValue[descriptorValue]]);
        if (offsetValue > 0 && backgroundValue > 2147483647 - offsetValue) return -75;
        if (offsetValue < 0 && offsetValue < -backgroundValue) return -22;
        filePosition[descriptorValue] = backgroundValue + offsetValue;
        return filePosition[descriptorValue];
    }
    static int duplicateDescriptor(int descriptorEntry, int newDescriptor, boolean assignValue, int settings) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        if (newDescriptor < 0 || newDescriptor >= descriptorLimit) return assignValue ? -9 : -22;
        if (assignValue && descriptorEntry == newDescriptor) return newDescriptor;
        if (assignValue) { if (openHandle[newDescriptor] != 0) closeFile(newDescriptor); }
        else { newDescriptor = emptyDescriptor(newDescriptor); if (newDescriptor < 0) return newDescriptor; }
        openHandle[newDescriptor] = descriptorValue + 1; setDescriptor[newDescriptor] = settings; referenceCount[descriptorValue]++;
        return newDescriptor;
    }
    static int removeFileEntryName(int nameAddress) {
        int lengthValue = readPath(nameAddress);
        if (lengthValue < 0) return lengthValue;
        int file = MemoryFileSystem.findEntry(pathName, lengthValue);
        if (file < 0) return file;
        MemoryFileSystem.namesList[file * 64] = 0;
        return 0;
    }
    static int setFileLength(int descriptorEntry, int lengthValue) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        if (kindValue[descriptorValue] != 2 || (openSettings[descriptorValue] & 3) == 0 || lengthValue < 0) return -22;
        if (lengthValue > MemoryFileSystem.maximumSize) return -27;
        int file = targetValue[descriptorValue], address = deviceValue.fileMemory() + file * MemoryFileSystem.maximumSize;
        for (int index = MemoryFileSystem.sizeList[file]; index < lengthValue; index++) deviceValue.writeMemory(address + index, 0);
        MemoryFileSystem.sizeList[file] = lengthValue;
        return 0;
    }
    static int readFileStatus(int descriptorEntry, int address) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        if (!ExecutionManager.clip(address, 48)) return -14;
        for (int index = 0; index < 12; index++) ExecutionManager.writeNumber(address + index * 4, 0);
        int file = targetValue[descriptorValue], size = kindValue[descriptorValue] == 2 ? MemoryFileSystem.sizeList[file] : 0;
        int grantPermission = kindValue[descriptorValue] == 2 ? MemoryFileSystem.permissionGrants[file] : 438;
        ExecutionManager.writeNumber(address, 1);
        ExecutionManager.writeNumber(address + 4, kindValue[descriptorValue] == 2 ? file + 1 : 100 + descriptorValue);
        ExecutionManager.writeNumber(address + 8, (kindValue[descriptorValue] == 2 ? 32768 : (kindValue[descriptorValue] == 1 ? 8192 : 49152)) | grantPermission);
        ExecutionManager.writeNumber(address + 12, kindValue[descriptorValue] == 2 && MemoryFileSystem.namesList[file * 64] == 0 ? 0 : 1);
        ExecutionManager.writeNumber(address + 28, size); ExecutionManager.writeNumber(address + 32, 512);
        ExecutionManager.writeNumber(address + 36, (size + 511) / 512);
        return 0;
    }
    static int controlDescriptor(int descriptorEntry, int command, int value) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        if (command == 0 || command == 1030) return duplicateDescriptor(descriptorEntry, value, false, command == 1030 ? 1 : 0);
        if (command == 1) return setDescriptor[descriptorEntry];
        if (command == 2) { if ((value & ~1) != 0) return -22; setDescriptor[descriptorEntry] = value; return 0; }
        if (command == 3) return openSettings[descriptorValue];
        if (command == 4) {
            if ((value & ~(3 | appendContinuation | doNotWait)) != 0) return -95;
            openSettings[descriptorValue] = (openSettings[descriptorValue] & 3) | (value & (appendContinuation | doNotWait)); return 0;
        }
        return -95;
    }
    static int createEndpoint(int addressScheme, int networkKind, int contractNumber) {
        if (addressScheme != 2) return -97;
        if (networkKind != 2) return -93;
        if (contractNumber != 0 && contractNumber != 17) return -93;
        int descriptorEntry = emptyDescriptor(0), descriptorValue = emptyHandle();
        if (descriptorEntry < 0 || descriptorValue < 0) return -24;
        return connect(descriptorEntry, descriptorValue, 3, 0, readWriteFlag);
    }
    static int endpointDescriptor(int descriptorEntry) {
        int descriptorValue = findDescriptor(descriptorEntry);
        if (descriptorValue < 0) return -9;
        return kindValue[descriptorValue] == 3 ? descriptorValue : -88;
    }
    static int address32(int address) {
        return deviceValue.readMemory(address) << 24 | deviceValue.readMemory(address + 1) << 16
            | deviceValue.readMemory(address + 2) << 8 | deviceValue.readMemory(address + 3);
    }
    static int checkAddress(int address, int lengthValue) {
        if (lengthValue < 16) return -22;
        if (!ExecutionManager.clip(address, 16)) return -14;
        return ExecutionManager.shortValue(address) == 2 ? 0 : -97;
    }
    static int bindAddress(int descriptorEntry, int address, int lengthValue) {
        int descriptorValue = endpointDescriptor(descriptorEntry);
        if (descriptorValue < 0) return descriptorValue;
        int result = checkAddress(address, lengthValue);
        if (result < 0) return result;
        if (networkHandle[descriptorValue] != 0) return -22;
        int networkAddress = address32(address + 4);
        if (networkAddress != 0 && networkAddress != networkStack.ownAddress) return -99;
        int portNumber = deviceValue.readMemory(address + 2) << 8 | deviceValue.readMemory(address + 3);
        result = networkStack.open(portNumber);
        if (result < 0) return result;
        networkHandle[descriptorValue] = result; targetValue[descriptorValue] = networkAddress;
        return 0;
    }
    static int autoBind(int descriptorValue) {
        if (networkHandle[descriptorValue] != 0) return 0;
        int result = networkStack.open(0);
        if (result < 0) return result;
        networkHandle[descriptorValue] = result;
        return 0;
    }
    // The last two sendto/recvfrom arguments are passed in an 8-byte request structure.
    static int sendDatagramData(int descriptorEntry, int dataAddress, int lengthValue, int settings, int requestedAddress) {
        int descriptorValue = endpointDescriptor(descriptorEntry);
        if (descriptorValue < 0) return descriptorValue;
        if (settings != 0) return -95;
        if (lengthValue < 0 || lengthValue > 1024) return -90;
        if (lengthValue != 0 && !ExecutionManager.clip(dataAddress, lengthValue)) return -14;
        if (!ExecutionManager.clip(requestedAddress, 8)) return -14;
        int address = ExecutionManager.number(requestedAddress);
        int result = checkAddress(address, ExecutionManager.number(requestedAddress + 4));
        if (result < 0) return result;
        int portNumber = deviceValue.readMemory(address + 2) << 8 | deviceValue.readMemory(address + 3);
        if (portNumber == 0) return -22;
        result = autoBind(descriptorValue);
        if (result < 0) return result;
        for (int index = 0; index < lengthValue; index++) transferData[index] = deviceValue.readMemory(dataAddress + index);
        return networkStack.send(networkHandle[descriptorValue], address32(address + 4), portNumber, transferData, lengthValue);
    }
    static void writeAddress(int address, int lengthValue, int networkAddress, int portNumber) {
        for (int index = 0; index < lengthValue && index < 16; index++) {
            int value = 0;
            if (index == 0) value = 2;
            if (index == 2) value = portNumber >>> 8;
            if (index == 3) value = portNumber;
            if (index >= 4 && index < 8) value = networkAddress >>> (56 - index * 8);
            deviceValue.writeMemory(address + index, value & 255);
        }
    }
    static int receiveDatagramData(int descriptorEntry, int dataAddress, int lengthValue, int settings, int requestedAddress) {
        int descriptorValue = endpointDescriptor(descriptorEntry);
        if (descriptorValue < 0) return descriptorValue;
        if ((settings & ~64) != 0) return -95;
        if (lengthValue < 0) return -22;
        if (lengthValue != 0 && !ExecutionManager.clip(dataAddress, lengthValue)) return -14;
        int address = 0, addressLengthAddress = 0, addressLength = 0;
        if (requestedAddress != 0) {
            if (!ExecutionManager.clip(requestedAddress, 8)) return -14;
            address = ExecutionManager.number(requestedAddress); addressLengthAddress = ExecutionManager.number(requestedAddress + 4);
            if (address != 0) {
                if (!ExecutionManager.clip(addressLengthAddress, 4)) return -14;
                addressLength = ExecutionManager.number(addressLengthAddress);
                if (addressLength < 0) return -22;
                if (!ExecutionManager.clip(address, addressLength < 16 ? addressLength : 16)) return -14;
            }
        }
        int result = autoBind(descriptorValue);
        if (result < 0) return result;
        int run = deviceValue.milliseconds();
        while (true) {
            result = networkStack.receive(networkHandle[descriptorValue], transferData, 1024, 0);
            if (result != -11) break;
            if ((settings & 64) != 0 || (openSettings[descriptorValue] & doNotWait) != 0) return -11;
            if (receiveTimeoutMilliseconds[descriptorValue] > 0 && deviceValue.milliseconds() - run >= receiveTimeoutMilliseconds[descriptorValue]) return -11;
            if (deviceValue.userRemainingMilliseconds() <= 10) return -11;
            deviceValue.yieldBriefly();
        }
        if (result < 0) return result;
        if (result > lengthValue) result = lengthValue;
        for (int index = 0; index < result; index++) deviceValue.writeMemory(dataAddress + index, transferData[index]);
        if (address != 0) {
            writeAddress(address, addressLength, networkStack.peerAddress(networkHandle[descriptorValue]), networkStack.peerPortNumber(networkHandle[descriptorValue]));
            ExecutionManager.writeNumber(addressLengthAddress, 16);
        }
        return result;
    }
    static int readSocketAddress(int descriptorEntry, int address, int lengthAddress) {
        int descriptorValue = endpointDescriptor(descriptorEntry);
        if (descriptorValue < 0) return descriptorValue;
        if (!ExecutionManager.clip(lengthAddress, 4)) return -14;
        int lengthValue = ExecutionManager.number(lengthAddress);
        if (lengthValue < 0) return -22;
        if (!ExecutionManager.clip(address, lengthValue < 16 ? lengthValue : 16)) return -14;
        int slotEntry = networkStack.index(networkHandle[descriptorValue]);
        writeAddress(address, lengthValue, targetValue[descriptorValue], slotEntry < 0 ? 0 : networkStack.ports[slotEntry]);
        ExecutionManager.writeNumber(lengthAddress, 16);
        return 0;
    }
    static int setReceiveTimeout(int descriptorEntry, int milliseconds) {
        int descriptorValue = endpointDescriptor(descriptorEntry);
        if (descriptorValue < 0) return descriptorValue;
        if (milliseconds < 0 || milliseconds > 2000) return -22;
        receiveTimeoutMilliseconds[descriptorValue] = milliseconds;
        return 0;
    }
}
