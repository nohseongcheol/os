// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 hluti_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class geymsla_tæki_tenging {
    static boolean upplýsingatækni_Laus_9e72441a = false;
    static int[] hluti_gögn = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) tæki_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Keyra_2 = tæki_VALUE.밀리초();
        while (tæki_VALUE.밀리초() - Keyra_2 < 500) {
            int staða_VALUE_e10195a1 = tæki_VALUE.입출력바이트읽기(0x1f7);
            if (staða_VALUE_e10195a1 == 0 || staða_VALUE_e10195a1 == 255) return -19;
            if ((staða_VALUE_e10195a1 & 128) == 0) {
                if ((staða_VALUE_e10195a1 & 33) != 0) return -5;
                if (!자료필요 || (staða_VALUE_e10195a1 & 8) != 0) return 0;
            }
            tæki_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int hluti_VALUE, int Skipun) {
        if (hluti_VALUE < 0 || hluti_VALUE >= 2048) return -22;
        tæki_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        tæki_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int NIÐURSTAÐA = 준비기다리기(false);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        tæki_VALUE.입출력바이트쓰기(0x1f2, 1);
        tæki_VALUE.입출력바이트쓰기(0x1f3, hluti_VALUE & 255);
        tæki_VALUE.입출력바이트쓰기(0x1f4, (hluti_VALUE >>> 8) & 255);
        tæki_VALUE.입출력바이트쓰기(0x1f5, 0);
        tæki_VALUE.입출력바이트쓰기(0x1f7, Skipun); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lestur(int hluti_VALUE) {
        int NIÐURSTAÐA = 요청(hluti_VALUE, 0x20);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = tæki_VALUE.입출력짧은수읽기(0x1f0);
            hluti_gögn[INDEX * 2] = VALUE & 255; hluti_gögn[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Skrift(int hluti_VALUE) {
        if (!upplýsingatækni_Laus_9e72441a || hluti_VALUE < 1 || hluti_VALUE > 518) return -19;
        int NIÐURSTAÐA = 요청(hluti_VALUE, 0x30);
        if (NIÐURSTAÐA < 0) return NIÐURSTAÐA;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            tæki_VALUE.입출력짧은수쓰기(0x1f0, hluti_gögn[INDEX * 2] | hluti_gögn[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!upplýsingatækni_Laus_9e72441a) return -19;
        tæki_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int þátta_heiltala(int Staðsetning) {
        return hluti_gögn[Staðsetning] | hluti_gögn[Staðsetning + 1] << 8 | hluti_gögn[Staðsetning + 2] << 16 | hluti_gögn[Staðsetning + 3] << 24;
    }
    static void skrifa_heiltala_VALUE(int Staðsetning, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) hluti_gögn[Staðsetning + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
