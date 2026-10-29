// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;
/** 문자(文字), Encoding_WAARDE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERTEREN_WAARDE. normaliseren_WAARDE/samenstelling_WAARDE 입력기는 별개다. */
public final class 문자 {
    public static int byte_AANTAL(byte[] gegevens) { return gegevens.length; }
    private 문자() {}
    public static int tijdsduur_WAARDE(String tekst) { return tekst.length(); }
    public static boolean 같음(String voorkant_WAARDE, String BACK_WAARDE) { return voorkant_WAARDE == null ? BACK_WAARDE == null : voorkant_WAARDE.equals(BACK_WAARDE); }
    public static String plakken_sms(String voorkant_WAARDE, String BACK_WAARDE) { return voorkant_WAARDE.concat(BACK_WAARDE); }
    public static String knippen_WAARDE(String tekst, int starten, int 끝) { return tekst.substring(starten, 끝); }
    public static int parseren_geheel_getal(String tekst) { try { return Integer.parseInt(tekst); } catch (NumberFormatException fout) { throw new nummer_opmaak_fout("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String schrijven_geheel_getal_WAARDE(int nummer) { return Integer.toString(nummer); }
    public static int codepoint_AANTAL(String tekst) {
        int nummer = 0;
        for (int lus_INDEX = 0; lus_INDEX < tekst.length(); lus_INDEX++, nummer++) {
            int codepoint = tekst.charAt(lus_INDEX);
            if (codepoint >= 0xd800 && codepoint <= 0xdbff && lus_INDEX + 1 < tekst.length() && tekst.charAt(lus_INDEX + 1) >= 0xdc00 && tekst.charAt(lus_INDEX + 1) <= 0xdfff) lus_INDEX++;
        }
        return nummer;
    }
    public static byte[] coderen(String tekst) {
        byte[] 임시 = new byte[tekst.length() * 3]; int 쓴수 = 0;
        for (int lus_INDEX = 0; lus_INDEX < tekst.length(); lus_INDEX++) {
            int codepoint = tekst.charAt(lus_INDEX);
            if (codepoint >= 0xd800 && codepoint <= 0xdbff && lus_INDEX + 1 < tekst.length() && tekst.charAt(lus_INDEX + 1) >= 0xdc00 && tekst.charAt(lus_INDEX + 1) <= 0xdfff) codepoint = 0x10000 + ((codepoint - 0xd800) << 10) + tekst.charAt(++lus_INDEX) - 0xdc00;
            else if (codepoint >= 0xd800 && codepoint <= 0xdfff) codepoint = '?';
            if (codepoint < 128) 임시[쓴수++] = (byte)codepoint;
            else if (codepoint < 2048) { 임시[쓴수++] = (byte)(192 | codepoint >> 6); 임시[쓴수++] = (byte)(128 | codepoint & 63); }
            else if (codepoint < 65536) { 임시[쓴수++] = (byte)(224 | codepoint >> 12); 임시[쓴수++] = (byte)(128 | codepoint >> 6 & 63); 임시[쓴수++] = (byte)(128 | codepoint & 63); }
            else { 임시[쓴수++] = (byte)(240 | codepoint >> 18); 임시[쓴수++] = (byte)(128 | codepoint >> 12 & 63); 임시[쓴수++] = (byte)(128 | codepoint >> 6 & 63); 임시[쓴수++] = (byte)(128 | codepoint & 63); }
        }
        byte[] resultaat = new byte[쓴수]; System.arraycopy(임시, 0, resultaat, 0, 쓴수); return resultaat;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String ontsleutelen_gegevens(byte[] byte_WAARDE) {
        StringBuilder resultaat = new StringBuilder();
        for (int lus_INDEX = 0; lus_INDEX < byte_WAARDE.length;) {
            int codepoint = byte_WAARDE[lus_INDEX++] & 255, nummer = codepoint < 128 ? 0 : codepoint >= 194 && codepoint < 224 ? 1 : codepoint >= 224 && codepoint < 240 ? 2 : codepoint >= 240 && codepoint <= 244 ? 3 : -1;
            if (nummer < 0 || byte_WAARDE.length - lus_INDEX < nummer) throw new nietig_argument_uitzondering("잘못된 UTF-8");
            int 최소 = nummer == 1 ? 128 : nummer == 2 ? 2048 : nummer == 3 ? 65536 : 0;
            if (nummer > 0) codepoint &= (1 << (6 - nummer)) - 1;
            for (int inner_functie = 0; inner_functie < nummer; inner_functie++) { int BACK_WAARDE = byte_WAARDE[lus_INDEX++] & 255; if ((BACK_WAARDE & 192) != 128) throw new nietig_argument_uitzondering("잘못된 UTF-8"); codepoint = codepoint << 6 | BACK_WAARDE & 63; }
            if (codepoint < 최소 || codepoint > 0x10ffff || codepoint >= 0xd800 && codepoint <= 0xdfff) throw new nietig_argument_uitzondering("잘못된 UTF-8");
            if (codepoint < 65536) resultaat.append((char)codepoint);
            else { codepoint -= 65536; resultaat.append((char)(0xd800 | codepoint >> 10)); resultaat.append((char)(0xdc00 | codepoint & 1023)); }
        }
        return resultaat.toString();
    }
}
