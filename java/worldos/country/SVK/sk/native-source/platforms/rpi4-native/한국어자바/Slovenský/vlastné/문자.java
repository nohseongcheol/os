// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;
/** 문자(文字), kódovanie_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizovať_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int Byte_COUNT(byte[] údaje) { return údaje.length; }
    private 문자() {}
    public static int dĺžka_VALUE(String Spracovanie_textu) { return Spracovanie_textu.length(); }
    public static boolean 같음(String predný_VALUE, String BACK_VALUE) { return predný_VALUE == null ? BACK_VALUE == null : predný_VALUE.equals(BACK_VALUE); }
    public static String prilepiť_SMS(String predný_VALUE, String BACK_VALUE) { return predný_VALUE.concat(BACK_VALUE); }
    public static String strihať_VALUE(String Spracovanie_textu, int Spustiť_2, int 끝) { return Spracovanie_textu.substring(Spustiť_2, 끝); }
    public static int analyzovať_celé_číslo(String Spracovanie_textu) { try { return Integer.parseInt(Spracovanie_textu); } catch (NumberFormatException chyba) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String zapísať_celé_číslo_VALUE(int 수) { return Integer.toString(수); }
    public static int bod_kódu_COUNT(String Spracovanie_textu) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Spracovanie_textu.length(); Loop_INDEX++, 수++) {
            int bod_kódu = Spracovanie_textu.charAt(Loop_INDEX);
            if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && Loop_INDEX + 1 < Spracovanie_textu.length() && Spracovanie_textu.charAt(Loop_INDEX + 1) >= 0xdc00 && Spracovanie_textu.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] kódovať(String Spracovanie_textu) {
        byte[] 임시 = new byte[Spracovanie_textu.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Spracovanie_textu.length(); Loop_INDEX++) {
            int bod_kódu = Spracovanie_textu.charAt(Loop_INDEX);
            if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && Loop_INDEX + 1 < Spracovanie_textu.length() && Spracovanie_textu.charAt(Loop_INDEX + 1) >= 0xdc00 && Spracovanie_textu.charAt(Loop_INDEX + 1) <= 0xdfff) bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + Spracovanie_textu.charAt(++Loop_INDEX) - 0xdc00;
            else if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) bod_kódu = '?';
            if (bod_kódu < 128) 임시[쓴수++] = (byte)bod_kódu;
            else if (bod_kódu < 2048) { 임시[쓴수++] = (byte)(192 | bod_kódu >> 6); 임시[쓴수++] = (byte)(128 | bod_kódu & 63); }
            else if (bod_kódu < 65536) { 임시[쓴수++] = (byte)(224 | bod_kódu >> 12); 임시[쓴수++] = (byte)(128 | bod_kódu >> 6 & 63); 임시[쓴수++] = (byte)(128 | bod_kódu & 63); }
            else { 임시[쓴수++] = (byte)(240 | bod_kódu >> 18); 임시[쓴수++] = (byte)(128 | bod_kódu >> 12 & 63); 임시[쓴수++] = (byte)(128 | bod_kódu >> 6 & 63); 임시[쓴수++] = (byte)(128 | bod_kódu & 63); }
        }
        byte[] KR = new byte[쓴수]; System.arraycopy(임시, 0, KR, 0, 쓴수); return KR;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dešifrovať_údaje(byte[] Byte_VALUE) {
        StringBuilder KR = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < Byte_VALUE.length;) {
            int bod_kódu = Byte_VALUE[Loop_INDEX++] & 255, 수 = bod_kódu < 128 ? 0 : bod_kódu >= 194 && bod_kódu < 224 ? 1 : bod_kódu >= 224 && bod_kódu < 240 ? 2 : bod_kódu >= 240 && bod_kódu <= 244 ? 3 : -1;
            if (수 < 0 || Byte_VALUE.length - Loop_INDEX < 수) throw new neplatné_argument_výnimka("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) bod_kódu &= (1 << (6 - 수)) - 1;
            for (int vnútorné_pozícia = 0; vnútorné_pozícia < 수; vnútorné_pozícia++) { int BACK_VALUE = Byte_VALUE[Loop_INDEX++] & 255; if ((BACK_VALUE & 192) != 128) throw new neplatné_argument_výnimka("잘못된 UTF-8"); bod_kódu = bod_kódu << 6 | BACK_VALUE & 63; }
            if (bod_kódu < 최소 || bod_kódu > 0x10ffff || bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) throw new neplatné_argument_výnimka("잘못된 UTF-8");
            if (bod_kódu < 65536) KR.append((char)bod_kódu);
            else { bod_kódu -= 65536; KR.append((char)(0xd800 | bod_kódu >> 10)); KR.append((char)(0xdc00 | bod_kódu & 1023)); }
        }
        return KR.toString();
    }
}
