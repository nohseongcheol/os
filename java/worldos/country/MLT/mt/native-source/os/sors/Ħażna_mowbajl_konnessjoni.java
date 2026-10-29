// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 taqsima_VALUE_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Ħażna_mowbajl_konnessjoni {
    static boolean 사용가능 = false;
    static int[] taqsima_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mowbajl_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int serje = mowbajl_VALUE.밀리초();
        while (mowbajl_VALUE.밀리초() - serje < 500) {
            int stat_VALUE = mowbajl_VALUE.입출력바이트읽기(0x1f7);
            if (stat_VALUE == 0 || stat_VALUE == 255) return -19;
            if ((stat_VALUE & 128) == 0) {
                if ((stat_VALUE & 33) != 0) return -5;
                if (!자료필요 || (stat_VALUE & 8) != 0) return 0;
            }
            mowbajl_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int taqsima_VALUE_366e0bfa, int kmand) {
        if (taqsima_VALUE_366e0bfa < 0 || taqsima_VALUE_366e0bfa >= 2048) return -22;
        mowbajl_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        mowbajl_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int miżura = 준비기다리기(false);
        if (miżura < 0) return miżura;
        mowbajl_VALUE.입출력바이트쓰기(0x1f2, 1);
        mowbajl_VALUE.입출력바이트쓰기(0x1f3, taqsima_VALUE_366e0bfa & 255);
        mowbajl_VALUE.입출력바이트쓰기(0x1f4, (taqsima_VALUE_366e0bfa >>> 8) & 255);
        mowbajl_VALUE.입출력바이트쓰기(0x1f5, 0);
        mowbajl_VALUE.입출력바이트쓰기(0x1f7, kmand); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int taqsima_VALUE_366e0bfa) {
        int miżura = 요청(taqsima_VALUE_366e0bfa, 0x20);
        if (miżura < 0) return miżura;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = mowbajl_VALUE.입출력짧은수읽기(0x1f0);
            taqsima_data[INDEX * 2] = VALUE & 255; taqsima_data[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int kiteb(int taqsima_VALUE_366e0bfa) {
        if (!사용가능 || taqsima_VALUE_366e0bfa < 1 || taqsima_VALUE_366e0bfa > 518) return -19;
        int miżura = 요청(taqsima_VALUE_366e0bfa, 0x30);
        if (miżura < 0) return miżura;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mowbajl_VALUE.입출력짧은수쓰기(0x1f0, taqsima_data[INDEX * 2] | taqsima_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        mowbajl_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizza_numru_sħiħ(int pożizzjoni) {
        return taqsima_data[pożizzjoni] | taqsima_data[pożizzjoni + 1] << 8 | taqsima_data[pożizzjoni + 2] << 16 | taqsima_data[pożizzjoni + 3] << 24;
    }
    static void kiteb_numru_sħiħ_VALUE(int pożizzjoni, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) taqsima_data[pożizzjoni + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
