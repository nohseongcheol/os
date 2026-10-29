// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package China.JChnOS.inputValue;

import java.util.ArrayDeque;
import java.util.Queue;

/** Transfers input events safely between interrupts and managed code. */
public final class InputManager {
    private final Queue<inputEvent> eventsList = new ArrayDeque<inputEvent>();
    private final int maximumEventCount;
    private int droppedEventCount;

    public InputManager(int maximumEventCount) {
        if (maximumEventCount <= 0) {
            throw new IllegalArgumentException("event 수가 올바르지 않습니다.");
        }
        this.maximumEventCount = maximumEventCount;
    }

    public synchronized void keyDown(int keyData) {
        putValue(new inputEvent(inputEvent.kindValue.keyDown, keyData & 0xff, 0));
    }

    public synchronized void keyUp(int keyData) {
        putValue(new inputEvent(inputEvent.kindValue.keyUp, keyData & 0xff, 0));
    }

    public synchronized void mouseMovement(int horizontalPosition, int verticalPosition) {
        putValue(new inputEvent(inputEvent.kindValue.mouseMovement, horizontalPosition, verticalPosition));
    }

    public synchronized inputEvent nextEvent() {
        return eventsList.poll();
    }

    public synchronized int droppedEventCount() {
        return droppedEventCount;
    }

    private void putValue(inputEvent event) {
        if (eventsList.size() == maximumEventCount) {
            eventsList.poll();
            droppedEventCount++;
        }
        eventsList.offer(event);
    }
}

