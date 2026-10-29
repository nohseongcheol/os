// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 rannán_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Stóras_gléas_nasc {
    static boolean teicneolaíocht_faisnéise_ar_fáil = false;
    static int[] rannán_sonraí = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) gléas_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Rith_2 = gléas_VALUE.밀리초();
        while (gléas_VALUE.밀리초() - Rith_2 < 500) {
            int staid_VALUE = gléas_VALUE.입출력바이트읽기(0x1f7);
            if (staid_VALUE == 0 || staid_VALUE == 255) return -19;
            if ((staid_VALUE & 128) == 0) {
                if ((staid_VALUE & 33) != 0) return -5;
                if (!자료필요 || (staid_VALUE & 8) != 0) return 0;
            }
            gléas_VALUE.잠시양보();
        }
        return -110;
    }
    static int iarratas_HTTP(int rannán_VALUE, int Ordú) {
        if (rannán_VALUE < 0 || rannán_VALUE >= 2048) return -22;
        gléas_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        gléas_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int tomhas = 준비기다리기(false);
        if (tomhas < 0) return tomhas;
        gléas_VALUE.입출력바이트쓰기(0x1f2, 1);
        gléas_VALUE.입출력바이트쓰기(0x1f3, rannán_VALUE & 255);
        gléas_VALUE.입출력바이트쓰기(0x1f4, (rannán_VALUE >>> 8) & 255);
        gléas_VALUE.입출력바이트쓰기(0x1f5, 0);
        gléas_VALUE.입출력바이트쓰기(0x1f7, Ordú); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Léigh(int rannán_VALUE) {
        int tomhas = iarratas_HTTP(rannán_VALUE, 0x20);
        if (tomhas < 0) return tomhas;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = gléas_VALUE.입출력짧은수읽기(0x1f0);
            rannán_sonraí[INDEX * 2] = VALUE & 255; rannán_sonraí[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Scríobh(int rannán_VALUE) {
        if (!teicneolaíocht_faisnéise_ar_fáil || rannán_VALUE < 1 || rannán_VALUE > 518) return -19;
        int tomhas = iarratas_HTTP(rannán_VALUE, 0x30);
        if (tomhas < 0) return tomhas;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            gléas_VALUE.입출력짧은수쓰기(0x1f0, rannán_sonraí[INDEX * 2] | rannán_sonraí[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!teicneolaíocht_faisnéise_ar_fáil) return -19;
        gléas_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int parsáil_slánuimhir(int suíomh) {
        return rannán_sonraí[suíomh] | rannán_sonraí[suíomh + 1] << 8 | rannán_sonraí[suíomh + 2] << 16 | rannán_sonraí[suíomh + 3] << 24;
    }
    static void scríobh_slánuimhir_VALUE(int suíomh, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) rannán_sonraí[suíomh + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
