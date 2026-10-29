// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 bo_lim_VALUE_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Xotira_qurilma_aloqa {
    static boolean 사용가능 = false;
    static int[] bo_lim_ma_lumotlar = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) qurilma_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Bajarish = qurilma_VALUE.밀리초();
        while (qurilma_VALUE.밀리초() - Bajarish < 500) {
            int holat_VALUE_e10195a1 = qurilma_VALUE.입출력바이트읽기(0x1f7);
            if (holat_VALUE_e10195a1 == 0 || holat_VALUE_e10195a1 == 255) return -19;
            if ((holat_VALUE_e10195a1 & 128) == 0) {
                if ((holat_VALUE_e10195a1 & 33) != 0) return -5;
                if (!자료필요 || (holat_VALUE_e10195a1 & 8) != 0) return 0;
            }
            qurilma_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int bo_lim_VALUE_366e0bfa, int Buyruq) {
        if (bo_lim_VALUE_366e0bfa < 0 || bo_lim_VALUE_366e0bfa >= 2048) return -22;
        qurilma_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        qurilma_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int o_lchov = 준비기다리기(false);
        if (o_lchov < 0) return o_lchov;
        qurilma_VALUE.입출력바이트쓰기(0x1f2, 1);
        qurilma_VALUE.입출력바이트쓰기(0x1f3, bo_lim_VALUE_366e0bfa & 255);
        qurilma_VALUE.입출력바이트쓰기(0x1f4, (bo_lim_VALUE_366e0bfa >>> 8) & 255);
        qurilma_VALUE.입출력바이트쓰기(0x1f5, 0);
        qurilma_VALUE.입출력바이트쓰기(0x1f7, Buyruq); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Oʻqish(int bo_lim_VALUE_366e0bfa) {
        int o_lchov = 요청(bo_lim_VALUE_366e0bfa, 0x20);
        if (o_lchov < 0) return o_lchov;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = qurilma_VALUE.입출력짧은수읽기(0x1f0);
            bo_lim_ma_lumotlar[INDEX * 2] = VALUE & 255; bo_lim_ma_lumotlar[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Yozish(int bo_lim_VALUE_366e0bfa) {
        if (!사용가능 || bo_lim_VALUE_366e0bfa < 1 || bo_lim_VALUE_366e0bfa > 518) return -19;
        int o_lchov = 요청(bo_lim_VALUE_366e0bfa, 0x30);
        if (o_lchov < 0) return o_lchov;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            qurilma_VALUE.입출력짧은수쓰기(0x1f0, bo_lim_ma_lumotlar[INDEX * 2] | bo_lim_ma_lumotlar[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        qurilma_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int tahlil_qilmoq_butun_son(int Holati) {
        return bo_lim_ma_lumotlar[Holati] | bo_lim_ma_lumotlar[Holati + 1] << 8 | bo_lim_ma_lumotlar[Holati + 2] << 16 | bo_lim_ma_lumotlar[Holati + 3] << 24;
    }
    static void yozmoq_butun_son_VALUE(int Holati, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) bo_lim_ma_lumotlar[Holati + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
