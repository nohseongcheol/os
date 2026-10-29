// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트 Alati 공통 Izlaz 및 ASCII Datoteka Ime Proces_VALUE_unos. */
public final class 자바도구 {
    /** UTF-8 bajt_VALUE 배열을 같은 배열의 UTF-16 단위로 바꾼다. 잘못된 입력은 odbiti_VALUE. */
    static int 원문해독(int[] podaci, int 길이) {
        int Čitaj = 0, Zapisuj = 0;
        if (길이 >= 3 && podaci[0] == 239 && podaci[1] == 187 && podaci[2] == 191) Čitaj = 3;
        while (Čitaj < 길이) {
            int VALUE = podaci[Čitaj++], 수 = 0, 최소 = 0;
            if (VALUE >= 194 && VALUE <= 223) { 수 = 1; 최소 = 128; VALUE &= 31; }
            else if (VALUE >= 224 && VALUE <= 239) { 수 = 2; 최소 = 2048; VALUE &= 15; }
            else if (VALUE >= 240 && VALUE <= 244) { 수 = 3; 최소 = 65536; VALUE &= 7; }
            else if (VALUE >= 128 || VALUE < 0) return -1;
            if (수 > 길이 - Čitaj) return -1;
            for (int i = 0; i < 수; i++) {
                int Dalje_artikl = podaci[Čitaj++]; if ((Dalje_artikl & 192) != 128) return -1;
                VALUE = (VALUE << 6) | (Dalje_artikl & 63);
            }
            if (VALUE < 최소 || VALUE > 0x10ffff || (VALUE >= 0xd800 && VALUE <= 0xdfff)) return -1;
            if (VALUE >= 65536) { VALUE -= 65536; podaci[Zapisuj++] = 0xd800 | (VALUE >> 10); podaci[Zapisuj++] = 0xdc00 | (VALUE & 1023); }
            else podaci[Zapisuj++] = VALUE;
        }
        return Zapisuj;
    }
    static void 수쓰기(int VALUE) {
        if (VALUE < 0) korisnik.zapisivanje_znak_VALUE('-'); else VALUE = -VALUE;
        int indeks_položaja = 1000000000;
        boolean Pokreni = false;
        while (indeks_položaja != 0) {
            int 수 = -(VALUE / indeks_položaja);
            if (수 != 0 || Pokreni || indeks_položaja == 1) { korisnik.zapisivanje_znak_VALUE('0' + 수); Pokreni = true; }
            VALUE %= indeks_položaja; indeks_položaja /= 10;
        }
    }
    static int Ime(int[] odredište_VALUE, String 원본) {
        if (원본.length() >= odredište_VALUE.length) return -1;
        for (int 수 = 0; 수 < odredište_VALUE.length; 수++) odredište_VALUE[수] = 수 < 원본.length() ? 원본.charAt(수) : 0;
        return 원본.length();
    }
    static boolean 같음(String 가, String SECOND_operand) {
        if (가.length() != SECOND_operand.length()) return false;
        for (int 수 = 0; 수 < 가.length(); 수++) if (가.charAt(수) != SECOND_operand.charAt(수)) return false;
        return true;
    }
}
