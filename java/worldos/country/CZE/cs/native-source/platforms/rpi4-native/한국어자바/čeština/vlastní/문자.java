// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** 문자(文字), Encoding_HODNOTA(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_HODNOTA. normalizovat_HODNOTA/složení_HODNOTA 입력기는 별개다. */
public final class 문자 {
    public static int bajt_POČET(byte[] data) { return data.length; }
    private 문자() {}
    public static int délka_HODNOTA(String text) { return text.length(); }
    public static boolean 같음(String přední_fotoaparát_HODNOTA, String BACK_HODNOTA) { return přední_fotoaparát_HODNOTA == null ? BACK_HODNOTA == null : přední_fotoaparát_HODNOTA.equals(BACK_HODNOTA); }
    public static String vložit_SMS(String přední_fotoaparát_HODNOTA, String BACK_HODNOTA) { return přední_fotoaparát_HODNOTA.concat(BACK_HODNOTA); }
    public static String stříhat_HODNOTA(String text, int Spustit_2, int 끝) { return text.substring(Spustit_2, 끝); }
    public static int parsovat_integer(String text) { try { return Integer.parseInt(text); } catch (NumberFormatException chyba) { throw new číslo_formát_selhání("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String zápis_integer_HODNOTA(int číslo) { return Integer.toString(číslo); }
    public static int bod_kódu_POČET(String text) {
        int číslo = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < text.length(); Loop_INDEX++, číslo++) {
            int bod_kódu = text.charAt(Loop_INDEX);
            if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && Loop_INDEX + 1 < text.length() && text.charAt(Loop_INDEX + 1) >= 0xdc00 && text.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return číslo;
    }
    public static byte[] kódovat(String text) {
        byte[] 임시 = new byte[text.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < text.length(); Loop_INDEX++) {
            int bod_kódu = text.charAt(Loop_INDEX);
            if (bod_kódu >= 0xd800 && bod_kódu <= 0xdbff && Loop_INDEX + 1 < text.length() && text.charAt(Loop_INDEX + 1) >= 0xdc00 && text.charAt(Loop_INDEX + 1) <= 0xdfff) bod_kódu = 0x10000 + ((bod_kódu - 0xd800) << 10) + text.charAt(++Loop_INDEX) - 0xdc00;
            else if (bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) bod_kódu = '?';
            if (bod_kódu < 128) 임시[쓴수++] = (byte)bod_kódu;
            else if (bod_kódu < 2048) { 임시[쓴수++] = (byte)(192 | bod_kódu >> 6); 임시[쓴수++] = (byte)(128 | bod_kódu & 63); }
            else if (bod_kódu < 65536) { 임시[쓴수++] = (byte)(224 | bod_kódu >> 12); 임시[쓴수++] = (byte)(128 | bod_kódu >> 6 & 63); 임시[쓴수++] = (byte)(128 | bod_kódu & 63); }
            else { 임시[쓴수++] = (byte)(240 | bod_kódu >> 18); 임시[쓴수++] = (byte)(128 | bod_kódu >> 12 & 63); 임시[쓴수++] = (byte)(128 | bod_kódu >> 6 & 63); 임시[쓴수++] = (byte)(128 | bod_kódu & 63); }
        }
        byte[] VÝSLEDEK = new byte[쓴수]; System.arraycopy(임시, 0, VÝSLEDEK, 0, 쓴수); return VÝSLEDEK;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dešifrovat_data(byte[] bajt_HODNOTA) {
        StringBuilder VÝSLEDEK = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bajt_HODNOTA.length;) {
            int bod_kódu = bajt_HODNOTA[Loop_INDEX++] & 255, číslo = bod_kódu < 128 ? 0 : bod_kódu >= 194 && bod_kódu < 224 ? 1 : bod_kódu >= 224 && bod_kódu < 240 ? 2 : bod_kódu >= 240 && bod_kódu <= 244 ? 3 : -1;
            if (číslo < 0 || bajt_HODNOTA.length - Loop_INDEX < číslo) throw new neplatný_argument_výjimka("잘못된 UTF-8");
            int 최소 = číslo == 1 ? 128 : číslo == 2 ? 2048 : číslo == 3 ? 65536 : 0;
            if (číslo > 0) bod_kódu &= (1 << (6 - číslo)) - 1;
            for (int vnitřní_pozice = 0; vnitřní_pozice < číslo; vnitřní_pozice++) { int BACK_HODNOTA = bajt_HODNOTA[Loop_INDEX++] & 255; if ((BACK_HODNOTA & 192) != 128) throw new neplatný_argument_výjimka("잘못된 UTF-8"); bod_kódu = bod_kódu << 6 | BACK_HODNOTA & 63; }
            if (bod_kódu < 최소 || bod_kódu > 0x10ffff || bod_kódu >= 0xd800 && bod_kódu <= 0xdfff) throw new neplatný_argument_výjimka("잘못된 UTF-8");
            if (bod_kódu < 65536) VÝSLEDEK.append((char)bod_kódu);
            else { bod_kódu -= 65536; VÝSLEDEK.append((char)(0xd800 | bod_kódu >> 10)); VÝSLEDEK.append((char)(0xdc00 | bod_kódu & 1023)); }
        }
        return VÝSLEDEK.toString();
    }
}
