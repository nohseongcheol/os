// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Small dedicated storage format using checksums and two copies. Persists changes only on fsync/sync. */
public final class preserveFile {
    static int currentPreservedCopy = -1, generationNumber = 0;
    static int[] fileTable = new int[1024];
    static int hashBytes(int value, int data) { return (value ^ data) * 16777619; }
    static void clearData() {
        for (int index = 0; index < 512; index++) StorageDeviceConnection.sectionData[index] = 0;
    }
    static int tableInteger(int position) {
        return fileTable[position] | fileTable[position + 1] << 8 | fileTable[position + 2] << 16 | fileTable[position + 3] << 24;
    }
    static void writeTableInteger(int position, int value) {
        for (int index = 0; index < 4; index++) fileTable[position + index] = (value >>> (index * 8)) & 255;
    }
    static boolean checkTable() {
        for (int file = 0; file < 8; file++) {
            int lengthValue = 0;
            for (int slotEntry = 0; slotEntry < 64; slotEntry++) MemoryFileSystem.name[slotEntry] = fileTable[file * 72 + slotEntry];
            while (lengthValue < 64 && MemoryFileSystem.name[lengthValue] != 0) lengthValue++;
            if (lengthValue == 0) continue;
            if (!MemoryFileSystem.checkName(MemoryFileSystem.name, lengthValue)
                || tableInteger(file * 72 + 64) < 0 || tableInteger(file * 72 + 64) > 16384) return false;
            for (int frontValue = 0; frontValue < file; frontValue++) {
                boolean equalText = fileTable[frontValue * 72 + lengthValue] == 0;
                for (int slotEntry = 0; slotEntry < lengthValue; slotEntry++) if (fileTable[frontValue * 72 + slotEntry] != MemoryFileSystem.name[slotEntry]) equalText = false;
                if (equalText) return false;
            }
        }
        return true;
    }
    static int checkPreservedCopy(int preservedCopy) {
        int startSection = 1 + preservedCopy * 259;
        if (StorageDeviceConnection.read(startSection) < 0 || StorageDeviceConnection.parseInteger(0) != 0x4a4b534e) return -1;
        int generationValue = StorageDeviceConnection.parseInteger(4), checksum = StorageDeviceConnection.parseInteger(8);
        if (generationValue < 1 || StorageDeviceConnection.parseInteger(12) != (generationValue ^ checksum ^ 0x4a4b534e)) return -1;
        int hashFile = 0x811c9dc5;
        for (int sectionValue = 0; sectionValue < 258; sectionValue++) {
            if (StorageDeviceConnection.read(startSection + 1 + sectionValue) < 0) return -1;
            for (int slotEntry = 0; slotEntry < 512; slotEntry++) {
                int value = StorageDeviceConnection.sectionData[slotEntry];
                hashFile = hashBytes(hashFile, value);
                if (sectionValue < 2) fileTable[sectionValue * 512 + slotEntry] = value;
            }
        }
        return hashFile == checksum && checkTable() ? generationValue : -1;
    }
    static int load(int preservedCopy) {
        int startSection = 1 + preservedCopy * 259;
        for (int sectionValue = 0; sectionValue < 2; sectionValue++) {
            if (StorageDeviceConnection.read(startSection + 1 + sectionValue) < 0) return -5;
            for (int slotEntry = 0; slotEntry < 512; slotEntry++) fileTable[sectionValue * 512 + slotEntry] = StorageDeviceConnection.sectionData[slotEntry];
        }
        for (int file = 0; file < 8; file++) {
            for (int slotEntry = 0; slotEntry < 64; slotEntry++) MemoryFileSystem.namesList[file * 64 + slotEntry] = fileTable[file * 72 + slotEntry];
            MemoryFileSystem.sizeList[file] = fileTable[file * 72] == 0 ? 0 : tableInteger(file * 72 + 64);
            MemoryFileSystem.permissionGrants[file] = tableInteger(file * 72 + 68) & 511;
            for (int sectionValue = 0; sectionValue < 32; sectionValue++) {
                if (StorageDeviceConnection.read(startSection + 3 + file * 32 + sectionValue) < 0) return -5;
                int address = deviceValue.fileMemory() + file * 16384 + sectionValue * 512;
                for (int slotEntry = 0; slotEntry < 512; slotEntry++) deviceValue.writeMemory(address + slotEntry, StorageDeviceConnection.sectionData[slotEntry]);
            }
        }
        return 0;
    }
    static void prepare() {
        if (StorageDeviceConnection.read(0) < 0 || StorageDeviceConnection.parseInteger(0) != 0x54534b4a
            || StorageDeviceConnection.parseInteger(4) != 0x3145524f || StorageDeviceConnection.parseInteger(8) != 2048
            || StorageDeviceConnection.parseInteger(12) != 0x3153464a) {
            TextTerminal.write("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        StorageDeviceConnection.isAvailable = true;
        int firstOrdinal = checkPreservedCopy(0), secondOrdinal = checkPreservedCopy(1);
        if (firstOrdinal < 0 && secondOrdinal < 0) { TextTerminal.write("STORE ready; no valid snapshot\n"); return; }
        currentPreservedCopy = firstOrdinal >= secondOrdinal ? 0 : 1; generationNumber = firstOrdinal >= secondOrdinal ? firstOrdinal : secondOrdinal;
        if (load(currentPreservedCopy) < 0) {
            TextTerminal.write("STORE read failed; halted to preserve files\n"); deviceValue.haltExecution();
        }
        TextTerminal.write("STORE restored generation "); TextTerminal.writeNumber(generationNumber); TextTerminal.Characters(10);
    }
    static int synchronize() {
        if (!StorageDeviceConnection.isAvailable) return -19;
        if (generationNumber == 2147483647) return -75;
        int nextItem = currentPreservedCopy == 0 ? 1 : 0, startSection = 1 + nextItem * 259;
        // Invalidate the previous commit and flush the device cache before writing the new body.
        clearData();
        if (StorageDeviceConnection.write(startSection) < 0 || StorageDeviceConnection.flushOutput() < 0) return -5;
        for (int slotEntry = 0; slotEntry < 1024; slotEntry++) fileTable[slotEntry] = 0;
        for (int file = 0; file < 8; file++) if (MemoryFileSystem.namesList[file * 64] != 0) {
            for (int slotEntry = 0; slotEntry < 64; slotEntry++) fileTable[file * 72 + slotEntry] = MemoryFileSystem.namesList[file * 64 + slotEntry];
            writeTableInteger(file * 72 + 64, MemoryFileSystem.sizeList[file]);
            writeTableInteger(file * 72 + 68, MemoryFileSystem.permissionGrants[file]);
        }
        int hashFile = 0x811c9dc5;
        for (int sectionValue = 0; sectionValue < 258; sectionValue++) {
            for (int slotEntry = 0; slotEntry < 512; slotEntry++) {
                int value = 0;
                if (sectionValue < 2) value = fileTable[sectionValue * 512 + slotEntry];
                else {
                    int file = (sectionValue - 2) / 32, position = (sectionValue - 2) % 32 * 512 + slotEntry;
                    if (fileTable[file * 72] != 0 && position < MemoryFileSystem.sizeList[file])
                        value = deviceValue.readMemory(deviceValue.fileMemory() + file * 16384 + position);
                }
                StorageDeviceConnection.sectionData[slotEntry] = value; hashFile = hashBytes(hashFile, value);
            }
            if (StorageDeviceConnection.write(startSection + 1 + sectionValue) < 0) return -5;
        }
        if (StorageDeviceConnection.flushOutput() < 0) return -5;
        clearData(); StorageDeviceConnection.writeIntegerValue(0, 0x4a4b534e);
        StorageDeviceConnection.writeIntegerValue(4, generationNumber + 1); StorageDeviceConnection.writeIntegerValue(8, hashFile);
        StorageDeviceConnection.writeIntegerValue(12, (generationNumber + 1) ^ hashFile ^ 0x4a4b534e);
        if (StorageDeviceConnection.write(startSection) < 0 || StorageDeviceConnection.flushOutput() < 0) return -5;
        currentPreservedCopy = nextItem; generationNumber++;
        return 0;
    }
}
