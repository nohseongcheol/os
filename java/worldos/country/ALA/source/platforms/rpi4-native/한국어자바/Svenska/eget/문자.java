// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svenska.eget;
/** 문자(文字), kodning_värde(符號): UTF-8 바이트와 UTF-16 문자열의 KONVERTERA_värde. normalisera_värde/komposition_värde 입력기는 별개다. */
public final class 문자 {
    public static int byte_ANTAL(byte[] data) { return data.length; }
    private 문자() {}
    public static int längd_värde(String text) { return text.length(); }
    public static boolean 같음(String framåtvänd_värde, String BACK_värde) { return framåtvänd_värde == null ? BACK_värde == null : framåtvänd_värde.equals(BACK_värde); }
    public static String klistra_in_SMS(String framåtvänd_värde, String BACK_värde) { return framåtvänd_värde.concat(BACK_värde); }
    public static String klippa_värde(String text, int Kör, int 끝) { return text.substring(Kör, 끝); }
    public static int parsa_heltal(String text) { try { return Integer.parseInt(text); } catch (NumberFormatException fel) { throw new nummer_format_fel("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String skriva_heltal_värde(int nummer) { return Integer.toString(nummer); }
    public static int kodpunkt_ANTAL(String text) {
        int nummer = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < text.length(); Loop_INDEX++, nummer++) {
            int kodpunkt = text.charAt(Loop_INDEX);
            if (kodpunkt >= 0xd800 && kodpunkt <= 0xdbff && Loop_INDEX + 1 < text.length() && text.charAt(Loop_INDEX + 1) >= 0xdc00 && text.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return nummer;
    }
    public static byte[] koda(String text) {
        byte[] 임시 = new byte[text.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < text.length(); Loop_INDEX++) {
            int kodpunkt = text.charAt(Loop_INDEX);
            if (kodpunkt >= 0xd800 && kodpunkt <= 0xdbff && Loop_INDEX + 1 < text.length() && text.charAt(Loop_INDEX + 1) >= 0xdc00 && text.charAt(Loop_INDEX + 1) <= 0xdfff) kodpunkt = 0x10000 + ((kodpunkt - 0xd800) << 10) + text.charAt(++Loop_INDEX) - 0xdc00;
            else if (kodpunkt >= 0xd800 && kodpunkt <= 0xdfff) kodpunkt = '?';
            if (kodpunkt < 128) 임시[쓴수++] = (byte)kodpunkt;
            else if (kodpunkt < 2048) { 임시[쓴수++] = (byte)(192 | kodpunkt >> 6); 임시[쓴수++] = (byte)(128 | kodpunkt & 63); }
            else if (kodpunkt < 65536) { 임시[쓴수++] = (byte)(224 | kodpunkt >> 12); 임시[쓴수++] = (byte)(128 | kodpunkt >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodpunkt & 63); }
            else { 임시[쓴수++] = (byte)(240 | kodpunkt >> 18); 임시[쓴수++] = (byte)(128 | kodpunkt >> 12 & 63); 임시[쓴수++] = (byte)(128 | kodpunkt >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodpunkt & 63); }
        }
        byte[] RESULTAT = new byte[쓴수]; System.arraycopy(임시, 0, RESULTAT, 0, 쓴수); return RESULTAT;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String avkryptera_data(byte[] byte_värde) {
        StringBuilder RESULTAT = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < byte_värde.length;) {
            int kodpunkt = byte_värde[Loop_INDEX++] & 255, nummer = kodpunkt < 128 ? 0 : kodpunkt >= 194 && kodpunkt < 224 ? 1 : kodpunkt >= 224 && kodpunkt < 240 ? 2 : kodpunkt >= 240 && kodpunkt <= 244 ? 3 : -1;
            if (nummer < 0 || byte_värde.length - Loop_INDEX < nummer) throw new ogiltig_argument_fel("잘못된 UTF-8");
            int 최소 = nummer == 1 ? 128 : nummer == 2 ? 2048 : nummer == 3 ? 65536 : 0;
            if (nummer > 0) kodpunkt &= (1 << (6 - nummer)) - 1;
            for (int inre_koppling_placera = 0; inre_koppling_placera < nummer; inre_koppling_placera++) { int BACK_värde = byte_värde[Loop_INDEX++] & 255; if ((BACK_värde & 192) != 128) throw new ogiltig_argument_fel("잘못된 UTF-8"); kodpunkt = kodpunkt << 6 | BACK_värde & 63; }
            if (kodpunkt < 최소 || kodpunkt > 0x10ffff || kodpunkt >= 0xd800 && kodpunkt <= 0xdfff) throw new ogiltig_argument_fel("잘못된 UTF-8");
            if (kodpunkt < 65536) RESULTAT.append((char)kodpunkt);
            else { kodpunkt -= 65536; RESULTAT.append((char)(0xd800 | kodpunkt >> 10)); RESULTAT.append((char)(0xdc00 | kodpunkt & 1023)); }
        }
        return RESULTAT.toString();
    }
}
