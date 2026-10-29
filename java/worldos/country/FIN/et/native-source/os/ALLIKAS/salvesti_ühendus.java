// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 jaotis_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class salvesti_ühendus {
    static boolean infotehnoloogia_Aktiivne_9e72441a = false;
    static int[] jaotis_andmed = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) seade_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Käivita_2 = seade_VALUE.밀리초();
        while (seade_VALUE.밀리초() - Käivita_2 < 500) {
            int Olek_VALUE = seade_VALUE.입출력바이트읽기(0x1f7);
            if (Olek_VALUE == 0 || Olek_VALUE == 255) return -19;
            if ((Olek_VALUE & 128) == 0) {
                if ((Olek_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Olek_VALUE & 8) != 0) return 0;
            }
            seade_VALUE.잠시양보();
        }
        return -110;
    }
    static int päring(int jaotis_VALUE, int Käsk) {
        if (jaotis_VALUE < 0 || jaotis_VALUE >= 2048) return -22;
        seade_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ kasutus_VALUE 안 함
        seade_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int TULEMUS = 준비기다리기(false);
        if (TULEMUS < 0) return TULEMUS;
        seade_VALUE.입출력바이트쓰기(0x1f2, 1);
        seade_VALUE.입출력바이트쓰기(0x1f3, jaotis_VALUE & 255);
        seade_VALUE.입출력바이트쓰기(0x1f4, (jaotis_VALUE >>> 8) & 255);
        seade_VALUE.입출력바이트쓰기(0x1f5, 0);
        seade_VALUE.입출력바이트쓰기(0x1f7, Käsk); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lugemine(int jaotis_VALUE) {
        int TULEMUS = päring(jaotis_VALUE, 0x20);
        if (TULEMUS < 0) return TULEMUS;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = seade_VALUE.입출력짧은수읽기(0x1f0);
            jaotis_andmed[INDEX * 2] = VALUE & 255; jaotis_andmed[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Kirjutamine(int jaotis_VALUE) {
        if (!infotehnoloogia_Aktiivne_9e72441a || jaotis_VALUE < 1 || jaotis_VALUE > 518) return -19;
        int TULEMUS = päring(jaotis_VALUE, 0x30);
        if (TULEMUS < 0) return TULEMUS;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            seade_VALUE.입출력짧은수쓰기(0x1f0, jaotis_andmed[INDEX * 2] | jaotis_andmed[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!infotehnoloogia_Aktiivne_9e72441a) return -19;
        seade_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int sõeluma_täisarv(int Asukoht) {
        return jaotis_andmed[Asukoht] | jaotis_andmed[Asukoht + 1] << 8 | jaotis_andmed[Asukoht + 2] << 16 | jaotis_andmed[Asukoht + 3] << 24;
    }
    static void kirjutamine_täisarv_VALUE(int Asukoht, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) jaotis_andmed[Asukoht + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
