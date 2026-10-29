// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Poland.JPolOS.deviceValue;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Manages PCI device discovery results and BAR/IRQ values. */
public final class PeripheralBusManager {
    public static final class deviceValue {
        private final int vendorIdentifier;
        private final int deviceIdentifier;
        private final int ioBase;
        private final int interruptNumber;

        public deviceValue(int vendorIdentifier, int deviceIdentifier, int ioBase, int interruptNumber) {
            this.vendorIdentifier = vendorIdentifier;
            this.deviceIdentifier = deviceIdentifier;
            this.ioBase = ioBase;
            this.interruptNumber = interruptNumber;
        }

        public int vendorIdentifier() { return vendorIdentifier; }
        public int deviceIdentifier() { return deviceIdentifier; }
        public int ioBase() { return ioBase; }
        public int interruptNumber() { return interruptNumber; }
    }

    private final List<deviceValue> devicesList = new ArrayList<deviceValue>();

    public void discoveredValue(deviceValue deviceValue) {
        devicesList.add(deviceValue);
    }

    public List<deviceValue> devicesList() {
        return Collections.unmodifiableList(devicesList);
    }

    public deviceValue findEntry(int vendorIdentifier, int deviceIdentifier) {
        for (deviceValue candidate : devicesList) {
            if (candidate.vendorIdentifier == vendorIdentifier && candidate.deviceIdentifier == deviceIdentifier) {
                return candidate;
            }
        }
        return null;
    }
}

