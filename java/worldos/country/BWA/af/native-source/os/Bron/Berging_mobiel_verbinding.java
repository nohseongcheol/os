// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 seksie_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Berging_mobiel_verbinding {
    static boolean 사용가능 = false;
    static int[] seksie_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobiel_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Loop = mobiel_VALUE.밀리초();
        while (mobiel_VALUE.밀리초() - Loop < 500) {
            int stand_VALUE = mobiel_VALUE.입출력바이트읽기(0x1f7);
            if (stand_VALUE == 0 || stand_VALUE == 255) return -19;
            if ((stand_VALUE & 128) == 0) {
                if ((stand_VALUE & 33) != 0) return -5;
                if (!자료필요 || (stand_VALUE & 8) != 0) return 0;
            }
            mobiel_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int seksie_VALUE, int Opdrag) {
        if (seksie_VALUE < 0 || seksie_VALUE >= 2048) return -22;
        mobiel_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        mobiel_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int maatreël = 준비기다리기(false);
        if (maatreël < 0) return maatreël;
        mobiel_VALUE.입출력바이트쓰기(0x1f2, 1);
        mobiel_VALUE.입출력바이트쓰기(0x1f3, seksie_VALUE & 255);
        mobiel_VALUE.입출력바이트쓰기(0x1f4, (seksie_VALUE >>> 8) & 255);
        mobiel_VALUE.입출력바이트쓰기(0x1f5, 0);
        mobiel_VALUE.입출력바이트쓰기(0x1f7, Opdrag); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lees(int seksie_VALUE) {
        int maatreël = 요청(seksie_VALUE, 0x20);
        if (maatreël < 0) return maatreël;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = mobiel_VALUE.입출력짧은수읽기(0x1f0);
            seksie_data[INDEX * 2] = VALUE & 255; seksie_data[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Skryf(int seksie_VALUE) {
        if (!사용가능 || seksie_VALUE < 1 || seksie_VALUE > 518) return -19;
        int maatreël = 요청(seksie_VALUE, 0x30);
        if (maatreël < 0) return maatreël;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mobiel_VALUE.입출력짧은수쓰기(0x1f0, seksie_data[INDEX * 2] | seksie_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        mobiel_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int ontleed_heelgetal(int Posisie) {
        return seksie_data[Posisie] | seksie_data[Posisie + 1] << 8 | seksie_data[Posisie + 2] << 16 | seksie_data[Posisie + 3] << 24;
    }
    static void skryf_heelgetal_VALUE(int Posisie, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) seksie_data[Posisie + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
