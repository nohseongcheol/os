// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cocos_Keeling_Islands.JCckOS.Host;

import java.util.HashMap;
import java.util.Map;
import Cocos_Keeling_Islands.JCckOS.Kernel.hardwareValue;

/** Hardware substitute for deterministic tests of the managed kernel on an ordinary JVM. */
public final class HostHardware implements hardwareValue {
    private final Map<Integer, Integer> hardwarePortValue = new HashMap<Integer, Integer>();
    private final StringBuilder serialLog = new StringBuilder();

    @Override
    public void serialOutput(String contentValue) {
        serialLog.append(contentValue);
        System.out.print(contentValue);
    }

    @Override
    public int readPortByte(int hardwarePortNumber) {
        Integer value = hardwarePortValue.get(Integer.valueOf(hardwarePortNumber));
        return value == null ? 0 : value.intValue();
    }

    @Override
    public void writePortByte(int hardwarePortNumber, int value) {
        hardwarePortValue.put(Integer.valueOf(hardwarePortNumber), Integer.valueOf(value & 0xff));
    }

    @Override
    public void haltCpu() {
        // Return immediately during host tests instead of waiting for the next event.
    }

    public String serialLog() {
        return serialLog.toString();
    }
}

