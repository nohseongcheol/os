// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 문자(文字), kodiranje_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizirati_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bajt_COUNT(byte[] podaci) { return podaci.length; }
    private 문자() {}
    public static int dužina_VALUE(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String 앞, String ZAD_VALUE) { return 앞 == null ? ZAD_VALUE == null : 앞.equals(ZAD_VALUE); }
    public static String zalijepiti_SMS(String 앞, String ZAD_VALUE) { return 앞.concat(ZAD_VALUE); }
    public static String izrezati_VALUE(String Tekst, int Pokreni, int 끝) { return Tekst.substring(Pokreni, 끝); }
    public static int raščlanjivati_cijeli_broj(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException GRESKA) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String pisati_cijeli_broj_VALUE(int 수) { return Integer.toString(수); }
    public static int kôd_znaka_COUNT(String Tekst) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++, 수++) {
            int kôd_znaka = Tekst.charAt(Loop_INDEX);
            if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] 부호화(String Tekst) {
        byte[] 임시 = new byte[Tekst.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++) {
            int kôd_znaka = Tekst.charAt(Loop_INDEX);
            if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) kôd_znaka = 0x10000 + ((kôd_znaka - 0xd800) << 10) + Tekst.charAt(++Loop_INDEX) - 0xdc00;
            else if (kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) kôd_znaka = '?';
            if (kôd_znaka < 128) 임시[쓴수++] = (byte)kôd_znaka;
            else if (kôd_znaka < 2048) { 임시[쓴수++] = (byte)(192 | kôd_znaka >> 6); 임시[쓴수++] = (byte)(128 | kôd_znaka & 63); }
            else if (kôd_znaka < 65536) { 임시[쓴수++] = (byte)(224 | kôd_znaka >> 12); 임시[쓴수++] = (byte)(128 | kôd_znaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | kôd_znaka & 63); }
            else { 임시[쓴수++] = (byte)(240 | kôd_znaka >> 18); 임시[쓴수++] = (byte)(128 | kôd_znaka >> 12 & 63); 임시[쓴수++] = (byte)(128 | kôd_znaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | kôd_znaka & 63); }
        }
        byte[] mjera = new byte[쓴수]; System.arraycopy(임시, 0, mjera, 0, 쓴수); return mjera;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dešifrirati_podaci(byte[] bajt_VALUE) {
        StringBuilder mjera = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bajt_VALUE.length;) {
            int kôd_znaka = bajt_VALUE[Loop_INDEX++] & 255, 수 = kôd_znaka < 128 ? 0 : kôd_znaka >= 194 && kôd_znaka < 224 ? 1 : kôd_znaka >= 224 && kôd_znaka < 240 ? 2 : kôd_znaka >= 240 && kôd_znaka <= 244 ? 3 : -1;
            if (수 < 0 || bajt_VALUE.length - Loop_INDEX < 수) throw new nevažeće_argument_izuzetak("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kôd_znaka &= (1 << (6 - 수)) - 1;
            for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 수; unutrašnje_spajanje_položaj++) { int ZAD_VALUE = bajt_VALUE[Loop_INDEX++] & 255; if ((ZAD_VALUE & 192) != 128) throw new nevažeće_argument_izuzetak("잘못된 UTF-8"); kôd_znaka = kôd_znaka << 6 | ZAD_VALUE & 63; }
            if (kôd_znaka < 최소 || kôd_znaka > 0x10ffff || kôd_znaka >= 0xd800 && kôd_znaka <= 0xdfff) throw new nevažeće_argument_izuzetak("잘못된 UTF-8");
            if (kôd_znaka < 65536) mjera.append((char)kôd_znaka);
            else { kôd_znaka -= 65536; mjera.append((char)(0xd800 | kôd_znaka >> 10)); mjera.append((char)(0xdc00 | kôd_znaka & 1023)); }
        }
        return mjera.toString();
    }
}
