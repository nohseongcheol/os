// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Shared guest-tool output and ASCII filename handling. */
public final class JavaTools {
    /** Converts a UTF-8 byte array into UTF-16 units in the same array. Rejects malformed input. */
    static int decodeSource(int[] data, int lengthValue) {
        int read = 0, write = 0;
        if (lengthValue >= 3 && data[0] == 239 && data[1] == 187 && data[2] == 191) read = 3;
        while (read < lengthValue) {
            int value = data[read++], number = 0, minimumValue = 0;
            if (value >= 194 && value <= 223) { number = 1; minimumValue = 128; value &= 31; }
            else if (value >= 224 && value <= 239) { number = 2; minimumValue = 2048; value &= 15; }
            else if (value >= 240 && value <= 244) { number = 3; minimumValue = 65536; value &= 7; }
            else if (value >= 128 || value < 0) return -1;
            if (number > lengthValue - read) return -1;
            for (int i = 0; i < number; i++) {
                int nextItem = data[read++]; if ((nextItem & 192) != 128) return -1;
                value = (value << 6) | (nextItem & 63);
            }
            if (value < minimumValue || value > 0x10ffff || (value >= 0xd800 && value <= 0xdfff)) return -1;
            if (value >= 65536) { value -= 65536; data[write++] = 0xd800 | (value >> 10); data[write++] = 0xdc00 | (value & 1023); }
            else data[write++] = value;
        }
        return write;
    }
    static void writeNumber(int value) {
        if (value < 0) User.writeCharacterValue('-'); else value = -value;
        int positionIndex = 1000000000;
        boolean run = false;
        while (positionIndex != 0) {
            int number = -(value / positionIndex);
            if (number != 0 || run || positionIndex == 1) { User.writeCharacterValue('0' + number); run = true; }
            value %= positionIndex; positionIndex /= 10;
        }
    }
    static int name(int[] destinationValue, String original) {
        if (original.length() >= destinationValue.length) return -1;
        for (int number = 0; number < destinationValue.length; number++) destinationValue[number] = number < original.length() ? original.charAt(number) : 0;
        return original.length();
    }
    static boolean equalText(String firstOperand, String secondOperand) {
        if (firstOperand.length() != secondOperand.length()) return false;
        for (int number = 0; number < firstOperand.length(); number++) if (firstOperand.charAt(number) != secondOperand.charAt(number)) return false;
        return true;
    }
}
