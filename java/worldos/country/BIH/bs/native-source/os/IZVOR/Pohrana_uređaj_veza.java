// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sekcija_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Pohrana_uređaj_veza {
    static boolean odjel_za_informacijske_tehnologije_dostupan = false;
    static int[] sekcija_podaci = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Pokreni = uređaj_VALUE.밀리초();
        while (uređaj_VALUE.밀리초() - Pokreni < 500) {
            int stanje_VALUE = uređaj_VALUE.입출력바이트읽기(0x1f7);
            if (stanje_VALUE == 0 || stanje_VALUE == 255) return -19;
            if ((stanje_VALUE & 128) == 0) {
                if ((stanje_VALUE & 33) != 0) return -5;
                if (!자료필요 || (stanje_VALUE & 8) != 0) return 0;
            }
            uređaj_VALUE.잠시양보();
        }
        return -110;
    }
    static int HTTP_zahtjev(int sekcija_VALUE, int Naredba) {
        if (sekcija_VALUE < 0 || sekcija_VALUE >= 2048) return -22;
        uređaj_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        uređaj_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int mjera = 준비기다리기(false);
        if (mjera < 0) return mjera;
        uređaj_VALUE.입출력바이트쓰기(0x1f2, 1);
        uređaj_VALUE.입출력바이트쓰기(0x1f3, sekcija_VALUE & 255);
        uređaj_VALUE.입출력바이트쓰기(0x1f4, (sekcija_VALUE >>> 8) & 255);
        uređaj_VALUE.입출력바이트쓰기(0x1f5, 0);
        uređaj_VALUE.입출력바이트쓰기(0x1f7, Naredba); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Čitaj(int sekcija_VALUE) {
        int mjera = HTTP_zahtjev(sekcija_VALUE, 0x20);
        if (mjera < 0) return mjera;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = uređaj_VALUE.입출력짧은수읽기(0x1f0);
            sekcija_podaci[INDEX * 2] = VALUE & 255; sekcija_podaci[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Piši(int sekcija_VALUE) {
        if (!odjel_za_informacijske_tehnologije_dostupan || sekcija_VALUE < 1 || sekcija_VALUE > 518) return -19;
        int mjera = HTTP_zahtjev(sekcija_VALUE, 0x30);
        if (mjera < 0) return mjera;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            uređaj_VALUE.입출력짧은수쓰기(0x1f0, sekcija_podaci[INDEX * 2] | sekcija_podaci[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!odjel_za_informacijske_tehnologije_dostupan) return -19;
        uređaj_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int raščlanjivati_cijeli_broj(int Pozicija) {
        return sekcija_podaci[Pozicija] | sekcija_podaci[Pozicija + 1] << 8 | sekcija_podaci[Pozicija + 2] << 16 | sekcija_podaci[Pozicija + 3] << 24;
    }
    static void pisati_cijeli_broj_VALUE(int Pozicija, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) sekcija_podaci[Pozicija + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
