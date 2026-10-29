// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** 문자(文字), šifriranje_VALUE(符號): UTF-8 바이트와 UTF-16 문자열의 CONVERT_VALUE. normalizirati_VALUE/조합 입력기는 별개다. */
public final class 문자 {
    public static int bajt_COUNT(byte[] podaci) { return podaci.length; }
    private 문자() {}
    public static int 길이(String Tekst) { return Tekst.length(); }
    public static boolean 같음(String prednja_VALUE, String TRAG_VALUE) { return prednja_VALUE == null ? TRAG_VALUE == null : prednja_VALUE.equals(TRAG_VALUE); }
    public static String zalijepiti_SMS(String prednja_VALUE, String TRAG_VALUE) { return prednja_VALUE.concat(TRAG_VALUE); }
    public static String izrezati_VALUE(String Tekst, int Pokreni, int 끝) { return Tekst.substring(Pokreni, 끝); }
    public static int rastavljati_cijeli_broj(String Tekst) { try { return Integer.parseInt(Tekst); } catch (NumberFormatException GREŠKA) { throw new 숫자형식예외("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String zapisivanje_cijeli_broj_VALUE(int 수) { return Integer.toString(수); }
    public static int točka_koda_COUNT(String Tekst) {
        int 수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++, 수++) {
            int kodna_točka = Tekst.charAt(Loop_INDEX);
            if (kodna_točka >= 0xd800 && kodna_točka <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) Loop_INDEX++;
        }
        return 수;
    }
    public static byte[] kodirati(String Tekst) {
        byte[] 임시 = new byte[Tekst.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEX = 0; Loop_INDEX < Tekst.length(); Loop_INDEX++) {
            int kodna_točka = Tekst.charAt(Loop_INDEX);
            if (kodna_točka >= 0xd800 && kodna_točka <= 0xdbff && Loop_INDEX + 1 < Tekst.length() && Tekst.charAt(Loop_INDEX + 1) >= 0xdc00 && Tekst.charAt(Loop_INDEX + 1) <= 0xdfff) kodna_točka = 0x10000 + ((kodna_točka - 0xd800) << 10) + Tekst.charAt(++Loop_INDEX) - 0xdc00;
            else if (kodna_točka >= 0xd800 && kodna_točka <= 0xdfff) kodna_točka = '?';
            if (kodna_točka < 128) 임시[쓴수++] = (byte)kodna_točka;
            else if (kodna_točka < 2048) { 임시[쓴수++] = (byte)(192 | kodna_točka >> 6); 임시[쓴수++] = (byte)(128 | kodna_točka & 63); }
            else if (kodna_točka < 65536) { 임시[쓴수++] = (byte)(224 | kodna_točka >> 12); 임시[쓴수++] = (byte)(128 | kodna_točka >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodna_točka & 63); }
            else { 임시[쓴수++] = (byte)(240 | kodna_točka >> 18); 임시[쓴수++] = (byte)(128 | kodna_točka >> 12 & 63); 임시[쓴수++] = (byte)(128 | kodna_točka >> 6 & 63); 임시[쓴수++] = (byte)(128 | kodna_točka & 63); }
        }
        byte[] REZULTAT = new byte[쓴수]; System.arraycopy(임시, 0, REZULTAT, 0, 쓴수); return REZULTAT;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String dešifrirati_podaci(byte[] bajt_VALUE) {
        StringBuilder REZULTAT = new StringBuilder();
        for (int Loop_INDEX = 0; Loop_INDEX < bajt_VALUE.length;) {
            int kodna_točka = bajt_VALUE[Loop_INDEX++] & 255, 수 = kodna_točka < 128 ? 0 : kodna_točka >= 194 && kodna_točka < 224 ? 1 : kodna_točka >= 224 && kodna_točka < 240 ? 2 : kodna_točka >= 240 && kodna_točka <= 244 ? 3 : -1;
            if (수 < 0 || bajt_VALUE.length - Loop_INDEX < 수) throw new nevaljan_argument_iznimka("잘못된 UTF-8");
            int 최소 = 수 == 1 ? 128 : 수 == 2 ? 2048 : 수 == 3 ? 65536 : 0;
            if (수 > 0) kodna_točka &= (1 << (6 - 수)) - 1;
            for (int unutarnji_položaj = 0; unutarnji_položaj < 수; unutarnji_položaj++) { int TRAG_VALUE = bajt_VALUE[Loop_INDEX++] & 255; if ((TRAG_VALUE & 192) != 128) throw new nevaljan_argument_iznimka("잘못된 UTF-8"); kodna_točka = kodna_točka << 6 | TRAG_VALUE & 63; }
            if (kodna_točka < 최소 || kodna_točka > 0x10ffff || kodna_točka >= 0xd800 && kodna_točka <= 0xdfff) throw new nevaljan_argument_iznimka("잘못된 UTF-8");
            if (kodna_točka < 65536) REZULTAT.append((char)kodna_točka);
            else { kodna_točka -= 65536; REZULTAT.append((char)(0xd800 | kodna_točka >> 10)); REZULTAT.append((char)(0xdc00 | kodna_točka & 1023)); }
        }
        return REZULTAT.toString();
    }
}
