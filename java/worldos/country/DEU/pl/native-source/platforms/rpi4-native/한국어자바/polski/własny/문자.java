// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** 문자(文字), Encoding_WARTOŚĆ(符號): UTF-8 바이트와 UTF-16 문자열의 KONWERTUJ_WARTOŚĆ. normalizować_WARTOŚĆ/kompozycja_WARTOŚĆ 입력기는 별개다. */
public final class 문자 {
    public static int bajt_ILE_LICZB(byte[] dane) { return dane.length; }
    private 문자() {}
    public static int długość_WARTOŚĆ(String tekst) { return tekst.length(); }
    public static boolean 같음(String przód_WARTOŚĆ, String BACK_WARTOŚĆ) { return przód_WARTOŚĆ == null ? BACK_WARTOŚĆ == null : przód_WARTOŚĆ.equals(BACK_WARTOŚĆ); }
    public static String wkleić_SMS(String przód_WARTOŚĆ, String BACK_WARTOŚĆ) { return przód_WARTOŚĆ.concat(BACK_WARTOŚĆ); }
    public static String wyciąć_WARTOŚĆ(String tekst, int Uruchom_2, int 끝) { return tekst.substring(Uruchom_2, 끝); }
    public static int analizować_liczba_całkowita(String tekst) { try { return Integer.parseInt(tekst); } catch (NumberFormatException błąd) { throw new identyfikator_format_awaria("숫자의 형식이나 범위를 확인하십시오."); } }
    public static String zapis_liczba_całkowita_WARTOŚĆ(int identyfikator) { return Integer.toString(identyfikator); }
    public static int kod_znaku_ILE_LICZB(String tekst) {
        int identyfikator = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < tekst.length(); Loop_INDEKS++, identyfikator++) {
            int kod_znaku = tekst.charAt(Loop_INDEKS);
            if (kod_znaku >= 0xd800 && kod_znaku <= 0xdbff && Loop_INDEKS + 1 < tekst.length() && tekst.charAt(Loop_INDEKS + 1) >= 0xdc00 && tekst.charAt(Loop_INDEKS + 1) <= 0xdfff) Loop_INDEKS++;
        }
        return identyfikator;
    }
    public static byte[] kodować(String tekst) {
        byte[] 임시 = new byte[tekst.length() * 3]; int 쓴수 = 0;
        for (int Loop_INDEKS = 0; Loop_INDEKS < tekst.length(); Loop_INDEKS++) {
            int kod_znaku = tekst.charAt(Loop_INDEKS);
            if (kod_znaku >= 0xd800 && kod_znaku <= 0xdbff && Loop_INDEKS + 1 < tekst.length() && tekst.charAt(Loop_INDEKS + 1) >= 0xdc00 && tekst.charAt(Loop_INDEKS + 1) <= 0xdfff) kod_znaku = 0x10000 + ((kod_znaku - 0xd800) << 10) + tekst.charAt(++Loop_INDEKS) - 0xdc00;
            else if (kod_znaku >= 0xd800 && kod_znaku <= 0xdfff) kod_znaku = '?';
            if (kod_znaku < 128) 임시[쓴수++] = (byte)kod_znaku;
            else if (kod_znaku < 2048) { 임시[쓴수++] = (byte)(192 | kod_znaku >> 6); 임시[쓴수++] = (byte)(128 | kod_znaku & 63); }
            else if (kod_znaku < 65536) { 임시[쓴수++] = (byte)(224 | kod_znaku >> 12); 임시[쓴수++] = (byte)(128 | kod_znaku >> 6 & 63); 임시[쓴수++] = (byte)(128 | kod_znaku & 63); }
            else { 임시[쓴수++] = (byte)(240 | kod_znaku >> 18); 임시[쓴수++] = (byte)(128 | kod_znaku >> 12 & 63); 임시[쓴수++] = (byte)(128 | kod_znaku >> 6 & 63); 임시[쓴수++] = (byte)(128 | kod_znaku & 63); }
        }
        byte[] WYNIK = new byte[쓴수]; System.arraycopy(임시, 0, WYNIK, 0, 쓴수); return WYNIK;
    }
    /** 잘못된 UTF-8은 잘못된인수예외으로 거부한다. */
    public static String odszyfrować_dane(byte[] bajt_WARTOŚĆ) {
        StringBuilder WYNIK = new StringBuilder();
        for (int Loop_INDEKS = 0; Loop_INDEKS < bajt_WARTOŚĆ.length;) {
            int kod_znaku = bajt_WARTOŚĆ[Loop_INDEKS++] & 255, identyfikator = kod_znaku < 128 ? 0 : kod_znaku >= 194 && kod_znaku < 224 ? 1 : kod_znaku >= 224 && kod_znaku < 240 ? 2 : kod_znaku >= 240 && kod_znaku <= 244 ? 3 : -1;
            if (identyfikator < 0 || bajt_WARTOŚĆ.length - Loop_INDEKS < identyfikator) throw new nieważny_argument_wyjątek("잘못된 UTF-8");
            int 최소 = identyfikator == 1 ? 128 : identyfikator == 2 ? 2048 : identyfikator == 3 ? 65536 : 0;
            if (identyfikator > 0) kod_znaku &= (1 << (6 - identyfikator)) - 1;
            for (int wewnętrzne_stanowisko = 0; wewnętrzne_stanowisko < identyfikator; wewnętrzne_stanowisko++) { int BACK_WARTOŚĆ = bajt_WARTOŚĆ[Loop_INDEKS++] & 255; if ((BACK_WARTOŚĆ & 192) != 128) throw new nieważny_argument_wyjątek("잘못된 UTF-8"); kod_znaku = kod_znaku << 6 | BACK_WARTOŚĆ & 63; }
            if (kod_znaku < 최소 || kod_znaku > 0x10ffff || kod_znaku >= 0xd800 && kod_znaku <= 0xdfff) throw new nieważny_argument_wyjątek("잘못된 UTF-8");
            if (kod_znaku < 65536) WYNIK.append((char)kod_znaku);
            else { kod_znaku -= 65536; WYNIK.append((char)(0xd800 | kod_znaku >> 10)); WYNIK.append((char)(0xdc00 | kod_znaku & 1023)); }
        }
        return WYNIK.toString();
    }
}
