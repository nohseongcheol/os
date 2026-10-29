// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 512-byte logical sectors on the first IDE device. This layer neither formats nor erases arbitrary devices. */
public final class StorageDeviceConnection {
    static boolean isAvailable = false;
    static int[] sectionData = new int[512];
    static void waitBriefly() {
        for (int index = 0; index < 4; index++) deviceValue.readIoByte(0x3f6);
    }
    static int waitUntilReady(boolean dataRequired) {
        int run = deviceValue.milliseconds();
        while (deviceValue.milliseconds() - run < 500) {
            int stateValue = deviceValue.readIoByte(0x1f7);
            if (stateValue == 0 || stateValue == 255) return -19;
            if ((stateValue & 128) == 0) {
                if ((stateValue & 33) != 0) return -5;
                if (!dataRequired || (stateValue & 8) != 0) return 0;
            }
            deviceValue.yieldBriefly();
        }
        return -110;
    }
    static int request(int sectionValue, int command) {
        if (sectionValue < 0 || sectionValue >= 2048) return -22;
        deviceValue.writeIoByte(0x3f6, 2); // Polling; IDE IRQ is not used.
        deviceValue.writeIoByte(0x1f6, 0xe0); waitBriefly();
        int result = waitUntilReady(false);
        if (result < 0) return result;
        deviceValue.writeIoByte(0x1f2, 1);
        deviceValue.writeIoByte(0x1f3, sectionValue & 255);
        deviceValue.writeIoByte(0x1f4, (sectionValue >>> 8) & 255);
        deviceValue.writeIoByte(0x1f5, 0);
        deviceValue.writeIoByte(0x1f7, command); waitBriefly();
        return waitUntilReady(true);
    }
    static int read(int sectionValue) {
        int result = request(sectionValue, 0x20);
        if (result < 0) return result;
        for (int index = 0; index < 256; index++) {
            int value = deviceValue.readIoShort(0x1f0);
            sectionData[index * 2] = value & 255; sectionData[index * 2 + 1] = value >>> 8;
        }
        waitBriefly(); return waitUntilReady(false);
    }
    static int write(int sectionValue) {
        if (!isAvailable || sectionValue < 1 || sectionValue > 518) return -19;
        int result = request(sectionValue, 0x30);
        if (result < 0) return result;
        for (int index = 0; index < 256; index++)
            deviceValue.writeIoShort(0x1f0, sectionData[index * 2] | sectionData[index * 2 + 1] << 8);
        waitBriefly(); return waitUntilReady(false);
    }
    static int flushOutput() {
        if (!isAvailable) return -19;
        deviceValue.writeIoByte(0x1f7, 0xe7); waitBriefly();
        return waitUntilReady(false);
    }
    static int parseInteger(int position) {
        return sectionData[position] | sectionData[position + 1] << 8 | sectionData[position + 2] << 16 | sectionData[position + 3] << 24;
    }
    static void writeIntegerValue(int position, int value) {
        for (int index = 0; index < 4; index++) sectionData[position + index] = (value >>> (index * 8)) & 255;
    }
}
