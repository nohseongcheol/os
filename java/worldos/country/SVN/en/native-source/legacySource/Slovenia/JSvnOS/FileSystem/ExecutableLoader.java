// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenia.JSvnOS.FileSystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Validates headers and load segments of little-endian ELF32 executables. */
public final class ExecutableLoader {
    public static final class sectionValue {
        private final int kindValue;
        private final int flagValue;
        private final int address;
        private final int filePosition;
        private final int size;

        sectionValue(int kindValue, int flagValue, int address, int filePosition, int size) {
            this.kindValue = kindValue;
            this.flagValue = flagValue;
            this.address = address;
            this.filePosition = filePosition;
            this.size = size;
        }

        public int kindValue() {
            return kindValue;
        }

        public int flagValue() {
            return flagValue;
        }

        public int address() {
            return address;
        }

        public int filePosition() {
            return filePosition;
        }

        public int size() {
            return size;
        }
    }

    public static final class image {
        private final int startAddress;
        private final List<sectionValue> sectionsList;

        image(int startAddress, List<sectionValue> sectionsList) {
            this.startAddress = startAddress;
            this.sectionsList = Collections.unmodifiableList(sectionsList);
        }

        public int startAddress() {
            return startAddress;
        }

        public List<sectionValue> sectionsList() {
            return sectionsList;
        }
    }

    public image Checks(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int startAddress = parseInteger(data, 24);
        int sectionTablePosition = parseInteger(data, 32);
        int sectionEntrySize = readShortInteger(data, 46);
        int sectionCount = readShortInteger(data, 48);
        if (sectionEntrySize < 40 || sectionTablePosition < 0
                || (long) sectionTablePosition + (long) sectionEntrySize * sectionCount > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<sectionValue> sectionsList = new ArrayList<sectionValue>();
        for (int index = 0; index < sectionCount; index++) {
            int position = sectionTablePosition + index * sectionEntrySize;
            int kindValue = parseInteger(data, position + 4);
            int flagValue = parseInteger(data, position + 8);
            int address = parseInteger(data, position + 12);
            int filePosition = parseInteger(data, position + 16);
            int size = parseInteger(data, position + 20);
            if (size < 0 || (kindValue != 8 && ((long) filePosition + size > data.length || filePosition < 0))) {
                throw new IllegalArgumentException("ELF sectionValue data 범위가 올바르지 않습니다.");
            }
            sectionsList.add(new sectionValue(kindValue, flagValue, address, filePosition, size));
        }
        return new image(startAddress, sectionsList);
    }

    private int parseInteger(byte[] data, int position) {
        if (position < 0 || position > data.length - 4) {
            throw new IllegalArgumentException("ELF Integer 범위를 벗어났습니다.");
        }
        return (data[position] & 0xff)
                | ((data[position + 1] & 0xff) << 8)
                | ((data[position + 2] & 0xff) << 16)
                | ((data[position + 3] & 0xff) << 24);
    }

    private int readShortInteger(byte[] data, int position) {
        if (position < 0 || position > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 Integer 범위를 벗어났습니다.");
        }
        return (data[position] & 0xff) | ((data[position + 1] & 0xff) << 8);
    }
}
