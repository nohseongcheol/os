// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Boot information lookup and allocation/release of fixed 4 KiB task regions; not a general physical page manager. */
public final class memoryRegion {
    static int[] sectionValue = new int[8192];
    static int[] useValue = new int[8];

    static int parseInteger(int address) {
        return deviceValue.readMemory(address) | (deviceValue.readMemory(address + 1) << 8)
            | (deviceValue.readMemory(address + 2) << 16) | (deviceValue.readMemory(address + 3) << 24);
    }

    static int upperMemorySize() {
        int systemInformation = deviceValue.bootInformation();
        if (deviceValue.bootMarker() != 0x2badb002 || systemInformation == 0 || (parseInteger(systemInformation) & 1) == 0) return -1;
        return parseInteger(systemInformation + 8);
    }

    static int allocateStorage() {
        for (int index = 0; index < useValue.length; index++) {
            if (useValue[index] == 0) {
                useValue[index] = 1;
                for (int slotEntry = 0; slotEntry < 1024; slotEntry++) sectionValue[index * 1024 + slotEntry] = 0;
                return index;
            }
        }
        return -1;
    }

    static boolean returnResult(int index) {
        if (index < 0 || index >= useValue.length || useValue[index] == 0) return false;
        useValue[index] = 0;
        return true;
    }

    static int usedEntryCount() {
        int itemCount = 0;
        for (int index = 0; index < useValue.length; index++) itemCount += useValue[index];
        return itemCount;
    }
}
