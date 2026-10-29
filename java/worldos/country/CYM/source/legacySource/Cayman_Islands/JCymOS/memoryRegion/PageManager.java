// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cayman_Islands.JCymOS.memoryRegion;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** Provides 4 KiB page mapping and copy-on-write. */
public final class PageManager {
    public static final int pageSize = 4096;

    private static final class pageValue {
        private byte[] data = new byte[pageSize];
        private int referenceCount = 1;
        private boolean canWrite = true;
        private boolean copyOnWrite;
    }

    public static final class AddressSpace {
        private final Map<Integer, pageValue> pageTable = new HashMap<Integer, pageValue>();
    }

    public AddressSpace newAddressSpace() {
        return new AddressSpace();
    }

    public void mapPage(AddressSpace addressRegion, int virtualAddress, boolean canWrite) {
        int index = pageNumber(virtualAddress);
        pageValue newPage = new pageValue();
        newPage.canWrite = canWrite;
        addressRegion.pageTable.put(Integer.valueOf(index), newPage);
    }

    public AddressSpace cloneCopyOnWrite(AddressSpace original) {
        AddressSpace clonedValue = new AddressSpace();
        for (Map.Entry<Integer, pageValue> entryValue : original.pageTable.entrySet()) {
            pageValue sharedPage = entryValue.getValue();
            sharedPage.referenceCount++;
            if (sharedPage.canWrite) {
                sharedPage.canWrite = false;
                sharedPage.copyOnWrite = true;
            }
            clonedValue.pageTable.put(entryValue.getKey(), sharedPage);
        }
        return clonedValue;
    }

    public byte readByteValue(AddressSpace addressRegion, int virtualAddress) {
        pageValue targetValue = findPage(addressRegion, virtualAddress);
        return targetValue.data[Math.floorMod(virtualAddress, pageSize)];
    }

    public void writeByteValue(AddressSpace addressRegion, int virtualAddress, byte value) {
        int index = pageNumber(virtualAddress);
        pageValue targetValue = findPage(addressRegion, virtualAddress);
        if (!targetValue.canWrite) {
            if (!targetValue.copyOnWrite) {
                throw new IllegalStateException("read 전용 쪽입니다.");
            }
            targetValue = createPrivatePage(addressRegion, index, targetValue);
        }
        targetValue.data[Math.floorMod(virtualAddress, pageSize)] = value;
    }

    public void privateRangeWrite(AddressSpace addressRegion, int startAddress, int size) {
        if (size < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int endAddress = Math.addExact(startAddress, size);
        for (int address = startAddress; address < endAddress; address = (pageNumber(address) + 1) * pageSize) {
            int index = pageNumber(address);
            pageValue targetValue = findPage(addressRegion, address);
            if (targetValue.copyOnWrite) {
                createPrivatePage(addressRegion, index, targetValue);
            } else {
                targetValue.canWrite = true;
            }
        }
    }

    public void rangeWrite(AddressSpace addressRegion, int startAddress, byte[] data) {
        for (int index = 0; index < data.length; index++) {
            writeByteValue(addressRegion, startAddress + index, data[index]);
        }
    }

    private pageValue createPrivatePage(AddressSpace addressRegion, int index, pageValue sharedPage) {
        pageValue privatePage = new pageValue();
        privatePage.data = Arrays.copyOf(sharedPage.data, sharedPage.data.length);
        privatePage.canWrite = true;
        privatePage.copyOnWrite = false;
        sharedPage.referenceCount--;
        addressRegion.pageTable.put(Integer.valueOf(index), privatePage);
        return privatePage;
    }

    private pageValue findPage(AddressSpace addressRegion, int address) {
        pageValue targetValue = addressRegion.pageTable.get(Integer.valueOf(pageNumber(address)));
        if (targetValue == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return targetValue;
    }

    private int pageNumber(int address) {
        if (address < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return address / pageSize;
    }
}

