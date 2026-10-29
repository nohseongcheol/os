// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hong_Kong_SAR_China.JHkgOS.memoryRegion;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** Handles aligned allocation, release and coalescing of physical memory. */
public final class MemoryManager {
    private final byte[] memoryRegion;
    private final TreeMap<Integer, Integer> emptyRegion = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> usedRegion = new TreeMap<Integer, Integer>();

    public MemoryManager(int totalSize) {
        if (totalSize < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        memoryRegion = new byte[totalSize];
        emptyRegion.put(Integer.valueOf(4096), Integer.valueOf(totalSize - 4096));
    }

    public synchronized int allocateStorage(int size) {
        return allocateAligned(size, 1);
    }

    public synchronized int allocateAligned(int size, int alignValue) {
        if (size <= 0 || alignValue <= 0 || (alignValue & (alignValue - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> entryValue : emptyRegion.entrySet()) {
            int run = entryValue.getKey().intValue();
            int regionSize = entryValue.getValue().intValue();
            int alignedStart = (run + alignValue - 1) & -alignValue;
            int frontValueSize = alignedStart - run;
            int finalSize = regionSize - frontValueSize - size;
            if (finalSize < 0) {
                continue;
            }
            emptyRegion.remove(Integer.valueOf(run));
            if (frontValueSize > 0) {
                emptyRegion.put(Integer.valueOf(run), Integer.valueOf(frontValueSize));
            }
            if (finalSize > 0) {
                emptyRegion.put(Integer.valueOf(alignedStart + size), Integer.valueOf(finalSize));
            }
            usedRegion.put(Integer.valueOf(alignedStart), Integer.valueOf(size));
            Arrays.fill(memoryRegion, alignedStart, alignedStart + size, (byte) 0);
            return alignedStart;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void releaseStorage(int address) {
        Integer sizeObject = usedRegion.remove(Integer.valueOf(address));
        if (sizeObject == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int run = address;
        int size = sizeObject.intValue();
        Map.Entry<Integer, Integer> frontValue = emptyRegion.lowerEntry(Integer.valueOf(run));
        if (frontValue != null && frontValue.getKey().intValue() + frontValue.getValue().intValue() == run) {
            run = frontValue.getKey().intValue();
            size += frontValue.getValue().intValue();
            emptyRegion.remove(frontValue.getKey());
        }
        Map.Entry<Integer, Integer> backValue = emptyRegion.ceilingEntry(Integer.valueOf(run));
        if (backValue != null && run + size == backValue.getKey().intValue()) {
            size += backValue.getValue().intValue();
            emptyRegion.remove(backValue.getKey());
        }
        emptyRegion.put(Integer.valueOf(run), Integer.valueOf(size));
    }

    public synchronized byte readByteValue(int address) {
        checkRange(address, 1);
        return memoryRegion[address];
    }

    public synchronized void writeByteValue(int address, byte value) {
        checkRange(address, 1);
        memoryRegion[address] = value;
    }

    public synchronized int totalSize() {
        return memoryRegion.length;
    }

    public synchronized int usedSize() {
        int totalValue = 0;
        for (Integer size : usedRegion.values()) {
            totalValue += size.intValue();
        }
        return totalValue;
    }

    private void checkRange(int address, int size) {
        if (address < 0 || size < 0 || address > memoryRegion.length - size) {
            throw new IndexOutOfBoundsException("memoryRegion 범위를 벗어났습니다.");
        }
    }
}

