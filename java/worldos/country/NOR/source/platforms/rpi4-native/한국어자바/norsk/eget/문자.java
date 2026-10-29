// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;
/** 문자(文字), koding_VERDI(符號): UTF-8 바이트와 UTF-16 문자열의 KONVERTER_VERDI. normalisere_VERDI/sammensetning_VERDI 입력기는 별개다. */
public final class 문자 {
    public static int byte_ANTALL(byte[] data) { return data.length; }
    private 문자() {}
    public static int lengde_VERDI(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String frontkamera_VERDI, String TILBAKE_VERDI) { return frontkamera_VERDI == null ? TILBAKE_VERDI == null : frontkamera_VERDI.equals(TILBAKE_VERDI); }
    public static String lime_inn_SMS(String frontkamera_VERDI, String TILBAKE_VERDI) { return frontkamera_VERDI.concat(TILBAKE_VERDI); }
    public static String klippe_VERDI_4601577b(String Tekst, int Kjør_2, int 끝) { return Tekst.substring(Kjør_2, 끝); }
    public static int dele_opp_heltall(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException feil) { throw new nummer_format_feil("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String skrive_heltall_VERDI(int nummer) { return Integer.toString(nummer); }
    public static int tegnkode_ANTALL(String Tekst) {
        int nummer = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Tekst.length(); Loop_INDEKS++, nummer++) {
            int tegnkode = Tekst.charAt(Loop_INDEKS);
            if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && Loop_INDEKS + 1 < Tekst.length() && Tekst.charAt(Loop_INDEKS + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEKS + 1) <= 0xdfff) Loop_INDEKS++;
        }
        return nummer;
    }
    public static byte[] 부호화(String Tekst) {
        byte[] 임시 = new byte[Tekst.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Tekst.length(); Loop_INDEKS++) {
            int tegnkode = Tekst.charAt(Loop_INDEKS);
            if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && Loop_INDEKS + 1 < Tekst.length() && Tekst.charAt(Loop_INDEKS + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEKS + 1) <= 0xdfff) tegnkode = 0x10000 + ((tegnkode - 0xd800) << 10) + Tekst.charAt(++Loop_INDEKS) - 0xdc00;
            else if (tegnkode >= 0xd800 && tegnkode <= 0xdfff) tegnkode = '?';
            if (tegnkode < 128) 임시[쓴수++] = (byte)tegnkode;
            else if (tegnkode < 2048) { 임시[쓴수++] = (byte)(192 | tegnkode >> 6); 임시[쓴수++] = (byte)(128 | tegnkode & 63); }
            else if (tegnkode < 65536) { 임시[쓴수++] = (byte)(224 | tegnkode >> 12); 임시[쓴수++] = (byte)(128 | tegnkode >> 6 & 63); 임시[쓴수++] = (byte)(128 | tegnkode & 63); }
            else { 임시[쓴수++] = (byte)(240 | tegnkode >> 18); 임시[쓴수++] = (byte)(128 | tegnkode >> 12 & 63); 임시[쓴수++] = (byte)(128 | tegnkode >> 6 & 63); 임시[쓴수++] = (byte)(128 | tegnkode & 63); }
        }
        byte[] KR = new byte[쓴수]; System.arraycopy(임시, 0, KR, 0, 쓴수); return KR;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dekryptere_data(byte[] byte_VERDI) {
        StringBuilder KR = new StringBuilder();
        for (int Loop_INDEKS = 0; Loop_INDEKS < byte_VERDI.length;) {
            int tegnkode = byte_VERDI[Loop_INDEKS++] & 255, nummer = tegnkode < 128 ? 0 : tegnkode >= 194 && tegnkode < 224 ? 1 : tegnkode >= 224 && tegnkode < 240 ? 2 : tegnkode >= 240 && tegnkode <= 244 ? 3 : -1;
            if (nummer < 0 || byte_VERDI.length - Loop_INDEKS < nummer) throw new ugyldig_argument_unntak("잘못된 UTF-8");
            int 최소 = nummer == 1 ? 128 : nummer == 2 ? 2048 : nummer == 3 ? 65536 : 0;
            if (nummer > 0) tegnkode &= (1 << (6 - nummer)) - 1;
            for (int indre_kobling_plassere = 0; indre_kobling_plassere < nummer; indre_kobling_plassere++) { int TILBAKE_VERDI = byte_VERDI[Loop_INDEKS++] & 255; if ((TILBAKE_VERDI & 192) != 128) throw new ugyldig_argument_unntak("잘못된 UTF-8"); tegnkode = tegnkode << 6 | TILBAKE_VERDI & 63; }
            if (tegnkode < 최소 || tegnkode > 0x10ffff || tegnkode >= 0xd800 && tegnkode <= 0xdfff) throw new ugyldig_argument_unntak("잘못된 UTF-8");
            if (tegnkode < 65536) KR.append((char)tegnkode);
            else { tegnkode -= 65536; KR.append((char)(0xd800 | tegnkode >> 10)); KR.append((char)(0xdc00 | tegnkode & 1023)); }
        }
        return KR.toString();
    }
}
