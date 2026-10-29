// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 oddíl_HODNOTA_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class úložiště_kontakt {
    static boolean informační_systémy_online = false;
    static int[] oddíl_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobilní_HODNOTA.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Spustit_2 = mobilní_HODNOTA.밀리초();
        while (mobilní_HODNOTA.밀리초() - Spustit_2 < 500) {
            int Stav_HODNOTA = mobilní_HODNOTA.입출력바이트읽기(0x1f7);
            if (Stav_HODNOTA == 0 || Stav_HODNOTA == 255) return -19;
            if ((Stav_HODNOTA & 128) == 0) {
                if ((Stav_HODNOTA & 33) != 0) return -5;
                if (!자료필요 || (Stav_HODNOTA & 8) != 0) return 0;
            }
            mobilní_HODNOTA.잠시양보();
        }
        return -110;
    }
    static int žádost(int oddíl_HODNOTA_366e0bfa, int příkaz) {
        if (oddíl_HODNOTA_366e0bfa < 0 || oddíl_HODNOTA_366e0bfa >= 2048) return -22;
        mobilní_HODNOTA.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ použít_HODNOTA 안 함
        mobilní_HODNOTA.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int VÝSLEDEK = 준비기다리기(false);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        mobilní_HODNOTA.입출력바이트쓰기(0x1f2, 1);
        mobilní_HODNOTA.입출력바이트쓰기(0x1f3, oddíl_HODNOTA_366e0bfa & 255);
        mobilní_HODNOTA.입출력바이트쓰기(0x1f4, (oddíl_HODNOTA_366e0bfa >>> 8) & 255);
        mobilní_HODNOTA.입출력바이트쓰기(0x1f5, 0);
        mobilní_HODNOTA.입출력바이트쓰기(0x1f7, příkaz); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Čtení(int oddíl_HODNOTA_366e0bfa) {
        int VÝSLEDEK = žádost(oddíl_HODNOTA_366e0bfa, 0x20);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int HODNOTA = mobilní_HODNOTA.입출력짧은수읽기(0x1f0);
            oddíl_data[INDEX * 2] = HODNOTA & 255; oddíl_data[INDEX * 2 + 1] = HODNOTA >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Zápis(int oddíl_HODNOTA_366e0bfa) {
        if (!informační_systémy_online || oddíl_HODNOTA_366e0bfa < 1 || oddíl_HODNOTA_366e0bfa > 518) return -19;
        int VÝSLEDEK = žádost(oddíl_HODNOTA_366e0bfa, 0x30);
        if (VÝSLEDEK < 0) return VÝSLEDEK;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mobilní_HODNOTA.입출력짧은수쓰기(0x1f0, oddíl_data[INDEX * 2] | oddíl_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int vyprázdnit_výstup() {
        if (!informační_systémy_online) return -19;
        mobilní_HODNOTA.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int parsovat_integer(int pozice) {
        return oddíl_data[pozice] | oddíl_data[pozice + 1] << 8 | oddíl_data[pozice + 2] << 16 | oddíl_data[pozice + 3] << 24;
    }
    static void zápis_integer_HODNOTA(int pozice, int HODNOTA) {
        for (int INDEX = 0; INDEX < 4; INDEX++) oddíl_data[pozice + INDEX] = (HODNOTA >>> (INDEX * 8)) & 255;
    }
}
