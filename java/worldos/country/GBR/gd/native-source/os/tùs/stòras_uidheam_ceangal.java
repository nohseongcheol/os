// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 earrann_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class stòras_uidheam_ceangal {
    static boolean 사용가능 = false;
    static int[] earrann_dàta = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) uidheam_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int ruith = uidheam_VALUE.밀리초();
        while (uidheam_VALUE.밀리초() - ruith < 500) {
            int cor_VALUE = uidheam_VALUE.입출력바이트읽기(0x1f7);
            if (cor_VALUE == 0 || cor_VALUE == 255) return -19;
            if ((cor_VALUE & 128) == 0) {
                if ((cor_VALUE & 33) != 0) return -5;
                if (!자료필요 || (cor_VALUE & 8) != 0) return 0;
            }
            uidheam_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int earrann_VALUE, int àithne) {
        if (earrann_VALUE < 0 || earrann_VALUE >= 2048) return -22;
        uidheam_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        uidheam_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int tomhas = 준비기다리기(false);
        if (tomhas < 0) return tomhas;
        uidheam_VALUE.입출력바이트쓰기(0x1f2, 1);
        uidheam_VALUE.입출력바이트쓰기(0x1f3, earrann_VALUE & 255);
        uidheam_VALUE.입출력바이트쓰기(0x1f4, (earrann_VALUE >>> 8) & 255);
        uidheam_VALUE.입출력바이트쓰기(0x1f5, 0);
        uidheam_VALUE.입출력바이트쓰기(0x1f7, àithne); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int earrann_VALUE) {
        int tomhas = 요청(earrann_VALUE, 0x20);
        if (tomhas < 0) return tomhas;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = uidheam_VALUE.입출력짧은수읽기(0x1f0);
            earrann_dàta[INDEX * 2] = VALUE & 255; earrann_dàta[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int sgrìobh(int earrann_VALUE) {
        if (!사용가능 || earrann_VALUE < 1 || earrann_VALUE > 518) return -19;
        int tomhas = 요청(earrann_VALUE, 0x30);
        if (tomhas < 0) return tomhas;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            uidheam_VALUE.입출력짧은수쓰기(0x1f0, earrann_dàta[INDEX * 2] | earrann_dàta[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        uidheam_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int 정수읽기(int suidhich) {
        return earrann_dàta[suidhich] | earrann_dàta[suidhich + 1] << 8 | earrann_dàta[suidhich + 2] << 16 | earrann_dàta[suidhich + 3] << 24;
    }
    static void sgrìobh_àireamh_shlàn_VALUE(int suidhich, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) earrann_dàta[suidhich + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
