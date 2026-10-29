// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Converts between UTF-8 bytes and UTF-16 strings. Normalization and composition input are separate concerns. */
public final class Characters {
    public static int byteCount(byte[] data) { return data.length; }
    private Characters() {}
    public static int lengthValue(String text) { return text.length(); }
    public static boolean equalText(String frontValue, String backValue) { return frontValue == null ? backValue == null : frontValue.equals(backValue); }
    public static String pasteText(String frontValue, String backValue) { return frontValue.concat(backValue); }
    public static String cutValue(String text, int run, int ending) { return text.substring(run, ending); }
    public static int parseInteger(String text) { try { return Integer.parseInt(text); } catch (NumberFormatException error) { throw new NumberFormatFailure("Check the number format and range."); } }
    public static String writeIntegerValue(int number) { return Integer.toString(number); }
    public static int codePointCount(String text) {
        int number = 0;
        for (int loopIndex = 0; loopIndex < text.length(); loopIndex++, number++) {
            int characterCode = text.charAt(loopIndex);
            if (characterCode >= 0xd800 && characterCode <= 0xdbff && loopIndex + 1 < text.length() && text.charAt(loopIndex + 1) >= 0xdc00 && text.charAt(loopIndex + 1) <= 0xdfff) loopIndex++;
        }
        return number;
    }
    public static byte[] encode(String text) {
        byte[] temporaryValue = new byte[text.length() * 3]; int written = 0;
        for (int loopIndex = 0; loopIndex < text.length(); loopIndex++) {
            int characterCode = text.charAt(loopIndex);
            if (characterCode >= 0xd800 && characterCode <= 0xdbff && loopIndex + 1 < text.length() && text.charAt(loopIndex + 1) >= 0xdc00 && text.charAt(loopIndex + 1) <= 0xdfff) characterCode = 0x10000 + ((characterCode - 0xd800) << 10) + text.charAt(++loopIndex) - 0xdc00;
            else if (characterCode >= 0xd800 && characterCode <= 0xdfff) characterCode = '?';
            if (characterCode < 128) temporaryValue[written++] = (byte)characterCode;
            else if (characterCode < 2048) { temporaryValue[written++] = (byte)(192 | characterCode >> 6); temporaryValue[written++] = (byte)(128 | characterCode & 63); }
            else if (characterCode < 65536) { temporaryValue[written++] = (byte)(224 | characterCode >> 12); temporaryValue[written++] = (byte)(128 | characterCode >> 6 & 63); temporaryValue[written++] = (byte)(128 | characterCode & 63); }
            else { temporaryValue[written++] = (byte)(240 | characterCode >> 18); temporaryValue[written++] = (byte)(128 | characterCode >> 12 & 63); temporaryValue[written++] = (byte)(128 | characterCode >> 6 & 63); temporaryValue[written++] = (byte)(128 | characterCode & 63); }
        }
        byte[] result = new byte[written]; System.arraycopy(temporaryValue, 0, result, 0, written); return result;
    }
    /** Rejects malformed UTF-8 with the API's invalid-argument exception. */
    public static String decryptData(byte[] byteValue) {
        StringBuilder result = new StringBuilder();
        for (int loopIndex = 0; loopIndex < byteValue.length;) {
            int characterCode = byteValue[loopIndex++] & 255, number = characterCode < 128 ? 0 : characterCode >= 194 && characterCode < 224 ? 1 : characterCode >= 224 && characterCode < 240 ? 2 : characterCode >= 240 && characterCode <= 244 ? 3 : -1;
            if (number < 0 || byteValue.length - loopIndex < number) throw new InvalidArgumentException("Invalid UTF-8");
            int minimumValue = number == 1 ? 128 : number == 2 ? 2048 : number == 3 ? 65536 : 0;
            if (number > 0) characterCode &= (1 << (6 - number)) - 1;
            for (int innerPosition = 0; innerPosition < number; innerPosition++) { int backValue = byteValue[loopIndex++] & 255; if ((backValue & 192) != 128) throw new InvalidArgumentException("Invalid UTF-8"); characterCode = characterCode << 6 | backValue & 63; }
            if (characterCode < minimumValue || characterCode > 0x10ffff || characterCode >= 0xd800 && characterCode <= 0xdfff) throw new InvalidArgumentException("Invalid UTF-8");
            if (characterCode < 65536) result.append((char)characterCode);
            else { characterCode -= 65536; result.append((char)(0xd800 | characterCode >> 10)); result.append((char)(0xdc00 | characterCode & 1023)); }
        }
        return result.toString();
    }
}
