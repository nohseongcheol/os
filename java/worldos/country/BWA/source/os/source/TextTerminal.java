// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 serial output and an 80x25 VGA text display. Unicode text is sent to the serial terminal as UTF-8. */
public final class TextTerminal {
    static int slotEntry = 0;
    static int colourValue = 7;

    static void prepare() {
        deviceValue.writeIoByte(0x3f9, 0);
        deviceValue.writeIoByte(0x3fb, 0x80);
        deviceValue.writeIoByte(0x3f8, 1);
        deviceValue.writeIoByte(0x3f9, 0);
        deviceValue.writeIoByte(0x3fb, 3);
        deviceValue.writeIoByte(0x3fa, 0xc7);
        deviceValue.writeIoByte(0x3fc, 0x0b);
        eraseEntry();
    }

    static void serialByte(int value) {
        int repetitionCount = 100000;
        while ((deviceValue.readIoByte(0x3fd) & 0x20) == 0 && repetitionCount > 0) repetitionCount--;
        if (repetitionCount > 0) deviceValue.writeIoByte(0x3f8, value);
    }

    static void eraseEntry() {
        for (int index = 0; index < 2000; index++) {
            deviceValue.writeMemory(0xb8000 + index * 2, 32);
            deviceValue.writeMemory(0xb8001 + index * 2, colourValue);
        }
        slotEntry = 0;
        cursorValue();
    }

    static void cursorValue() {
        deviceValue.writeIoByte(0x3d4, 14);
        deviceValue.writeIoByte(0x3d5, slotEntry >> 8);
        deviceValue.writeIoByte(0x3d4, 15);
        deviceValue.writeIoByte(0x3d5, slotEntry & 255);
    }

    static void screenCharacter(int value) {
        if (value == 13) return;
        if (value == 10) {
            slotEntry = (slotEntry / 80 + 1) * 80;
        } else if (value == 8) {
            if (slotEntry > 0) {
                slotEntry--;
                deviceValue.writeMemory(0xb8000 + slotEntry * 2, 32);
            }
        } else {
            deviceValue.writeMemory(0xb8000 + slotEntry * 2, value < 128 ? value : '?');
            deviceValue.writeMemory(0xb8001 + slotEntry * 2, colourValue);
            slotEntry++;
        }
        if (slotEntry >= 2000) {
            for (int index = 0; index < 3840; index++)
                deviceValue.writeMemory(0xb8000 + index, deviceValue.readMemory(0xb80a0 + index));
            for (int index = 1920; index < 2000; index++) {
                deviceValue.writeMemory(0xb8000 + index * 2, 32);
                deviceValue.writeMemory(0xb8001 + index * 2, colourValue);
            }
            slotEntry = 1920;
        }
        cursorValue();
    }

    static void Characters(int value) {
        if (value < 128) {
            if (value == 10) serialByte(13);
            serialByte(value);
        } else if (value < 2048) {
            serialByte(0xc0 | (value >> 6));
            serialByte(0x80 | (value & 63));
        } else {
            serialByte(0xe0 | (value >> 12));
            serialByte(0x80 | ((value >> 6) & 63));
            serialByte(0x80 | (value & 63));
        }
        screenCharacter(value);
    }

    static void write(String contentValue) {
        for (int index = 0; index < contentValue.length(); index++) Characters(contentValue.charAt(index));
    }

    static void writeNumber(int value) {
        // Never negate to positive, so Integer.MIN_VALUE is safe too.
        if (value < 0) Characters('-');
        else value = -value;
        int positionIndex = 1000000000;
        boolean run = false;
        while (positionIndex > 0) {
            int digitValue = -(value / positionIndex);
            if (digitValue != 0 || run || positionIndex == 1) {
                Characters('0' + digitValue);
                run = true;
            }
            value %= positionIndex;
            positionIndex /= 10;
        }
    }

    static int readSerial() {
        if ((deviceValue.readIoByte(0x3fd) & 1) != 0) return deviceValue.readIoByte(0x3f8);
        return -1;
    }
}
