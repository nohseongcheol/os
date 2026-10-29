// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 64 RAM files, 16384 bytes per file, 16 descriptors. All data and policy live in Java. Calls do not yield, so they are atomic between cooperative tasks on the current single core. This is neither disk storage nor a full POSIX implementation. Negative results are error numbers. */
public final class MemoryFiles {
    static final int fileCount = 64;
    static int[] name = new int[fileCount * 64];
    static int[] namelen = new int[fileCount];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] contentValue = new int[fileCount * 4096];
    static int[] lengthValue = new int[fileCount];
    static int[] referenceCount = new int[fileCount];
    static int[] useValue = new int[16];
    static int[] targetValue = new int[16];
    static int[] position = new int[16];
    static int[] methodMode = new int[16];
    static int[] path = new int[64];
    static int pathLength;

    public static int fileLimit() { return fileCount; }
    static int readData(int file, int positionIndex) { return (contentValue[file * 4096 + positionIndex / 4] >>> ((positionIndex & 3) * 8)) & 255; }
    static void writeData(int file, int positionIndex, int value) {
        int slotEntry = file * 4096 + positionIndex / 4, moveValue = (positionIndex & 3) * 8;
        contentValue[slotEntry] = (contentValue[slotEntry] & ~(255 << moveValue)) | ((value & 255) << moveValue);
    }

    public static int pathStart(int size) {
        pathLength = 0;
        if (size < 1 || size > 63) return -36;
        pathLength = size;
        for (int loopIndex = 0; loopIndex < size; loopIndex++) path[loopIndex] = 0;
        return 0;
    }
    public static int pathByte(int index, int value) {
        if (index < 0 || index >= pathLength || value < 1 || value > 255) return -22;
        path[index] = value; return 0;
    }
    static int findEntry() {
        for (int fileIndex = 0; fileIndex < fileCount; fileIndex++) if (namelen[fileIndex] > 0 && namelen[fileIndex] == canonicalLength && prefixValue(name, fileIndex * 64, namelen[fileIndex], canonicalValue, canonicalLength)) return fileIndex;
        return -1;
    }
    public static int open(int flagsValue) {
        if (pathLength == 0 || (flagsValue & ~0x6c3) != 0 || (flagsValue & 3) == 3) return -22;
        for (int loopIndex = 0; loopIndex < pathLength; loopIndex++) if (path[loopIndex] == 0) return -22;
        if ((flagsValue & 0x200) != 0 && (flagsValue & 3) == 0) return -22;
        int result = normalizeValue(); if (result < 0) return result;
        if (findDirectory(canonicalLength) >= 0) return -21;
        result = checkParent(); if (result < 0) return result;
        int file = findEntry();
        if (file >= 0 && (flagsValue & 0xc0) == 0xc0) return -17;
        if (file < 0 && (flagsValue & 0x40) == 0) return -2;
        int descriptorEntry = -1;
        for (int loopIndex = 0; loopIndex < 16; loopIndex++) if (useValue[loopIndex] == 0) { descriptorEntry = loopIndex; break; }
        if (descriptorEntry < 0) return -24;
        if (file < 0) {
            for (int loopIndex = 0; loopIndex < fileCount; loopIndex++) if (namelen[loopIndex] == 0 && referenceCount[loopIndex] == 0) { file = loopIndex; break; }
            if (file < 0) return -28;
            namelen[file] = canonicalLength;
            for (int loopIndex = 0; loopIndex < canonicalLength; loopIndex++) name[file * 64 + loopIndex] = canonicalValue[loopIndex];
            lengthValue[file] = 0;
        }
        if ((flagsValue & 0x200) != 0) lengthValue[file] = 0;
        useValue[descriptorEntry] = 1; targetValue[descriptorEntry] = file; position[descriptorEntry] = 0; methodMode[descriptorEntry] = flagsValue;
        referenceCount[file]++;
        return descriptorEntry + 3;
    }
    static int verify(int descriptorEntry) {
        return descriptorEntry >= 3 && descriptorEntry < 19 && useValue[descriptorEntry - 3] != 0 ? descriptorEntry - 3 : -1;
    }
    public static int read(int descriptorEntry) {
        int slotEntry = verify(descriptorEntry);
        if (slotEntry < 0 || (methodMode[slotEntry] & 3) == 1) return -9;
        int file = targetValue[slotEntry];
        if (position[slotEntry] >= lengthValue[file]) return 256; // Distinguish EOF from actual bytes 0x00..0xff.
        return readData(file, position[slotEntry]++);
    }
    public static int write(int descriptorEntry, int value) {
        int slotEntry = verify(descriptorEntry);
        if (slotEntry < 0 || (methodMode[slotEntry] & 3) == 0) return -9;
        int file = targetValue[slotEntry];
        if ((methodMode[slotEntry] & 0x400) != 0) position[slotEntry] = lengthValue[file];
        if (position[slotEntry] >= 16384) return -28;
        while (lengthValue[file] < position[slotEntry]) writeData(file, lengthValue[file]++, 0);
        writeData(file, position[slotEntry]++, value);
        if (lengthValue[file] < position[slotEntry]) lengthValue[file] = position[slotEntry];
        return 1;
    }
    public static int seekPosition(int descriptorEntry, int distanceValue, int projectRoot) {
        int slotEntry = verify(descriptorEntry);
        if (slotEntry < 0) return -9;
        if (projectRoot < 0 || projectRoot > 2 || distanceValue < -16384 || distanceValue > 16384) return -22;
        int newPosition = distanceValue + (projectRoot == 0 ? 0 : projectRoot == 1 ? position[slotEntry] : lengthValue[targetValue[slotEntry]]);
        if (newPosition < 0 || newPosition > 16384) return -22;
        position[slotEntry] = newPosition; return newPosition;
    }
    public static int close(int descriptorEntry) {
        int slotEntry = verify(descriptorEntry);
        if (slotEntry < 0) return -9;
        referenceCount[targetValue[slotEntry]]--; useValue[slotEntry] = 0; return 0;
    }
    public static int size(int descriptorEntry) {
        int slotEntry = verify(descriptorEntry); return slotEntry < 0 ? -9 : lengthValue[targetValue[slotEntry]];
    }
    public static int setLength(int descriptorEntry, int size) {
        int slotEntry = verify(descriptorEntry);
        if (slotEntry < 0 || (methodMode[slotEntry] & 3) == 0) return -9;
        if (size < 0 || size > 16384) return -22;
        int file = targetValue[slotEntry];
        while (lengthValue[file] < size) writeData(file, lengthValue[file]++, 0);
        lengthValue[file] = size; return 0;
    }
    public static int eraseEntry() {
        if (pathLength == 0) return -22;
        int result = normalizeValue(); if (result < 0) return result;
        if (findDirectory(canonicalLength) >= 0) return -21;
        result = checkParent(); if (result < 0) return result;
        int file = findEntry();
        if (file < 0) return -2;
        namelen[file] = 0; return 0; // Keep an open file until its last close.
    }
    static void entryList() {
        pathStart(1); pathByte(0, '.'); pathEntries();
    }
    public static int exportedNameLength(int index) {
        if (index < 0 || index >= fileCount || namelen[index] == 0) return 0;
        for (int loopIndex = 0; loopIndex < namelen[index]; loopIndex++) if (name[index * 64 + loopIndex] == '/') return 0;
        return namelen[index];
    }
    public static int exportedNameByte(int index, int positionIndex) {
        return index >= 0 && index < fileCount && positionIndex >= 0 && positionIndex < namelen[index] ? name[index * 64 + positionIndex] : -22;
    }
    public static int exportedFileSize(int index) { return index >= 0 && index < fileCount ? lengthValue[index] : -22; }
    static int[] canonicalValue = new int[64], currentItem = new int[64], directoryName = new int[16 * 64], directoryLength = new int[16];
    static int canonicalLength, currentLength;
    static boolean prefixValue(int[] namesList, int run, int pathValue, int[] frontValue, int leadingPath) {
        if (pathValue < leadingPath) return false;
        for (int loopIndex = 0; loopIndex < leadingPath; loopIndex++) if (namesList[run + loopIndex] != frontValue[loopIndex]) return false;
        return true;
    }
    static int normalizeValue() {
        if (pathLength == 0) return -22;
        canonicalLength = path[0] == '/' ? 0 : currentLength;
        for (int loopIndex = 0; loopIndex < canonicalLength; loopIndex++) canonicalValue[loopIndex] = currentItem[loopIndex];
        int readCursor = 0;
        while (readCursor < pathLength) {
            while (readCursor < pathLength && path[readCursor] == '/') readCursor++;
            int startPosition = readCursor; while (readCursor < pathLength && path[readCursor] != '/') { if (path[readCursor] == 0) return -22; readCursor++; }
            int entryCount = readCursor - startPosition; if (entryCount == 0 || entryCount == 1 && path[startPosition] == '.') continue;
            if (entryCount == 2 && path[startPosition] == '.' && path[startPosition + 1] == '.') {
                while (canonicalLength > 0 && canonicalValue[canonicalLength - 1] != '/') canonicalLength--;
                if (canonicalLength > 0) canonicalLength--;
                continue;
            }
            if (canonicalLength + entryCount + (canonicalLength == 0 ? 0 : 1) > 63) return -36;
            if (canonicalLength > 0) canonicalValue[canonicalLength++] = '/';
            for (int loopIndex = startPosition; loopIndex < readCursor; loopIndex++) canonicalValue[canonicalLength++] = path[loopIndex];
        }
        return 0;
    }
    static int findDirectory(int entryCount) {
        if (entryCount == 0) return 0;
        for (int loopIndex = 1; loopIndex < 16; loopIndex++) if (directoryLength[loopIndex] == entryCount && prefixValue(directoryName, loopIndex * 64, entryCount, canonicalValue, entryCount)) return loopIndex;
        return -1;
    }
    static int checkParent() {
        int entryCount = canonicalLength; while (entryCount > 0 && canonicalValue[entryCount - 1] != '/') entryCount--;
        return findDirectory(entryCount == 0 ? 0 : entryCount - 1) < 0 ? -2 : 0;
    }
    public static int createDirectory() {
        int processedValue = normalizeValue(); if (processedValue < 0) return processedValue;
        if (findDirectory(canonicalLength) >= 0 || findEntry() >= 0) return -17;
        processedValue = checkParent(); if (processedValue < 0) return processedValue;
        for (int loopIndex = 1; loopIndex < 16; loopIndex++) if (directoryLength[loopIndex] == 0) {
            directoryLength[loopIndex] = canonicalLength; for (int innerPosition = 0; innerPosition < canonicalLength; innerPosition++) directoryName[loopIndex * 64 + innerPosition] = canonicalValue[innerPosition]; return 0;
        }
        return -28;
    }
    public static int entryKind() {
        int processedValue = normalizeValue(); if (processedValue < 0) return processedValue;
        if (findDirectory(canonicalLength) >= 0) return 2;
        return findEntry() >= 0 ? 1 : 0;
    }
    public static int changeDirectory() {
        int processedValue = normalizeValue(); if (processedValue < 0) return processedValue;
        if (findDirectory(canonicalLength) < 0) return -2;
        currentLength = canonicalLength; for (int loopIndex = 0; loopIndex < currentLength; loopIndex++) currentItem[loopIndex] = canonicalValue[loopIndex]; return 0;
    }
    public static int removeDirectory() {
        int processedValue = normalizeValue(); if (processedValue < 0) return processedValue;
        int directoryNumber = findDirectory(canonicalLength); if (directoryNumber < 0) return -2; if (directoryNumber == 0) return -16;
        if (currentLength == canonicalLength && prefixValue(currentItem, 0, currentLength, canonicalValue, canonicalLength)) return -16;
        for (int loopIndex = 0; loopIndex < fileCount; loopIndex++) {
            if (namelen[loopIndex] > canonicalLength && prefixValue(name, loopIndex * 64, namelen[loopIndex], canonicalValue, canonicalLength) && name[loopIndex * 64 + canonicalLength] == '/') return -39;
        }
        for (int loopIndex = 0; loopIndex < 16; loopIndex++) {
            if (directoryLength[loopIndex] > canonicalLength && prefixValue(directoryName, loopIndex * 64, directoryLength[loopIndex], canonicalValue, canonicalLength) && directoryName[loopIndex * 64 + canonicalLength] == '/') return -39;
        }
        directoryLength[directoryNumber] = 0; return 0;
    }
    public static int renameEntry(int originalNumber) {
        if (originalNumber < 0 || originalNumber >= fileCount || namelen[originalNumber] == 0) return -2;
        int processedValue = normalizeValue(); if (processedValue < 0) return processedValue;
        if (findDirectory(canonicalLength) >= 0) return -21;
        processedValue = checkParent(); if (processedValue < 0) return processedValue;
        int previousValue = findEntry(); if (previousValue == originalNumber) return 0;
        if (previousValue >= 0) namelen[previousValue] = 0;
        namelen[originalNumber] = canonicalLength; for (int loopIndex = 0; loopIndex < canonicalLength; loopIndex++) name[originalNumber * 64 + loopIndex] = canonicalValue[loopIndex]; return 0;
    }
    static int entryStart(int[] dataArray, int startingPoint, int entryCount) {
        if (!prefixValue(dataArray, startingPoint, entryCount, canonicalValue, canonicalLength)) return -1;
        int startPosition = canonicalLength;
        if (startPosition > 0) { if (entryCount <= startPosition || dataArray[startingPoint + startPosition] != '/') return -1; startPosition++; }
        if (entryCount <= startPosition) return -1;
        for (int loopIndex = startPosition; loopIndex < entryCount; loopIndex++) if (dataArray[startingPoint + loopIndex] == '/') return -1;
        return startPosition;
    }
    static void currentWrite() { TerminalIO.Characters('/'); for (int loopIndex = 0; loopIndex < currentLength; loopIndex++) Board.writeSerial(currentItem[loopIndex]); }
    static int pathEntries() {
        int processedValue = normalizeValue(); if (processedValue < 0) return processedValue;
        int fileTargetValue = findEntry();
        if (fileTargetValue >= 0) { for (int loopIndex = 0; loopIndex < canonicalLength; loopIndex++) Board.writeSerial(canonicalValue[loopIndex]); TerminalIO.write("  "); TerminalIO.number(lengthValue[fileTargetValue]); TerminalIO.write("byteValue(주기억 file)\n"); return 0; }
        if (findDirectory(canonicalLength) < 0) return -2;
        for (int trailingValue = 1; trailingValue < 16; trailingValue++) if (directoryLength[trailingValue] > 0) {
            int startPosition = entryStart(directoryName, trailingValue * 64, directoryLength[trailingValue]); if (startPosition < 0) continue;
            for (int loopIndex = startPosition; loopIndex < directoryLength[trailingValue]; loopIndex++) Board.writeSerial(directoryName[trailingValue * 64 + loopIndex]); TerminalIO.write("/\n");
        }
        for (int fileIndex = 0; fileIndex < fileCount; fileIndex++) if (namelen[fileIndex] > 0) {
            int startPosition = entryStart(name, fileIndex * 64, namelen[fileIndex]); if (startPosition < 0) continue;
            for (int loopIndex = startPosition; loopIndex < namelen[fileIndex]; loopIndex++) Board.writeSerial(name[fileIndex * 64 + loopIndex]);
            TerminalIO.write("  "); TerminalIO.number(lengthValue[fileIndex]); TerminalIO.write("byteValue(주기억 file)\n");
        }
        return 0;
    }
}
