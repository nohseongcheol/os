// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Spain.JEspOS.FileSystem;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Reads the four primary partitions of a DOS MBR. */
public final class primaryPartitionTable {
    public static final class partitionValue {
        private final int kindValue;
        private final long startSection;
        private final long sectionCount;

        partitionValue(int kindValue, long startSection, long sectionCount) {
            this.kindValue = kindValue;
            this.startSection = startSection;
            this.sectionCount = sectionCount;
        }

        public int kindValue() { return kindValue; }
        public long startSection() { return startSection; }
        public long sectionCount() { return sectionCount; }
    }

    public List<partitionValue> read(byte[] firstSection) {
        if (firstSection == null || firstSection.length < 512
                || (firstSection[510] & 0xff) != 0x55 || (firstSection[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<partitionValue> result = new ArrayList<partitionValue>();
        for (int index = 0; index < 4; index++) {
            int position = 446 + index * 16;
            int kindValue = firstSection[position + 4] & 0xff;
            long run = littleEndianInteger(firstSection, position + 8);
            long size = littleEndianInteger(firstSection, position + 12);
            if (kindValue != 0 && size != 0) {
                result.add(new partitionValue(kindValue, run, size));
            }
        }
        return Collections.unmodifiableList(result);
    }

    private long littleEndianInteger(byte[] data, int position) {
        return (data[position] & 0xffL)
                | ((data[position + 1] & 0xffL) << 8)
                | ((data[position + 2] & 0xffL) << 16)
                | ((data[position + 3] & 0xffL) << 24);
    }
}

