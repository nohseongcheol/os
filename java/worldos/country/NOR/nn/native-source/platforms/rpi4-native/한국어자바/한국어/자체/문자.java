// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), koding_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalisere_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_COUNT(byte[] data) { return data.length; }
    private 문자() {}
    public static int lengd_VALUE(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String 앞, String TILBAKE_VALUE) { return 앞 == null ? TILBAKE_VALUE == null : 앞.equals(TILBAKE_VALUE); }
    public static String lime_inn_SMS(String 앞, String TILBAKE_VALUE) { return 앞.concat(TILBAKE_VALUE); }
    public static String klippe_VALUE(String Tekst, int Køyr_2, int 끝) { return Tekst.substring(Køyr_2, 끝); }
    public static int dele_opp_heiltal(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException FEIL) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String skrive_heiltal_VALUE(int 수) { return Integer.toString(수); }
    public static int teiknkode_COUNT(String Tekst) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++, 수++) {
            int teiknkode = Tekst.charAt(Loop_INDEX);
            if (teiknkode >= 0xd800 && teiknkode <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Tekst) {
        byte[] 임시 = new byte[Tekst.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++) {
            int teiknkode = Tekst.charAt(Loop_INDEX);
            if (teiknkode >= 0xd800 && teiknkode <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) teiknkode = 0x10000 + ((teiknkode - 0xd800) << 10) + Tekst.charAt(++Loop_INDEX) - 0xdc00;
            else if (teiknkode >= 0xd800 && teiknkode <= 0xdfff) teiknkode = '?';
            if (teiknkode < 128) 임시[쓴수++] = (byte)teiknkode;
            else if (teiknkode < 2048) { 임시[쓴수++] = (byte)(192 | teiknkode >> 6); 임시[쓴수++] = (byte)(128 | teiknkode & 63); }
            else if (teiknkode < 65536) { 임시[쓴수++] = (byte)(224 | teiknkode >> 12); 임시[쓴수++] = (byte)(128 | teiknkode >> 6 & 63); 임시[쓴수++] = (byte)(128 | teiknkode & 63); }
            else { 임시[쓴수++] = (byte)(240 | teiknkode >> 18); 임시[쓴수++] = (byte)(128 | teiknkode >> 12 & 63); 임시[쓴수++] = (byte)(128 | teiknkode >> 6 & 63); 임시[쓴수++] = (byte)(128 | teiknkode & 63); }
        }
        byte[] forretningsmål = new byte[쓴수]; System.arraycopy(임시, 0, forretningsmål, 0, 쓴수); return forretningsmål;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dekryptere_data(byte[] byte_VALUE) {
        StringBuilder forretningsmål = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_VALUE.length;) {
            int teiknkode = byte_VALUE[Loop_INDEX++] & 255, 수 = teiknkode < 128 ? 0 : teiknkode >= 194 && teiknkode < 224 ? 1 : teiknkode >= 224 && teiknkode < 240 ? 2 : teiknkode >= 240 && teiknkode <= 244 ? 3 : -1;
            if (수 < 0 || byte_VALUE.length - Loop_INDEX < 수) throw new ugyldig_argument_unntak("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) teiknkode &= (1 << (6 - 수)) - 1;
            for (int indre_kopling_plassere = 0; indre_kopling_plassere < 수; indre_kopling_plassere++) { int TILBAKE_VALUE = byte_VALUE[Loop_INDEX++] & 255; if ((TILBAKE_VALUE & 192) != 128) throw new ugyldig_argument_unntak("잘못된 UTF-8"); teiknkode = teiknkode << 6 | TILBAKE_VALUE & 63; }
            if (teiknkode < 최소 || teiknkode > 0x10ffff || teiknkode >= 0xd800 && teiknkode <= 0xdfff) throw new ugyldig_argument_unntak("잘못된 UTF-8");
            if (teiknkode < 65536) forretningsmål.append((char)teiknkode);
            else { teiknkode -= 65536; forretningsmål.append((char)(0xd800 | teiknkode >> 10)); forretningsmål.append((char)(0xdc00 | teiknkode & 1023)); }
        }
        return forretningsmål.toString();
    }
}
