// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Yemen.JYemOS.inputValue;

public final class inputEvent {
    public enum kindValue {
        keyDown,
        keyUp,
        mouseMovement,
        mouseButtonPressed,
        mouseButtonReleased
    }

    private final kindValue eventKind;
    private final int firstValue;
    private final int secondValue;

    public inputEvent(kindValue eventKind, int firstValue, int secondValue) {
        this.eventKind = eventKind;
        this.firstValue = firstValue;
        this.secondValue = secondValue;
    }

    public kindValue eventKind() {
        return eventKind;
    }

    public int firstValue() {
        return firstValue;
    }

    public int secondValue() {
        return secondValue;
    }
}

