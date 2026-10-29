// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 osa_ARVO. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class tallennuslaite_yhteys {
    static boolean tietojärjestelmät_Aktiivinen_9e72441a = false;
    static int[] osa_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) laite_ARVO.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Suorita_2 = laite_ARVO.밀리초();
        while (laite_ARVO.밀리초() - Suorita_2 < 500) {
            int Tila_ARVO = laite_ARVO.입출력바이트읽기(0x1f7);
            if (Tila_ARVO == 0 || Tila_ARVO == 255) return -19;
            if ((Tila_ARVO & 128) == 0) {
                if ((Tila_ARVO & 33) != 0) return -5;
                if (!자료필요 || (Tila_ARVO & 8) != 0) return 0;
            }
            laite_ARVO.잠시양보();
        }
        return -110;
    }
    static int pyyntö(int osa_ARVO, int komento) {
        if (osa_ARVO < 0 || osa_ARVO >= 2048) return -22;
        laite_ARVO.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ käyttö_ARVO 안 함
        laite_ARVO.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int TULOS = 준비기다리기(false);
        if (TULOS < 0) return TULOS;
        laite_ARVO.입출력바이트쓰기(0x1f2, 1);
        laite_ARVO.입출력바이트쓰기(0x1f3, osa_ARVO & 255);
        laite_ARVO.입출력바이트쓰기(0x1f4, (osa_ARVO >>> 8) & 255);
        laite_ARVO.입출력바이트쓰기(0x1f5, 0);
        laite_ARVO.입출력바이트쓰기(0x1f7, komento); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Luku(int osa_ARVO) {
        int TULOS = pyyntö(osa_ARVO, 0x20);
        if (TULOS < 0) return TULOS;
        for (int INDEKSI = 0; INDEKSI < 256; INDEKSI++) {
            int ARVO = laite_ARVO.입출력짧은수읽기(0x1f0);
            osa_data[INDEKSI * 2] = ARVO & 255; osa_data[INDEKSI * 2 + 1] = ARVO >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Kirjoitus(int osa_ARVO) {
        if (!tietojärjestelmät_Aktiivinen_9e72441a || osa_ARVO < 1 || osa_ARVO > 518) return -19;
        int TULOS = pyyntö(osa_ARVO, 0x30);
        if (TULOS < 0) return TULOS;
        for (int INDEKSI = 0; INDEKSI < 256; INDEKSI++)
            laite_ARVO.입출력짧은수쓰기(0x1f0, osa_data[INDEKSI * 2] | osa_data[INDEKSI * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!tietojärjestelmät_Aktiivinen_9e72441a) return -19;
        laite_ARVO.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int jäsentää_kokonaisluku(int paikka) {
        return osa_data[paikka] | osa_data[paikka + 1] << 8 | osa_data[paikka + 2] << 16 | osa_data[paikka + 3] << 24;
    }
    static void kirjoitus_kokonaisluku_ARVO(int paikka, int ARVO) {
        for (int INDEKSI = 0; INDEKSI < 4; INDEKSI++) osa_data[paikka + INDEKSI] = (ARVO >>> (INDEKSI * 8)) & 255;
    }
}
