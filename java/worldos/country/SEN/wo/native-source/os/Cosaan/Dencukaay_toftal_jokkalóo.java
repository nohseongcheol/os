// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 dog_xëyma. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Dencukaay_toftal_jokkalóo {
    static boolean 사용가능 = false;
    static int[] dog_mbir = new int[512];
    static void 잠깐기다리기() {
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) toftal_xëyma.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int daw = toftal_xëyma.밀리초();
        while (toftal_xëyma.밀리초() - daw < 500) {
            int nekkin_xëyma = toftal_xëyma.입출력바이트읽기(0x1f7);
            if (nekkin_xëyma == 0 || nekkin_xëyma == 255) return -19;
            if ((nekkin_xëyma & 128) == 0) {
                if ((nekkin_xëyma & 33) != 0) return -5;
                if (!자료필요 || (nekkin_xëyma & 8) != 0) return 0;
            }
            toftal_xëyma.잠시양보();
        }
        return -110;
    }
    static int 요청(int dog_xëyma, int ndigel) {
        if (dog_xëyma < 0 || dog_xëyma >= 2048) return -22;
        toftal_xëyma.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        toftal_xëyma.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        toftal_xëyma.입출력바이트쓰기(0x1f2, 1);
        toftal_xëyma.입출력바이트쓰기(0x1f3, dog_xëyma & 255);
        toftal_xëyma.입출력바이트쓰기(0x1f4, (dog_xëyma >>> 8) & 255);
        toftal_xëyma.입출력바이트쓰기(0x1f5, 0);
        toftal_xëyma.입출력바이트쓰기(0x1f7, ndigel); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int dog_xëyma) {
        int 결과 = 요청(dog_xëyma, 0x20);
        if (결과 < 0) return 결과;
        for (int àlluwa_tur = 0; àlluwa_tur < 256; àlluwa_tur++) {
            int xëyma = toftal_xëyma.입출력짧은수읽기(0x1f0);
            dog_mbir[àlluwa_tur * 2] = xëyma & 255; dog_mbir[àlluwa_tur * 2 + 1] = xëyma >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int biir(int dog_xëyma) {
        if (!사용가능 || dog_xëyma < 1 || dog_xëyma > 518) return -19;
        int 결과 = 요청(dog_xëyma, 0x30);
        if (결과 < 0) return 결과;
        for (int àlluwa_tur = 0; àlluwa_tur < 256; àlluwa_tur++)
            toftal_xëyma.입출력짧은수쓰기(0x1f0, dog_mbir[àlluwa_tur * 2] | dog_mbir[àlluwa_tur * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        toftal_xëyma.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int Segg_lëmm(int 위치) {
        return dog_mbir[위치] | dog_mbir[위치 + 1] << 8 | dog_mbir[위치 + 2] << 16 | dog_mbir[위치 + 3] << 24;
    }
    static void biir_lëmm_xëyma(int 위치, int xëyma) {
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) dog_mbir[위치 + àlluwa_tur] = (xëyma >>> (àlluwa_tur * 8)) & 255;
    }
}
