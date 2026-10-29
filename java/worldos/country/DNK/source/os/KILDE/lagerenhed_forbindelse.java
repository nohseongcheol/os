// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sektion_VÆRDI. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class lagerenhed_forbindelse {
    static boolean it_Aktiv_9e72441a = false;
    static int[] sektion_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) enhed_VÆRDI.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Kør_2 = enhed_VÆRDI.밀리초();
        while (enhed_VÆRDI.밀리초() - Kør_2 < 500) {
            int status_VÆRDI = enhed_VÆRDI.입출력바이트읽기(0x1f7);
            if (status_VÆRDI == 0 || status_VÆRDI == 255) return -19;
            if ((status_VÆRDI & 128) == 0) {
                if ((status_VÆRDI & 33) != 0) return -5;
                if (!자료필요 || (status_VÆRDI & 8) != 0) return 0;
            }
            enhed_VÆRDI.잠시양보();
        }
        return -110;
    }
    static int anmodning(int sektion_VÆRDI, int Kommando) {
        if (sektion_VÆRDI < 0 || sektion_VÆRDI >= 2048) return -22;
        enhed_VÆRDI.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ brug_VÆRDI 안 함
        enhed_VÆRDI.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int KR = 준비기다리기(false);
        if (KR < 0) return KR;
        enhed_VÆRDI.입출력바이트쓰기(0x1f2, 1);
        enhed_VÆRDI.입출력바이트쓰기(0x1f3, sektion_VÆRDI & 255);
        enhed_VÆRDI.입출력바이트쓰기(0x1f4, (sektion_VÆRDI >>> 8) & 255);
        enhed_VÆRDI.입출력바이트쓰기(0x1f5, 0);
        enhed_VÆRDI.입출력바이트쓰기(0x1f7, Kommando); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Læse(int sektion_VÆRDI) {
        int KR = anmodning(sektion_VÆRDI, 0x20);
        if (KR < 0) return KR;
        for (int INDEKS = 0; INDEKS < 256; INDEKS++) {
            int VÆRDI = enhed_VÆRDI.입출력짧은수읽기(0x1f0);
            sektion_data[INDEKS * 2] = VÆRDI & 255; sektion_data[INDEKS * 2 + 1] = VÆRDI >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Skrive(int sektion_VÆRDI) {
        if (!it_Aktiv_9e72441a || sektion_VÆRDI < 1 || sektion_VÆRDI > 518) return -19;
        int KR = anmodning(sektion_VÆRDI, 0x30);
        if (KR < 0) return KR;
        for (int INDEKS = 0; INDEKS < 256; INDEKS++)
            enhed_VÆRDI.입출력짧은수쓰기(0x1f0, sektion_data[INDEKS * 2] | sektion_data[INDEKS * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!it_Aktiv_9e72441a) return -19;
        enhed_VÆRDI.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int opdele_tekst_heltal(int Placering) {
        return sektion_data[Placering] | sektion_data[Placering + 1] << 8 | sektion_data[Placering + 2] << 16 | sektion_data[Placering + 3] << 24;
    }
    static void skrive_heltal_VÆRDI(int Placering, int VÆRDI) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) sektion_data[Placering + INDEKS] = (VÆRDI >>> (INDEKS * 8)) & 255;
    }
}
