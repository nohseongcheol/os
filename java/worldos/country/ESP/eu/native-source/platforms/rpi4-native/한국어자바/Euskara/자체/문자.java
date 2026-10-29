// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 문자(文字), kodeketa_balio(符號): UTF-8 바이트와 UTF-16 문자열의 BIHURTU_balio. normalizatu_balio/조합 입력기는 별개다. */
public final class 문자 {
    public static int byte_ZENBATU(byte[] datuak) { return datuak.length; }
    private 문자() {}
    public static int luzera_balio(String Testua) { return Testua.length(); }
    public static boolean 같음(String aurrekoa_balio, String ATZERA_balio) { return aurrekoa_balio == null ? ATZERA_balio == null : aurrekoa_balio.equals(ATZERA_balio); }
    public static String itsatsi_SMS(String aurrekoa_balio, String ATZERA_balio) { return aurrekoa_balio.concat(ATZERA_balio); }
    public static String ebaki_balio(String Testua, int Exekutatu_2, int 끝) { return Testua.substring(Exekutatu_2, 끝); }
    public static int analizatu_osoko_zenbaki(String Testua) { try { return Integer.parseInt(Testua); } catch (NumberFormatException errorea) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String idatzi_osoko_zenbaki_balio(int 수) { return Integer.toString(수); }
    public static int karaktere_kode_ZENBATU(String Testua) {
        int 수 = 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Testua.length(); Loop_INDIZE++, 수++) {
            int karaktere_kode = Testua.charAt(Loop_INDIZE);
            if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdbff && Loop_INDIZE + 1 < Testua.length() && Testua.charAt(Loop_INDIZE + 1) >= 0xdc00 && Testua.charAt(Loop_INDIZE + 1) <= 0xdfff) Loop_INDIZE++;
        }
        return 수;
    }
    public static byte[] 부호화(String Testua) {
        byte[] 임시 = new byte[Testua.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDIZE = 0; Loop_INDIZE < Testua.length(); Loop_INDIZE++) {
            int karaktere_kode = Testua.charAt(Loop_INDIZE);
            if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdbff && Loop_INDIZE + 1 < Testua.length() && Testua.charAt(Loop_INDIZE + 1) >= 0xdc00 && Testua.charAt(Loop_INDIZE + 1) <= 0xdfff) karaktere_kode = 0x10000 + ((karaktere_kode - 0xd800) << 10) + Testua.charAt(++Loop_INDIZE) - 0xdc00;
            else if (karaktere_kode >= 0xd800 && karaktere_kode <= 0xdfff) karaktere_kode = '?';
            if (karaktere_kode < 128) 임시[쓴수++] = (byte)karaktere_kode;
            else if (karaktere_kode < 2048) { 임시[쓴수++] = (byte)(192 | karaktere_kode >> 6); 임시[쓴수++] = (byte)(128 | karaktere_kode & 63); }
            else if (karaktere_kode < 65536) { 임시[쓴수++] = (byte)(224 | karaktere_kode >> 12); 임시[쓴수++] = (byte)(128 | karaktere_kode >> 6 & 63); 임시[쓴수++] = (byte)(128 | karaktere_kode & 63); }
            else { 임시[쓴수++] = (byte)(240 | karaktere_kode >> 18); 임시[쓴수++] = (byte)(128 | karaktere_kode >> 12 & 63); 임시[쓴수++] = (byte)(128 | karaktere_kode >> 6 & 63); 임시[쓴수++] = (byte)(128 | karaktere_kode & 63); }
        }
        byte[] EMAITZA = new byte[쓴수]; System.arraycopy(임시, 0, EMAITZA, 0, 쓴수); return EMAITZA;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String desenkriptatu_datuak(byte[] byte_balio) {
        StringBuilder EMAITZA = new StringBuilder();
        for (int Loop_INDIZE = 0; Loop_INDIZE < byte_balio.length;) {
            int karaktere_kode = byte_balio[Loop_INDIZE++] & 255, 수 = karaktere_kode < 128 ? 0 : karaktere_kode >= 194 && karaktere_kode < 224 ? 1 : karaktere_kode >= 224 && karaktere_kode < 240 ? 2 : karaktere_kode >= 240 && karaktere_kode <= 244 ? 3 : -1;
            if (수 < 0 || byte_balio.length - Loop_INDIZE < 수) throw new baliogabe_arg_salbuespen("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) karaktere_kode &= (1 << (6 - 수)) - 1;
            for (int barnekoa_kargu = 0; barnekoa_kargu < 수; barnekoa_kargu++) { int ATZERA_balio = byte_balio[Loop_INDIZE++] & 255; if ((ATZERA_balio & 192) != 128) throw new baliogabe_arg_salbuespen("잘못된 UTF-8"); karaktere_kode = karaktere_kode << 6 | ATZERA_balio & 63; }
            if (karaktere_kode < 최소 || karaktere_kode > 0x10ffff || karaktere_kode >= 0xd800 && karaktere_kode <= 0xdfff) throw new baliogabe_arg_salbuespen("잘못된 UTF-8");
            if (karaktere_kode < 65536) EMAITZA.append((char)karaktere_kode);
            else { karaktere_kode -= 65536; EMAITZA.append((char)(0xd800 | karaktere_kode >> 10)); EMAITZA.append((char)(0xdc00 | karaktere_kode & 1023)); }
        }
        return EMAITZA.toString();
    }
}
