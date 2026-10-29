// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Polled PC/AT PS/2 translated set 1 input, with the basic US keyboard layout, Shift, Backspace and Enter. */
public final class Keyboard {
    static boolean shiftLeft = false;
    static boolean shiftRight = false;
    static boolean extensionValue = false;
    static String defaultValue = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String shiftValue = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int read() {
        int stateValue = deviceValue.readIoByte(0x64);
        if ((stateValue & 1) == 0) return -1;
        int value = deviceValue.readIoByte(0x60);
        if ((stateValue & 0x20) != 0) return -1;
        if (value == 0xe0 || value == 0xe1) { extensionValue = true; return -1; }
        if (extensionValue) { extensionValue = false; return -1; }
        if (value == 42 || value == 170) { shiftLeft = value == 42; return -1; }
        if (value == 54 || value == 182) { shiftRight = value == 54; return -1; }
        if (value >= defaultValue.length()) return -1;
        int Characters = (shiftLeft || shiftRight) ? shiftValue.charAt(value) : defaultValue.charAt(value);
        return Characters == 0 ? -1 : Characters;
    }
}
