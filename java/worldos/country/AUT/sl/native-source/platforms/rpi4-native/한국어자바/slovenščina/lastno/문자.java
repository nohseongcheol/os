// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** 문자(文字), kodiranje_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizirati_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bajt_COUNT(byte[] podatki) { return podatki.length; }
    private 문자() {}
    public static int 길이(String Besedilo) { return Besedilo.length(); }
    public static boolean 같음(String sprednja_VALUE, String ZAJ_VALUE) { return sprednja_VALUE == null ? ZAJ_VALUE == null : sprednja_VALUE.equals(ZAJ_VALUE); }
    public static String prilepiti_SMS(String sprednja_VALUE, String ZAJ_VALUE) { return sprednja_VALUE.concat(ZAJ_VALUE); }
    public static String rezati_VALUE(String Besedilo, int Zaženi, int 끝) { return Besedilo.substring(Zaženi, 끝); }
    public static int razčlenjevati_celo_število(String Besedilo) { try { return Integer.parseInt(Besedilo); } catch (NumberFormatException NAPAKA) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String pisati_celo_število_VALUE(int 수) { return Integer.toString(수); }
    public static int koda_znaka_COUNT(String Besedilo) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Besedilo.length(); Loop_INDEX++, 수++) {
            int koda_znaka = Besedilo.charAt(Loop_INDEX);
            if (koda_znaka >= 0xd800 && koda_znaka <= 0xdbff && Loop_INDEX + 1 < Besedilo.length() && Besedilo.charAt(Loop_INDEX + 1) >= 0xdc00 && Besedilo.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] kodirati(String Besedilo) {
        byte[] 임시 = new byte[Besedilo.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Besedilo.length(); Loop_INDEX++) {
            int koda_znaka = Besedilo.charAt(Loop_INDEX);
            if (koda_znaka >= 0xd800 && koda_znaka <= 0xdbff && Loop_INDEX + 1 < Besedilo.length() && Besedilo.charAt(Loop_INDEX + 1) >= 0xdc00 && Besedilo.charAt(Loop_INDEX + 1) <= 0xdfff) koda_znaka = 0x10000 + ((koda_znaka - 0xd800) << 10) + Besedilo.charAt(++Loop_INDEX) - 0xdc00;
            else if (koda_znaka >= 0xd800 && koda_znaka <= 0xdfff) koda_znaka = '?';
            if (koda_znaka < 128) 임시[쓴수++] = (byte)koda_znaka;
            else if (koda_znaka < 2048) { 임시[쓴수++] = (byte)(192 | koda_znaka >> 6); 임시[쓴수++] = (byte)(128 | koda_znaka & 63); }
            else if (koda_znaka < 65536) { 임시[쓴수++] = (byte)(224 | koda_znaka >> 12); 임시[쓴수++] = (byte)(128 | koda_znaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | koda_znaka & 63); }
            else { 임시[쓴수++] = (byte)(240 | koda_znaka >> 18); 임시[쓴수++] = (byte)(128 | koda_znaka >> 12 & 63); 임시[쓴수++] = (byte)(128 | koda_znaka >> 6 & 63); 임시[쓴수++] = (byte)(128 | koda_znaka & 63); }
        }
        byte[] REZULTAT = new byte[쓴수]; System.arraycopy(임시, 0, REZULTAT, 0, 쓴수); return REZULTAT;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dešifrirati_podatki(byte[] bajt_VALUE) {
        StringBuilder REZULTAT = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bajt_VALUE.length;) {
            int koda_znaka = bajt_VALUE[Loop_INDEX++] & 255, 수 = koda_znaka < 128 ? 0 : koda_znaka >= 194 && koda_znaka < 224 ? 1 : koda_znaka >= 224 && koda_znaka < 240 ? 2 : koda_znaka >= 240 && koda_znaka <= 244 ? 3 : -1;
            if (수 < 0 || bajt_VALUE.length - Loop_INDEX < 수) throw new neveljaven_argument_izjema("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) koda_znaka &= (1 << (6 - 수)) - 1;
            for (int notranje_položaj = 0; notranje_položaj < 수; notranje_položaj++) { int ZAJ_VALUE = bajt_VALUE[Loop_INDEX++] & 255; if ((ZAJ_VALUE & 192) != 128) throw new neveljaven_argument_izjema("잘못된 UTF-8"); koda_znaka = koda_znaka << 6 | ZAJ_VALUE & 63; }
            if (koda_znaka < 최소 || koda_znaka > 0x10ffff || koda_znaka >= 0xd800 && koda_znaka <= 0xdfff) throw new neveljaven_argument_izjema("잘못된 UTF-8");
            if (koda_znaka < 65536) REZULTAT.append((char)koda_znaka);
            else { koda_znaka -= 65536; REZULTAT.append((char)(0xd800 | koda_znaka >> 10)); REZULTAT.append((char)(0xdc00 | koda_znaka & 1023)); }
        }
        return REZULTAT.toString();
    }
}
