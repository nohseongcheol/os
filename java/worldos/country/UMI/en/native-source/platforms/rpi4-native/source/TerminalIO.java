// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class TerminalIO {
    static void Characters(int value) {
        if (value < 0x80) Board.writeSerial(value);
        else if (value < 0x800) {
            Board.writeSerial(0xc0 | (value >> 6)); Board.writeSerial(0x80 | (value & 63));
        } else if (value < 0x10000) {
            Board.writeSerial(0xe0 | (value >> 12)); Board.writeSerial(0x80 | ((value >> 6) & 63)); Board.writeSerial(0x80 | (value & 63));
        } else {
            Board.writeSerial(0xf0 | (value >> 18)); Board.writeSerial(0x80 | ((value >> 12) & 63));
            Board.writeSerial(0x80 | ((value >> 6) & 63)); Board.writeSerial(0x80 | (value & 63));
        }
    }
    static void write(String text) {
        for (int index = 0; index < text.length(); index++) {
            int value = text.charAt(index);
            if (value >= 0xd800 && value <= 0xdbff && index + 1 < text.length()) {
                int bottomValue = text.charAt(index + 1);
                if (bottomValue >= 0xdc00 && bottomValue <= 0xdfff) {
                    value = 0x10000 + ((value - 0xd800) << 10) + bottomValue - 0xdc00; index++;
                }
            }
            if (value >= 0xd800 && value <= 0xdfff) value = 0xfffd;
            Characters(value);
        }
    }
    static void number(int value) {
        if (value < 0) Characters('-'); else value = -value;
        int positionIndex = 1000000000;
        boolean run = false;
        while (positionIndex > 0) {
            int digitValue = -(value / positionIndex);
            if (digitValue != 0 || run || positionIndex == 1) { Characters('0' + digitValue); run = true; }
            value %= positionIndex; positionIndex /= 10;
        }
    }
}
