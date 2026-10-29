// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Called through the int 0x80 gate. Validate every user pointer and length before access. */
public final class invokeSystemCall {
    static int[] temporaryBuffer = new int[1024];

    static int arrayLength(int address) {
        if (!ExecutionManager.clip(address, 4)) return -14;
        int lengthValue = ExecutionManager.number(address);
        if (lengthValue < 0 || lengthValue > (ExecutionManager.userEnd - address - 4) / 4) return -14;
        return lengthValue;
    }

    public static int processValueEntry(int index, int firstOperand, int secondOperand, int thirdOperand, int fourthOperand, int fifthOperand) {
        if (index == 30) return FileDescriptorManager.openFile(firstOperand, secondOperand, thirdOperand);
        if (index == 31) return FileDescriptorManager.readFile(firstOperand, secondOperand, thirdOperand);
        if (index == 32) return FileDescriptorManager.writeFile(firstOperand, secondOperand, thirdOperand);
        if (index == 33) return FileDescriptorManager.closeFile(firstOperand);
        if (index == 34) return FileDescriptorManager.seekFile(firstOperand, secondOperand, thirdOperand);
        if (index == 35) return FileDescriptorManager.duplicateDescriptor(firstOperand, 0, false, 0);
        if (index == 36) return FileDescriptorManager.duplicateDescriptor(firstOperand, secondOperand, true, 0);
        if (index == 37) return FileDescriptorManager.readFileStatus(firstOperand, secondOperand);
        if (index == 38) return FileDescriptorManager.removeFileEntryName(firstOperand);
        if (index == 39) return FileDescriptorManager.setFileLength(firstOperand, secondOperand);
        if (index == 40) return FileDescriptorManager.controlDescriptor(firstOperand, secondOperand, thirdOperand);
        if (index == 41) return FileDescriptorManager.createEndpoint(firstOperand, secondOperand, thirdOperand);
        if (index == 42) return FileDescriptorManager.bindAddress(firstOperand, secondOperand, thirdOperand);
        if (index == 43) return FileDescriptorManager.sendDatagramData(firstOperand, secondOperand, thirdOperand, fourthOperand, fifthOperand);
        if (index == 44) return FileDescriptorManager.receiveDatagramData(firstOperand, secondOperand, thirdOperand, fourthOperand, fifthOperand);
        if (index == 45) return FileDescriptorManager.readSocketAddress(firstOperand, secondOperand, thirdOperand);
        if (index == 46) return FileDescriptorManager.setReceiveTimeout(firstOperand, secondOperand);
        if (index == 47) {
            int descriptorValue = FileDescriptorManager.findDescriptor(firstOperand);
            if (descriptorValue < 0) return -9;
            if (FileDescriptorManager.kindValue[descriptorValue] != 2) return -22;
            return preserveFile.synchronize();
        }
        if (index == 1) {
            int lengthValue = arrayLength(firstOperand);
            if (lengthValue < 0) return lengthValue;
            if (lengthValue > 4096) return -90;
            for (int characterValue = 0; characterValue < lengthValue; characterValue++) TextTerminal.Characters(ExecutionManager.number(firstOperand + 4 + characterValue * 4) & 65535);
            return lengthValue;
        }
        if (index == 2) return ExecutionManager.argumentCount;
        if (index == 3) return firstOperand >= 0 && firstOperand < ExecutionManager.argumentCount ? ExecutionManager.argumentAddress[firstOperand] : 0;
        if (index == 10) return networkStack.open(firstOperand);
        if (index == 11) {
            int lengthValue = arrayLength(fourthOperand);
            if (lengthValue < 0) return lengthValue;
            if (fifthOperand < 0 || fifthOperand > lengthValue || fifthOperand > 1024) return -90;
            for (int position = 0; position < fifthOperand; position++) temporaryBuffer[position] = ExecutionManager.number(fourthOperand + 4 + position * 4) & 255;
            return networkStack.send(firstOperand, secondOperand, thirdOperand, temporaryBuffer, fifthOperand);
        }
        if (index == 12) {
            int lengthValue = arrayLength(secondOperand);
            if (lengthValue < 0) return lengthValue;
            if (thirdOperand < 0 || thirdOperand > 2000) return -22;
            int result = networkStack.receive(firstOperand, temporaryBuffer, lengthValue < 1024 ? lengthValue : 1024, thirdOperand);
            if (result >= 0) for (int position = 0; position < result; position++) ExecutionManager.writeNumber(secondOperand + 4 + position * 4, temporaryBuffer[position]);
            return result;
        }
        if (index == 13) return networkStack.close(firstOperand);
        if (index == 14) return networkStack.ownAddress;
        if (index == 15) return networkStack.peerAddress(firstOperand);
        if (index == 16) return networkStack.peerPortNumber(firstOperand);
        if (index == 22) {
            if (firstOperand < 0 || firstOperand > 65535) return -22;
            TextTerminal.Characters(firstOperand); return 1;
        }
        if (index == 20 || index == 21) {
            int nameSize = arrayLength(firstOperand), dataSize = arrayLength(secondOperand);
            if (nameSize < 0 || dataSize < 0) return -14;
            if (nameSize < 1 || nameSize > 64) return -22;
            int lengthValue = 0;
            while (lengthValue < nameSize && ExecutionManager.number(firstOperand + 4 + lengthValue * 4) != 0) {
                MemoryFileSystem.name[lengthValue] = ExecutionManager.number(firstOperand + 4 + lengthValue * 4);
                lengthValue++;
            }
            if (!MemoryFileSystem.checkName(MemoryFileSystem.name, lengthValue)) return -22;
            if (index == 20) {
                int file = MemoryFileSystem.findEntry(MemoryFileSystem.name, lengthValue);
                if (file < 0) return file;
                int size = MemoryFileSystem.sizeList[file];
                if (size > dataSize) return -90;
                int address = deviceValue.fileMemory() + file * MemoryFileSystem.maximumSize;
                for (int number = 0; number < size; number++) ExecutionManager.writeNumber(secondOperand + 4 + number * 4, deviceValue.readMemory(address + number));
                return size;
            }
            if (thirdOperand < 0 || thirdOperand > dataSize) return -22;
            if (thirdOperand > MemoryFileSystem.maximumSize) return -90;
            for (int number = 0; number < thirdOperand; number++) MemoryFileSystem.editValue[number] = ExecutionManager.number(secondOperand + 4 + number * 4) & 255;
            return MemoryFileSystem.storeValue(MemoryFileSystem.name, lengthValue, MemoryFileSystem.editValue, thirdOperand);
        }
        return -38;
    }
}
