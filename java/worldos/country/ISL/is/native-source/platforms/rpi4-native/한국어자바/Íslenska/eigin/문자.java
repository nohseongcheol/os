// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** 문자(文字), kóðun_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. staðla_VALUE/samsetning_VALUE 입력기는 별개다. */
public final class 문자 {
    public static int bæti_COUNT(byte[] gögn) { return gögn.length; }
    private 문자() {}
    public static int lengd_VALUE(String Texti) { return Texti.length(); }
    public static boolean 같음(String myndavél_að_framan_VALUE, String TIL_BAKA_VALUE) { return myndavél_að_framan_VALUE == null ? TIL_BAKA_VALUE == null : myndavél_að_framan_VALUE.equals(TIL_BAKA_VALUE); }
    public static String líma_SMS(String myndavél_að_framan_VALUE, String TIL_BAKA_VALUE) { return myndavél_að_framan_VALUE.concat(TIL_BAKA_VALUE); }
    public static String klippa_VALUE(String Texti, int Keyra_2, int 끝) { return Texti.substring(Keyra_2, 끝); }
    public static int þátta_heiltala(String Texti) { try { return Integer.parseInt(Texti); } catch (NumberFormatException Villa) { throw new númer_snið_bilun("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String skrifa_heiltala_VALUE(int númer) { return Integer.toString(númer); }
    public static int stafkóði_COUNT(String Texti) {
        int númer = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Texti.length(); Loop_INDEX++, númer++) {
            int stafkóði = Texti.charAt(Loop_INDEX);
            if (stafkóði >= 0xd800 && stafkóði <= 0xdbff && Loop_INDEX + 1 < Texti.length() && Texti.charAt(Loop_INDEX + 1) >= 0xdc00 && Texti.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return númer;
    }
    public static byte[] 부호화(String Texti) {
        byte[] 임시 = new byte[Texti.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Texti.length(); Loop_INDEX++) {
            int stafkóði = Texti.charAt(Loop_INDEX);
            if (stafkóði >= 0xd800 && stafkóði <= 0xdbff && Loop_INDEX + 1 < Texti.length() && Texti.charAt(Loop_INDEX + 1) >= 0xdc00 && Texti.charAt(Loop_INDEX + 1) <= 0xdfff) stafkóði = 0x10000 + ((stafkóði - 0xd800) << 10) + Texti.charAt(++Loop_INDEX) - 0xdc00;
            else if (stafkóði >= 0xd800 && stafkóði <= 0xdfff) stafkóði = '?';
            if (stafkóði < 128) 임시[쓴수++] = (byte)stafkóði;
            else if (stafkóði < 2048) { 임시[쓴수++] = (byte)(192 | stafkóði >> 6); 임시[쓴수++] = (byte)(128 | stafkóði & 63); }
            else if (stafkóði < 65536) { 임시[쓴수++] = (byte)(224 | stafkóði >> 12); 임시[쓴수++] = (byte)(128 | stafkóði >> 6 & 63); 임시[쓴수++] = (byte)(128 | stafkóði & 63); }
            else { 임시[쓴수++] = (byte)(240 | stafkóði >> 18); 임시[쓴수++] = (byte)(128 | stafkóði >> 12 & 63); 임시[쓴수++] = (byte)(128 | stafkóði >> 6 & 63); 임시[쓴수++] = (byte)(128 | stafkóði & 63); }
        }
        byte[] NIÐURSTAÐA = new byte[쓴수]; System.arraycopy(임시, 0, NIÐURSTAÐA, 0, 쓴수); return NIÐURSTAÐA;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dulráða_gögn(byte[] bæti_VALUE) {
        StringBuilder NIÐURSTAÐA = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bæti_VALUE.length;) {
            int stafkóði = bæti_VALUE[Loop_INDEX++] & 255, númer = stafkóði < 128 ? 0 : stafkóði >= 194 && stafkóði < 224 ? 1 : stafkóði >= 224 && stafkóði < 240 ? 2 : stafkóði >= 240 && stafkóði <= 244 ? 3 : -1;
            if (númer < 0 || bæti_VALUE.length - Loop_INDEX < númer) throw new ógilt_frumbreyta_undantekning("잘못된 UTF-8");
            int 최소 = númer == 1 ? 128 : númer == 2 ? 2048 : númer == 3 ? 65536 : 0;
            if (númer > 0) stafkóði &= (1 << (6 - númer)) - 1;
            for (int innri_samtenging_staða = 0; innri_samtenging_staða < númer; innri_samtenging_staða++) { int TIL_BAKA_VALUE = bæti_VALUE[Loop_INDEX++] & 255; if ((TIL_BAKA_VALUE & 192) != 128) throw new ógilt_frumbreyta_undantekning("잘못된 UTF-8"); stafkóði = stafkóði << 6 | TIL_BAKA_VALUE & 63; }
            if (stafkóði < 최소 || stafkóði > 0x10ffff || stafkóði >= 0xd800 && stafkóði <= 0xdfff) throw new ógilt_frumbreyta_undantekning("잘못된 UTF-8");
            if (stafkóði < 65536) NIÐURSTAÐA.append((char)stafkóði);
            else { stafkóði -= 65536; NIÐURSTAÐA.append((char)(0xd800 | stafkóði >> 10)); NIÐURSTAÐA.append((char)(0xdc00 | stafkóði & 1023)); }
        }
        return NIÐURSTAÐA.toString();
    }
}
