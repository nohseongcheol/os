// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 narzędzia 공통 pozycja_wyjścia 및 ASCII nazwa_pliku Nazwa Proces_WARTOŚĆ_wpis. */
public final class 자바도구 {
    /** UTF-8 bajt_WARTOŚĆ 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 odrzucić_WARTOŚĆ. */
    static int 원문해독(int[] dane, int długość_WARTOŚĆ) {
        int Odczyt = 0, Zapis = 0;
        if (długość_WARTOŚĆ >= 3 && dane[0] == 239 && dane[1] == 187 && dane[2] == 191) Odczyt = 3;
        while (Odczyt < długość_WARTOŚĆ) {
            int WARTOŚĆ = dane[Odczyt++], identyfikator = 0, 최소 = 0;
            if (WARTOŚĆ >= 194 && WARTOŚĆ <= 223) { identyfikator = 1; 최소 = 128; WARTOŚĆ &= 31; }
            else if (WARTOŚĆ >= 224 && WARTOŚĆ <= 239) { identyfikator = 2; 최소 = 2048; WARTOŚĆ &= 15; }
            else if (WARTOŚĆ >= 240 && WARTOŚĆ <= 244) { identyfikator = 3; 최소 = 65536; WARTOŚĆ &= 7; }
            else if (WARTOŚĆ >= 128 || WARTOŚĆ < 0) return -1;
            if (identyfikator > długość_WARTOŚĆ - Odczyt) return -1;
            for (int i = 0; i < identyfikator; i++) {
                int Dalej_towar = dane[Odczyt++]; if ((Dalej_towar & 192) != 128) return -1;
                WARTOŚĆ = (WARTOŚĆ << 6) | (Dalej_towar & 63);
            }
            if (WARTOŚĆ < 최소 || WARTOŚĆ > 0x10ffff || (WARTOŚĆ >= 0xd800 && WARTOŚĆ <= 0xdfff)) return -1;
            if (WARTOŚĆ >= 65536) { WARTOŚĆ -= 65536; dane[Zapis++] = 0xd800 | (WARTOŚĆ >> 10); dane[Zapis++] = 0xdc00 | (WARTOŚĆ & 1023); }
            else dane[Zapis++] = WARTOŚĆ;
        }
        return Zapis;
    }
    static void zapis_identyfikator(int WARTOŚĆ) {
        if (WARTOŚĆ < 0) przestrzeń_użytkownika.zapis_znak_WARTOŚĆ('-'); else WARTOŚĆ = -WARTOŚĆ;
        int indeks_pozycji = 1000000000;
        boolean Uruchom_2 = false;
        while (indeks_pozycji != 0) {
            int identyfikator = -(WARTOŚĆ / indeks_pozycji);
            if (identyfikator != 0 || Uruchom_2 || indeks_pozycji == 1) { przestrzeń_użytkownika.zapis_znak_WARTOŚĆ('0' + identyfikator); Uruchom_2 = true; }
            WARTOŚĆ %= indeks_pozycji; indeks_pozycji /= 10;
        }
    }
    static int Nazwa(int[] cel_WARTOŚĆ, String 원본) {
        if (원본.length() >= cel_WARTOŚĆ.length) return -1;
        for (int identyfikator = 0; identyfikator < cel_WARTOŚĆ.length; identyfikator++) cel_WARTOŚĆ[identyfikator] = identyfikator < 원본.length() ? 원본.charAt(identyfikator) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SEKUNDA_operand) {
        if (가.length() != SEKUNDA_operand.length()) return false;
        for (int identyfikator = 0; identyfikator < 가.length(); identyfikator++) if (가.charAt(identyfikator) != SEKUNDA_operand.charAt(identyfikator)) return false;
        return true;
    }
}
