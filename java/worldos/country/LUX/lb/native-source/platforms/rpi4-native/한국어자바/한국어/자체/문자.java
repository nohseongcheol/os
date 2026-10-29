// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), Codéierung_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normaliséieren_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int Byte_COUNT(byte[] Daten) { return Daten.length; }
    private 문자() {}
    public static int Längt_VALUE(String SMS) { return SMS.length(); }
    public static boolean 같음(String 앞, String Zeréck_VALUE) { return 앞 == null ? Zeréck_VALUE == null : 앞.equals(Zeréck_VALUE); }
    public static String apechen_SMS(String 앞, String Zeréck_VALUE) { return 앞.concat(Zeréck_VALUE); }
    public static String schneiden_VALUE(String SMS, int Laf, int 끝) { return SMS.substring(Laf, 끝); }
    public static int analyséieren_Ganzzuel(String SMS) { try { return Integer.parseInt(SMS); } catch (NumberFormatException Feeler) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String schreiwen_Ganzzuel_VALUE(int 수) { return Integer.toString(수); }
    public static int Zeechecode_COUNT(String SMS) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++, 수++) {
            int Zeechecode = SMS.charAt(Loop_INDEX);
            if (Zeechecode >= 0xd800 && Zeechecode <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String SMS) {
        byte[] 임시 = new byte[SMS.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < SMS.length(); Loop_INDEX++) {
            int Zeechecode = SMS.charAt(Loop_INDEX);
            if (Zeechecode >= 0xd800 && Zeechecode <= 0xdbff && Loop_INDEX + 1 < SMS.length() && SMS.charAt(Loop_INDEX + 1) >= 0xdc00 && SMS.charAt(Loop_INDEX + 1) <= 0xdfff) Zeechecode = 0x10000 + ((Zeechecode - 0xd800) << 10) + SMS.charAt(++Loop_INDEX) - 0xdc00;
            else if (Zeechecode >= 0xd800 && Zeechecode <= 0xdfff) Zeechecode = '?';
            if (Zeechecode < 128) 임시[쓴수++] = (byte)Zeechecode;
            else if (Zeechecode < 2048) { 임시[쓴수++] = (byte)(192 | Zeechecode >> 6); 임시[쓴수++] = (byte)(128 | Zeechecode & 63); }
            else if (Zeechecode < 65536) { 임시[쓴수++] = (byte)(224 | Zeechecode >> 12); 임시[쓴수++] = (byte)(128 | Zeechecode >> 6 & 63); 임시[쓴수++] = (byte)(128 | Zeechecode & 63); }
            else { 임시[쓴수++] = (byte)(240 | Zeechecode >> 18); 임시[쓴수++] = (byte)(128 | Zeechecode >> 12 & 63); 임시[쓴수++] = (byte)(128 | Zeechecode >> 6 & 63); 임시[쓴수++] = (byte)(128 | Zeechecode & 63); }
        }
        byte[] Mooss = new byte[쓴수]; System.arraycopy(임시, 0, Mooss, 0, 쓴수); return Mooss;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String decryptéieren_Daten(byte[] Byte_VALUE) {
        StringBuilder Mooss = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < Byte_VALUE.length;) {
            int Zeechecode = Byte_VALUE[Loop_INDEX++] & 255, 수 = Zeechecode < 128 ? 0 : Zeechecode >= 194 && Zeechecode < 224 ? 1 : Zeechecode >= 224 && Zeechecode < 240 ? 2 : Zeechecode >= 240 && Zeechecode <= 244 ? 3 : -1;
            if (수 < 0 || Byte_VALUE.length - Loop_INDEX < 수) throw new 잘못된인수예외("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) Zeechecode &= (1 << (6 - 수)) - 1;
            for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 수; intern_Verknëppung_positionéieren++) { int Zeréck_VALUE = Byte_VALUE[Loop_INDEX++] & 255; if ((Zeréck_VALUE & 192) != 128) throw new 잘못된인수예외("잘못된 UTF-8"); Zeechecode = Zeechecode << 6 | Zeréck_VALUE & 63; }
            if (Zeechecode < 최소 || Zeechecode > 0x10ffff || Zeechecode >= 0xd800 && Zeechecode <= 0xdfff) throw new 잘못된인수예외("잘못된 UTF-8");
            if (Zeechecode < 65536) Mooss.append((char)Zeechecode);
            else { Zeechecode -= 65536; Mooss.append((char)(0xd800 | Zeechecode >> 10)); Mooss.append((char)(0xdc00 | Zeechecode & 1023)); }
        }
        return Mooss.toString();
    }
}
