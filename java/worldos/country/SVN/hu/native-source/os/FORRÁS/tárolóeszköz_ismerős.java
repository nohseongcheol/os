// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 szakasz_ÉRTÉK. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class tárolóeszköz_ismerős {
    static boolean informatikai_részleg_Aktív_9e72441a = false;
    static int[] szakasz_adat = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_ÉRTÉK.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Futtatás = mobil_ÉRTÉK.밀리초();
        while (mobil_ÉRTÉK.밀리초() - Futtatás < 500) {
            int Állapot_ÉRTÉK = mobil_ÉRTÉK.입출력바이트읽기(0x1f7);
            if (Állapot_ÉRTÉK == 0 || Állapot_ÉRTÉK == 255) return -19;
            if ((Állapot_ÉRTÉK & 128) == 0) {
                if ((Állapot_ÉRTÉK & 33) != 0) return -5;
                if (!자료필요 || (Állapot_ÉRTÉK & 8) != 0) return 0;
            }
            mobil_ÉRTÉK.잠시양보();
        }
        return -110;
    }
    static int kérés(int szakasz_ÉRTÉK, int Parancs) {
        if (szakasz_ÉRTÉK < 0 || szakasz_ÉRTÉK >= 2048) return -22;
        mobil_ÉRTÉK.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ használ_ÉRTÉK 안 함
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int KR = 준비기다리기(false);
        if (KR < 0) return KR;
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f2, 1);
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f3, szakasz_ÉRTÉK & 255);
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f4, (szakasz_ÉRTÉK >>> 8) & 255);
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f5, 0);
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f7, Parancs); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Olvasás(int szakasz_ÉRTÉK) {
        int KR = kérés(szakasz_ÉRTÉK, 0x20);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int ÉRTÉK = mobil_ÉRTÉK.입출력짧은수읽기(0x1f0);
            szakasz_adat[INDEX * 2] = ÉRTÉK & 255; szakasz_adat[INDEX * 2 + 1] = ÉRTÉK >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Írás(int szakasz_ÉRTÉK) {
        if (!informatikai_részleg_Aktív_9e72441a || szakasz_ÉRTÉK < 1 || szakasz_ÉRTÉK > 518) return -19;
        int KR = kérés(szakasz_ÉRTÉK, 0x30);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mobil_ÉRTÉK.입출력짧은수쓰기(0x1f0, szakasz_adat[INDEX * 2] | szakasz_adat[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informatikai_részleg_Aktív_9e72441a) return -19;
        mobil_ÉRTÉK.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int elemez_egész_szám(int Pozíció) {
        return szakasz_adat[Pozíció] | szakasz_adat[Pozíció + 1] << 8 | szakasz_adat[Pozíció + 2] << 16 | szakasz_adat[Pozíció + 3] << 24;
    }
    static void ír_egész_szám_ÉRTÉK(int Pozíció, int ÉRTÉK) {
        for (int INDEX = 0; INDEX < 4; INDEX++) szakasz_adat[Pozíció + INDEX] = (ÉRTÉK >>> (INDEX * 8)) & 255;
    }
}
