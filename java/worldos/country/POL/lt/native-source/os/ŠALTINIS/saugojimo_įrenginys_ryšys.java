// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sekcija_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class saugojimo_įrenginys_ryšys {
    static boolean informacinės_technologijos_Aktyvus_9e72441a = false;
    static int[] sekcija_duomenys = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) įrenginys_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Paleisti = įrenginys_VALUE.밀리초();
        while (įrenginys_VALUE.밀리초() - Paleisti < 500) {
            int Būsena_VALUE = įrenginys_VALUE.입출력바이트읽기(0x1f7);
            if (Būsena_VALUE == 0 || Būsena_VALUE == 255) return -19;
            if ((Būsena_VALUE & 128) == 0) {
                if ((Būsena_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Būsena_VALUE & 8) != 0) return 0;
            }
            įrenginys_VALUE.잠시양보();
        }
        return -110;
    }
    static int užklausa(int sekcija_VALUE, int Komanda) {
        if (sekcija_VALUE < 0 || sekcija_VALUE >= 2048) return -22;
        įrenginys_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ naudoti_VALUE 안 함
        įrenginys_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int REZULTATAS = 준비기다리기(false);
        if (REZULTATAS < 0) return REZULTATAS;
        įrenginys_VALUE.입출력바이트쓰기(0x1f2, 1);
        įrenginys_VALUE.입출력바이트쓰기(0x1f3, sekcija_VALUE & 255);
        įrenginys_VALUE.입출력바이트쓰기(0x1f4, (sekcija_VALUE >>> 8) & 255);
        įrenginys_VALUE.입출력바이트쓰기(0x1f5, 0);
        įrenginys_VALUE.입출력바이트쓰기(0x1f7, Komanda); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Skaitymas(int sekcija_VALUE) {
        int REZULTATAS = užklausa(sekcija_VALUE, 0x20);
        if (REZULTATAS < 0) return REZULTATAS;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = įrenginys_VALUE.입출력짧은수읽기(0x1f0);
            sekcija_duomenys[INDEX * 2] = VALUE & 255; sekcija_duomenys[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Rašymas(int sekcija_VALUE) {
        if (!informacinės_technologijos_Aktyvus_9e72441a || sekcija_VALUE < 1 || sekcija_VALUE > 518) return -19;
        int REZULTATAS = užklausa(sekcija_VALUE, 0x30);
        if (REZULTATAS < 0) return REZULTATAS;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            įrenginys_VALUE.입출력짧은수쓰기(0x1f0, sekcija_duomenys[INDEX * 2] | sekcija_duomenys[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informacinės_technologijos_Aktyvus_9e72441a) return -19;
        įrenginys_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizuoti_sintaksę_sveikasis_skaičius(int Pozicija) {
        return sekcija_duomenys[Pozicija] | sekcija_duomenys[Pozicija + 1] << 8 | sekcija_duomenys[Pozicija + 2] << 16 | sekcija_duomenys[Pozicija + 3] << 24;
    }
    static void rašymas_sveikasis_skaičius_VALUE(int Pozicija, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) sekcija_duomenys[Pozicija + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
