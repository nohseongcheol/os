// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 odsek_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class naprava_za_shranjevanje_povezava {
    static boolean informacijska_tehnologija_Dejaven_9e72441a = false;
    static int[] odsek_podatki = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) naprava_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Zaženi = naprava_VALUE.밀리초();
        while (naprava_VALUE.밀리초() - Zaženi < 500) {
            int stanje_VALUE = naprava_VALUE.입출력바이트읽기(0x1f7);
            if (stanje_VALUE == 0 || stanje_VALUE == 255) return -19;
            if ((stanje_VALUE & 128) == 0) {
                if ((stanje_VALUE & 33) != 0) return -5;
                if (!자료필요 || (stanje_VALUE & 8) != 0) return 0;
            }
            naprava_VALUE.잠시양보();
        }
        return -110;
    }
    static int zahteva(int odsek_VALUE, int Ukaz) {
        if (odsek_VALUE < 0 || odsek_VALUE >= 2048) return -22;
        naprava_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ uporaba_VALUE 안 함
        naprava_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int REZULTAT = 준비기다리기(false);
        if (REZULTAT < 0) return REZULTAT;
        naprava_VALUE.입출력바이트쓰기(0x1f2, 1);
        naprava_VALUE.입출력바이트쓰기(0x1f3, odsek_VALUE & 255);
        naprava_VALUE.입출력바이트쓰기(0x1f4, (odsek_VALUE >>> 8) & 255);
        naprava_VALUE.입출력바이트쓰기(0x1f5, 0);
        naprava_VALUE.입출력바이트쓰기(0x1f7, Ukaz); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Branje(int odsek_VALUE) {
        int REZULTAT = zahteva(odsek_VALUE, 0x20);
        if (REZULTAT < 0) return REZULTAT;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = naprava_VALUE.입출력짧은수읽기(0x1f0);
            odsek_podatki[INDEX * 2] = VALUE & 255; odsek_podatki[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Pisanje(int odsek_VALUE) {
        if (!informacijska_tehnologija_Dejaven_9e72441a || odsek_VALUE < 1 || odsek_VALUE > 518) return -19;
        int REZULTAT = zahteva(odsek_VALUE, 0x30);
        if (REZULTAT < 0) return REZULTAT;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            naprava_VALUE.입출력짧은수쓰기(0x1f0, odsek_podatki[INDEX * 2] | odsek_podatki[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informacijska_tehnologija_Dejaven_9e72441a) return -19;
        naprava_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int razčlenjevati_celo_število(int Položaj) {
        return odsek_podatki[Položaj] | odsek_podatki[Položaj + 1] << 8 | odsek_podatki[Položaj + 2] << 16 | odsek_podatki[Položaj + 3] << 24;
    }
    static void pisati_celo_število_VALUE(int Položaj, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) odsek_podatki[Položaj + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
