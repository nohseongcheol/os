// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lithuania.JLtuOS.FileSystem;

import java.util.HashMap;
import java.util.Map;

/** Maintains independent per-process descriptors and shareable open-file descriptions. */
public final class fileDescriptorTable {
    private static final int maximumDescriptor = 32;

    private static final class descriptorEntry {
        private final FileSystem.openedFile openedFile;
        private boolean closeOnExec;

        descriptorEntry(FileSystem.openedFile openedFile) {
            this.openedFile = openedFile;
        }
    }

    private final FileSystem FileSystem;
    private final Map<Integer, descriptorEntry> descriptorEntries = new HashMap<Integer, descriptorEntry>();

    public fileDescriptorTable(FileSystem FileSystem) {
        this.FileSystem = FileSystem;
    }

    public int open(String name) {
        FileSystem.openedFile openedFile = FileSystem.open(name);
        if (openedFile == null) {
            return -2;
        }
        int index = emptyIndex(3);
        if (index < 0) {
            return -24;
        }
        descriptorEntries.put(Integer.valueOf(index), new descriptorEntry(openedFile));
        return index;
    }

    public int read(int index, byte[] receiveDestination, int size) {
        descriptorEntry entryValue = descriptorEntries.get(Integer.valueOf(index));
        if (entryValue == null) {
            return -9;
        }
        if (size < 0 || size > receiveDestination.length) {
            return -22;
        }
        int remainderData = entryValue.openedFile.data.length - entryValue.openedFile.position;
        int readSize = Math.min(size, Math.max(remainderData, 0));
        System.arraycopy(entryValue.openedFile.data, entryValue.openedFile.position, receiveDestination, 0, readSize);
        entryValue.openedFile.position += readSize;
        return readSize;
    }

    public int movePosition(int index, int distanceValue, int projectRoot) {
        descriptorEntry entryValue = descriptorEntries.get(Integer.valueOf(index));
        if (entryValue == null) {
            return -9;
        }
        int backgroundValue;
        if (projectRoot == 0) {
            backgroundValue = 0;
        } else if (projectRoot == 1) {
            backgroundValue = entryValue.openedFile.position;
        } else if (projectRoot == 2) {
            backgroundValue = entryValue.openedFile.data.length;
        } else {
            return -22;
        }
        int newPosition = backgroundValue + distanceValue;
        if (newPosition < 0) {
            return -22;
        }
        entryValue.openedFile.position = newPosition;
        return newPosition;
    }

    public int close(int index) {
        descriptorEntry entryValue = descriptorEntries.remove(Integer.valueOf(index));
        if (entryValue == null) {
            return -9;
        }
        entryValue.openedFile.referenceCount--;
        return 0;
    }

    public int clonedDescriptor(int index, int minimumNumber) {
        descriptorEntry entryValue = descriptorEntries.get(Integer.valueOf(index));
        if (entryValue == null) {
            return -9;
        }
        int newNumber = emptyIndex(minimumNumber);
        if (newNumber < 0) {
            return -24;
        }
        entryValue.openedFile.referenceCount++;
        descriptorEntries.put(Integer.valueOf(newNumber), new descriptorEntry(entryValue.openedFile));
        return newNumber;
    }

    public int duplicateAt(int index, int newNumber) {
        if (index == newNumber) {
            return descriptorEntries.containsKey(Integer.valueOf(index)) ? index : -9;
        }
        if (newNumber < 0 || newNumber >= maximumDescriptor) {
            return -9;
        }
        descriptorEntry original = descriptorEntries.get(Integer.valueOf(index));
        if (original == null) {
            return -9;
        }
        if (descriptorEntries.containsKey(Integer.valueOf(newNumber))) {
            close(newNumber);
        }
        original.openedFile.referenceCount++;
        descriptorEntries.put(Integer.valueOf(newNumber), new descriptorEntry(original.openedFile));
        return newNumber;
    }

    public int setCloseOnExec(int index, boolean value) {
        descriptorEntry entryValue = descriptorEntries.get(Integer.valueOf(index));
        if (entryValue == null) {
            return -9;
        }
        entryValue.closeOnExec = value;
        return 0;
    }

    public int closeOnExecValue(int index) {
        descriptorEntry entryValue = descriptorEntries.get(Integer.valueOf(index));
        if (entryValue == null) {
            return -9;
        }
        return entryValue.closeOnExec ? 1 : 0;
    }

    public fileInformation systemInformation(int index) {
        if (index >= 0 && index <= 2) {
            return new fileInformation(0, 0020666);
        }
        descriptorEntry entryValue = descriptorEntries.get(Integer.valueOf(index));
        if (entryValue == null) {
            return null;
        }
        return new fileInformation(entryValue.openedFile.data.length, 0100444);
    }

    public void closeOnExec() {
        Integer[] numberList = descriptorEntries.keySet().toArray(new Integer[0]);
        for (Integer index : numberList) {
            descriptorEntry entryValue = descriptorEntries.get(index);
            if (entryValue != null && entryValue.closeOnExec) {
                close(index.intValue());
            }
        }
    }

    public boolean isOpen(int index) {
        return descriptorEntries.containsKey(Integer.valueOf(index));
    }

    public fileDescriptorTable cloneValue() {
        fileDescriptorTable result = new fileDescriptorTable(FileSystem);
        for (Map.Entry<Integer, descriptorEntry> entryValue : descriptorEntries.entrySet()) {
            entryValue.getValue().openedFile.referenceCount++;
            descriptorEntry newDescriptor = new descriptorEntry(entryValue.getValue().openedFile);
            newDescriptor.closeOnExec = entryValue.getValue().closeOnExec;
            result.descriptorEntries.put(entryValue.getKey(), newDescriptor);
        }
        return result;
    }

    private int emptyIndex(int minimumNumber) {
        for (int index = Math.max(0, minimumNumber); index < maximumDescriptor; index++) {
            if (!descriptorEntries.containsKey(Integer.valueOf(index))) {
                return index;
            }
        }
        return -1;
    }
}
