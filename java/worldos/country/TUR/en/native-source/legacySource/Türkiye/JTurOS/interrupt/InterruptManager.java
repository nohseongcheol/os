// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiye.JTurOS.interrupt;

import java.util.Arrays;

/** Registers and dispatches the Java-managed handlers of the IDT. */
public final class InterruptManager {
    private final InterruptHandler[] handlerList = new InterruptHandler[256];
    private boolean active;

    public void registerEntry(int index, InterruptHandler Handler) {
        verifyNumber(index);
        handlerList[index] = Handler;
    }

    public void releaseStorage(int index) {
        verifyNumber(index);
        handlerList[index] = null;
    }

    public int distributeValue(int index, int savedStackAddress) {
        verifyNumber(index);
        if (!active) {
            return savedStackAddress;
        }
        InterruptHandler Handler = handlerList[index];
        return Handler == null ? savedStackAddress : Handler.processValueEntry(savedStackAddress);
    }

    public void enable() {
        active = true;
    }

    public void deactivate() {
        active = false;
    }

    public boolean isActive() {
        return active;
    }

    public void releaseAll() {
        Arrays.fill(handlerList, null);
    }

    private void verifyNumber(int index) {
        if (index < 0 || index >= handlerList.length) {
            throw new IllegalArgumentException("interrupt 번호가 올바르지 않습니다.");
        }
    }
}

