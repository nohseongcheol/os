// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Validates ELF32 in read-only executable bundles, passes arguments and runs one user process at a time. */
public final class ExecutionManager {
    static final int startUserProgram = 0x04000000;
    static final int userEnd = 0x04400000;
    static final int imageEndAddress = 0x04200000;
    static final int argumentStart = 0x04300000;
    static int argumentCount = 0;
    static int[] argumentAddress = new int[16];

    static boolean clip(int address, int lengthValue) {
        return address >= startUserProgram && address < userEnd && lengthValue >= 0 && lengthValue <= userEnd - address;
    }

    static int number(int address) { return memoryRegion.parseInteger(address); }
    static int shortValue(int address) { return deviceValue.readMemory(address) | deviceValue.readMemory(address + 1) << 8; }
    static void writeNumber(int address, int value) {
        for (int index = 0; index < 4; index++) deviceValue.writeMemory(address + index, value >>> (index * 8));
    }

    static int groupCount() {
        int address = deviceValue.ExecutableBundle();
        int size = deviceValue.executableBundleSize();
        if (size < 8 || number(address) != 0x50414b4a) return 0;
        int itemCount = number(address + 4);
        return itemCount >= 0 && itemCount <= 32 && itemCount <= (size - 8) / 24 ? itemCount : 0;
    }

    static void entryList() {
        for (int index = 0; index < groupCount(); index++) {
            int entryValue = deviceValue.ExecutableBundle() + 8 + index * 24;
            for (int characterValue = 0; characterValue < 16 && deviceValue.readMemory(entryValue + characterValue) != 0; characterValue++)
                TextTerminal.Characters(deviceValue.readMemory(entryValue + characterValue));
            TextTerminal.write("\n");
        }
    }

    static int findEntry(int[] inputValue, int run, int lengthValue) {
        if (lengthValue <= 0 || lengthValue >= 16) return 0;
        for (int index = 0; index < groupCount(); index++) {
            int entryValue = deviceValue.ExecutableBundle() + 8 + index * 24;
            boolean equalText = deviceValue.readMemory(entryValue + lengthValue) == 0;
            for (int characterValue = 0; characterValue < lengthValue; characterValue++)
                if (inputValue[run + characterValue] != deviceValue.readMemory(entryValue + characterValue)) equalText = false;
            if (equalText) return entryValue;
        }
        return 0;
    }

    static int validate(int file, int lengthValue) {
        if (lengthValue < 52 || number(file) != 0x464c457f || deviceValue.readMemory(file + 4) != 1
            || deviceValue.readMemory(file + 5) != 1 || deviceValue.readMemory(file + 6) != 1
            || shortValue(file + 16) != 2 || shortValue(file + 18) != 3 || number(file + 20) != 1
            || shortValue(file + 40) != 52 || shortValue(file + 42) != 32) return -8;
        int entryPointValue = number(file + 24);
        int tablePosition = number(file + 28);
        int itemCount = shortValue(file + 44);
        if (itemCount == 0 || itemCount > 16 || tablePosition < 52 || tablePosition > lengthValue - itemCount * 32) return -8;
        boolean isExecutable = false;
        for (int index = 0; index < itemCount; index++) {
            int lookupTable = file + tablePosition + index * 32;
            int kindValue = number(lookupTable);
            if (kindValue == 2 || kindValue == 3) return -8; // No support for dynamic linking or an interpreter.
            if (kindValue != 1) continue;
            int position = number(lookupTable + 4), address = number(lookupTable + 8), fileSize = number(lookupTable + 16), memorySize = number(lookupTable + 20);
            int alignValue = number(lookupTable + 28);
            if (address < startUserProgram || address >= imageEndAddress || memorySize < 0 || memorySize > imageEndAddress - address
                || fileSize < 0 || fileSize > memorySize || position < 0 || (fileSize > 0 && position > lengthValue - fileSize)
                || (alignValue != 0 && (alignValue < 0 || (alignValue & (alignValue - 1)) != 0
                    || ((address - position) & (alignValue - 1)) != 0))) return -8;
            for (int frontValue = 0; frontValue < index; frontValue++) {
                int previousItem = file + tablePosition + frontValue * 32;
                if (number(previousItem) == 1 && memorySize > 0 && number(previousItem + 20) > 0
                    && address < number(previousItem + 8) + number(previousItem + 20) && number(previousItem + 8) < address + memorySize) return -8;
            }
            if ((number(lookupTable + 24) & 1) != 0 && entryPointValue >= address && entryPointValue - address < fileSize) isExecutable = true;
        }
        return isExecutable ? entryPointValue : -8;
    }

    static int executeCommand(int[] inputValue, int run, int lengthValue) {
        while (run < lengthValue && inputValue[run] == ' ') run++;
        int ending = run;
        while (ending < lengthValue && inputValue[ending] != ' ') ending++;
        int entryValue = findEntry(inputValue, run, ending - run);
        if (entryValue == 0) return -2;
        int position = number(entryValue + 16), size = number(entryValue + 20);
        if (position < 8 + groupCount() * 24 || size < 52 || position > deviceValue.executableBundleSize() - size) return -8;
        int file = deviceValue.ExecutableBundle() + position;
        int entryPointValue = validate(file, size);
        if (entryPointValue < 0) return entryPointValue;
        deviceValue.userClearContents();
        int tablePosition = number(file + 28), itemCount = shortValue(file + 44);
        for (int index = 0; index < itemCount; index++) {
            int lookupTable = file + tablePosition + index * 32;
            if (number(lookupTable) != 1) continue;
            int original = file + number(lookupTable + 4), destinationValue = number(lookupTable + 8), fileSize = number(lookupTable + 16);
            for (int byteValue = 0; byteValue < fileSize; byteValue++) deviceValue.writeMemory(destinationValue + byteValue, deviceValue.readMemory(original + byteValue));
        }
        argumentCount = 0;
        int storeValue = argumentStart;
        while (ending < lengthValue) {
            while (ending < lengthValue && inputValue[ending] == ' ') ending++;
            if (ending == lengthValue) break;
            if (argumentCount == argumentAddress.length) return -22;
            run = ending;
            while (ending < lengthValue && inputValue[ending] != ' ') ending++;
            argumentAddress[argumentCount++] = storeValue;
            writeNumber(storeValue, ending - run);
            for (int characterValue = run; characterValue < ending; characterValue++) writeNumber(storeValue + 4 + (characterValue - run) * 4, inputValue[characterValue]);
            storeValue += 4 + (ending - run) * 4;
        }
        networkStack.cleanProcess();
        FileDescriptorManager.startProcess();
        int result = deviceValue.runUserProgram(entryPointValue, userEnd - 16);
        FileDescriptorManager.cleanProcess();
        networkStack.cleanProcess();
        return result;
    }
}
