// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), enkodering_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normaliseer_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int greep_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int lengte_VALUE(String Teks) { return Teks.length(); }
    public static boolean 같음(String voor_VALUE, String TERUG_VALUE) { return voor_VALUE == null ? TERUG_VALUE == null : voor_VALUE.equals(TERUG_VALUE); }
    public static String plak_SMS(String voor_VALUE, String TERUG_VALUE) { return voor_VALUE.concat(TERUG_VALUE); }
    public static String sny_VALUE(String Teks, int Loop, int 끝) { return Teks.substring(Loop, 끝); }
    public static int ontleed_heelgetal(String Teks) { try { return Integer.parseInt(Teks); } catch (NumberFormatException Fout) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String skryf_heelgetal_VALUE(int 수) { return Integer.toString(수); }
    public static int karakterkode_COUNT(String Teks) {
        int 수 = 0;
        for (int lus_INDEX = 0; lus_INDEX < Teks.length(); lus_INDEX++, 수++) {
            int karakterkode = Teks.charAt(lus_INDEX);
            if (karakterkode >= 0xd800 && karakterkode <= 0xdbff && lus_INDEX + 1 < Teks.length() && Teks.charAt(lus_INDEX + 1) >= 0xdc00 && Teks.charAt(lus_INDEX + 1) <= 0xdfff) lus_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Teks) {
        byte[] 임시 = new byte[Teks.length() * 3]; int 쓴수 = 0;
        for (int lus_INDEX = 0; lus_INDEX < Teks.length(); lus_INDEX++) {
            int karakterkode = Teks.charAt(lus_INDEX);
            if (karakterkode >= 0xd800 && karakterkode <= 0xdbff && lus_INDEX + 1 < Teks.length() && Teks.charAt(lus_INDEX + 1) >= 0xdc00 && Teks.charAt(lus_INDEX + 1) <= 0xdfff) karakterkode = 0x10000 + ((karakterkode - 0xd800) << 10) + Teks.charAt(++lus_INDEX) - 0xdc00;
            else if (karakterkode >= 0xd800 && karakterkode <= 0xdfff) karakterkode = '?';
            if (karakterkode < 128) 임시[쓴수++] = (byte)karakterkode;
            else if (karakterkode < 2048) { 임시[쓴수++] = (byte)(192 | karakterkode >> 6); 임시[쓴수++] = (byte)(128 | karakterkode & 63); }
            else if (karakterkode < 65536) { 임시[쓴수++] = (byte)(224 | karakterkode >> 12); 임시[쓴수++] = (byte)(128 | karakterkode >> 6 & 63); 임시[쓴수++] = (byte)(128 | karakterkode & 63); }
            else { 임시[쓴수++] = (byte)(240 | karakterkode >> 18); 임시[쓴수++] = (byte)(128 | karakterkode >> 12 & 63); 임시[쓴수++] = (byte)(128 | karakterkode >> 6 & 63); 임시[쓴수++] = (byte)(128 | karakterkode & 63); }
        }
        byte[] maatreël = new byte[쓴수]; System.arraycopy(임시, 0, maatreël, 0, 쓴수); return maatreël;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dekripteer_data(byte[] greep_VALUE) {
        StringBuilder maatreël = new StringBuilder();
        for (int lus_INDEX = 0; lus_INDEX < greep_VALUE.length;) {
            int karakterkode = greep_VALUE[lus_INDEX++] & 255, 수 = karakterkode < 128 ? 0 : karakterkode >= 194 && karakterkode < 224 ? 1 : karakterkode >= 224 && karakterkode < 240 ? 2 : karakterkode >= 240 && karakterkode <= 244 ? 3 : -1;
            if (수 < 0 || greep_VALUE.length - lus_INDEX < 수) throw new ongeldig_argument_uitsondering("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) karakterkode &= (1 << (6 - 수)) - 1;
            for (int binnebind_plaas = 0; binnebind_plaas < 수; binnebind_plaas++) { int TERUG_VALUE = greep_VALUE[lus_INDEX++] & 255; if ((TERUG_VALUE & 192) != 128) throw new ongeldig_argument_uitsondering("잘못된 UTF-8"); karakterkode = karakterkode << 6 | TERUG_VALUE & 63; }
            if (karakterkode < 최소 || karakterkode > 0x10ffff || karakterkode >= 0xd800 && karakterkode <= 0xdfff) throw new ongeldig_argument_uitsondering("잘못된 UTF-8");
            if (karakterkode < 65536) maatreël.append((char)karakterkode);
            else { karakterkode -= 65536; maatreël.append((char)(0xd800 | karakterkode >> 10)); maatreël.append((char)(0xdc00 | karakterkode & 1023)); }
        }
        return maatreël.toString();
    }
}
