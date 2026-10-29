// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** 문자(文字), kodning_VÆRDI(符號): UTF-8 바이트와 UTF-16 문자열의 KONVERTER_VÆRDI. normalisere_VÆRDI/komposition_VÆRDI 입력기는 별개다. */
public final class 문자 {
    public static int byte_TÆL(byte[] data) { return data.length; }
    private 문자() {}
    public static int varighed_VÆRDI(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String frontvendt_VÆRDI, String BACK_VÆRDI) { return frontvendt_VÆRDI == null ? BACK_VÆRDI == null : frontvendt_VÆRDI.equals(BACK_VÆRDI); }
    public static String sætte_ind_sms(String frontvendt_VÆRDI, String BACK_VÆRDI) { return frontvendt_VÆRDI.concat(BACK_VÆRDI); }
    public static String klip_VÆRDI(String Tekst, int Kør_2, int 끝) { return Tekst.substring(Kør_2, 끝); }
    public static int opdele_tekst_heltal(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException fejl) { throw new tal_format_fejl("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String skrive_heltal_VÆRDI(int tal) { return Integer.toString(tal); }
    public static int tegnkode_TÆL(String Tekst) {
        int tal = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < Tekst.length(); Loop_INDEKS++, tal++) {
            int tegnkode = Tekst.charAt(Loop_INDEKS);
            if (tegnkode >= 0xd800 && tegnkode <= 0xdbff && Loop_INDEKS + 1 < Tekst.length() && Tekst.charAt(Loop_INDEKS + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEKS + 1) <= 0xdfff) Loop_INDEKS++;
        }
        return tal;
    }
    public static byte[] kode(String Tekst) {
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
    public static String dekryptere_data(byte[] byte_VÆRDI) {
        StringBuilder KR = new StringBuilder();
        for (int Loop_INDEKS = 0; Loop_INDEKS < byte_VÆRDI.length;) {
            int tegnkode = byte_VÆRDI[Loop_INDEKS++] & 255, tal = tegnkode < 128 ? 0 : tegnkode >= 194 && tegnkode < 224 ? 1 : tegnkode >= 224 && tegnkode < 240 ? 2 : tegnkode >= 240 && tegnkode <= 244 ? 3 : -1;
            if (tal < 0 || byte_VÆRDI.length - Loop_INDEKS < tal) throw new ugyldig_argument_undtagelse("잘못된 UTF-8");
            int 최소 = tal == 1 ? 128 : tal == 2 ? 2048 : tal == 3 ? 65536 : 0;
            if (tal > 0) tegnkode &= (1 << (6 - tal)) - 1;
            for (int indre_placere = 0; indre_placere < tal; indre_placere++) { int BACK_VÆRDI = byte_VÆRDI[Loop_INDEKS++] & 255; if ((BACK_VÆRDI & 192) != 128) throw new ugyldig_argument_undtagelse("잘못된 UTF-8"); tegnkode = tegnkode << 6 | BACK_VÆRDI & 63; }
            if (tegnkode < 최소 || tegnkode > 0x10ffff || tegnkode >= 0xd800 && tegnkode <= 0xdfff) throw new ugyldig_argument_undtagelse("잘못된 UTF-8");
            if (tegnkode < 65536) KR.append((char)tegnkode);
            else { tegnkode -= 65536; KR.append((char)(0xd800 | tegnkode >> 10)); KR.append((char)(0xdc00 | tegnkode & 1023)); }
        }
        return KR.toString();
    }
}
