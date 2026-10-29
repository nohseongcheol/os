// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Austria.JAutOS.storageDevice;

import java.util.Arrays;

/** 512-byte logical-sector device matching the ATA 28-bit command layer. */
public final class AdvancedTechnologyAttachment {
    public static final int sectionSize = 512;
    private final byte[] data;
    private final boolean readOnlyValue;

    public AdvancedTechnologyAttachment(int sectionCount, boolean readOnlyValue) {
        if (sectionCount <= 0) {
            throw new IllegalArgumentException("sectionValue 수가 올바르지 않습니다.");
        }
        data = new byte[Math.multiplyExact(sectionCount, sectionSize)];
        this.readOnlyValue = readOnlyValue;
    }

    public int sectionCount() {
        return data.length / sectionSize;
    }

    public void read(int sectionIndex, byte[] receiveDestination) {
        checkRange(sectionIndex, receiveDestination);
        System.arraycopy(data, sectionIndex * sectionSize, receiveDestination, 0, sectionSize);
    }

    public void write(int sectionIndex, byte[] dataToWrite) {
        if (readOnlyValue) {
            throw new IllegalStateException("read 전용 장치입니다.");
        }
        checkRange(sectionIndex, dataToWrite);
        System.arraycopy(dataToWrite, 0, data, sectionIndex * sectionSize, sectionSize);
    }

    public void eraseEntry() {
        if (readOnlyValue) {
            throw new IllegalStateException("read 전용 장치입니다.");
        }
        Arrays.fill(data, (byte) 0);
    }

    private void checkRange(int sectionIndex, byte[] temporarySpace) {
        if (sectionIndex < 0 || sectionIndex >= sectionCount() || temporarySpace.length < sectionSize) {
            throw new IllegalArgumentException("ATA sectionValue 범위가 올바르지 않습니다.");
        }
    }
}

