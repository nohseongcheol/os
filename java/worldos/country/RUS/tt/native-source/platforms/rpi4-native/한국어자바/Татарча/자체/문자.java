// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
/** 문자(文字), кодлау_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. нормальләштерү_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int байт_COUNT(byte[] мәгълүмат) { return мәгълүмат.length; }
    private 문자() {}
    public static int озынлык_VALUE(String Mäten) { return Mäten.length(); }
    public static boolean 같음(String 앞, String Артка_VALUE) { return 앞 == null ? Артка_VALUE == null : 앞.equals(Артка_VALUE); }
    public static String өстәү_СМС(String 앞, String Артка_VALUE) { return 앞.concat(Артка_VALUE); }
    public static String кисү_VALUE(String Mäten, int эшләтү, int 끝) { return Mäten.substring(эшләтү, 끝); }
    public static int бүлү_бөтен_сан(String Mäten) { try { return Integer.parseInt(Mäten); } catch (NumberFormatException Хата) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String язу_бөтен_сан_VALUE(int 수) { return Integer.toString(수); }
    public static int символ_коды_COUNT(String Mäten) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Mäten.length(); Loop_INDEX++, 수++) {
            int символ_коды = Mäten.charAt(Loop_INDEX);
            if (символ_коды >= 0xd800 && символ_коды <= 0xdbff && Loop_INDEX + 1 < Mäten.length() && Mäten.charAt(Loop_INDEX + 1) >= 0xdc00 && Mäten.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Mäten) {
        byte[] 임시 = new byte[Mäten.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Mäten.length(); Loop_INDEX++) {
            int символ_коды = Mäten.charAt(Loop_INDEX);
            if (символ_коды >= 0xd800 && символ_коды <= 0xdbff && Loop_INDEX + 1 < Mäten.length() && Mäten.charAt(Loop_INDEX + 1) >= 0xdc00 && Mäten.charAt(Loop_INDEX + 1) <= 0xdfff) символ_коды = 0x10000 + ((символ_коды - 0xd800) << 10) + Mäten.charAt(++Loop_INDEX) - 0xdc00;
            else if (символ_коды >= 0xd800 && символ_коды <= 0xdfff) символ_коды = '?';
            if (символ_коды < 128) 임시[쓴수++] = (byte)символ_коды;
            else if (символ_коды < 2048) { 임시[쓴수++] = (byte)(192 | символ_коды >> 6); 임시[쓴수++] = (byte)(128 | символ_коды & 63); }
            else if (символ_коды < 65536) { 임시[쓴수++] = (byte)(224 | символ_коды >> 12); 임시[쓴수++] = (byte)(128 | символ_коды >> 6 & 63); 임시[쓴수++] = (byte)(128 | символ_коды & 63); }
            else { 임시[쓴수++] = (byte)(240 | символ_коды >> 18); 임시[쓴수++] = (byte)(128 | символ_коды >> 12 & 63); 임시[쓴수++] = (byte)(128 | символ_коды >> 6 & 63); 임시[쓴수++] = (byte)(128 | символ_коды & 63); }
        }
        byte[] үлчәм = new byte[쓴수]; System.arraycopy(임시, 0, үлчәм, 0, 쓴수); return үлчәм;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String шифрны_ачу_мәгълүмат(byte[] байт_VALUE) {
        StringBuilder үлчәм = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < байт_VALUE.length;) {
            int символ_коды = байт_VALUE[Loop_INDEX++] & 255, 수 = символ_коды < 128 ? 0 : символ_коды >= 194 && символ_коды < 224 ? 1 : символ_коды >= 224 && символ_коды < 240 ? 2 : символ_коды >= 240 && символ_коды <= 244 ? 3 : -1;
            if (수 < 0 || байт_VALUE.length - Loop_INDEX < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) символ_коды &= (1 << (6 - 수)) - 1;
            for (int Эчке_берләштерү_урнаштыру = 0; Эчке_берләштерү_урнаштыру < 수; Эчке_берләштерү_урнаштыру++) { int Артка_VALUE = байт_VALUE[Loop_INDEX++] & 255; if ((Артка_VALUE & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); символ_коды = символ_коды << 6 | Артка_VALUE & 63; }
            if (символ_коды < 최소 || символ_коды > 0x10ffff || символ_коды >= 0xd800 && символ_коды <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (символ_коды < 65536) үлчәм.append((char)символ_коды);
            else { символ_коды -= 65536; үлчәм.append((char)(0xd800 | символ_коды >> 10)); үлчәм.append((char)(0xdc00 | символ_коды & 1023)); }
        }
        return үлчәм.toString();
    }
}
