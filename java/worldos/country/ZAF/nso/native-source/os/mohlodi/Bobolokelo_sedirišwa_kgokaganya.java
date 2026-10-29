// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 karolo_boleng. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Bobolokelo_sedirišwa_kgokaganya {
    static boolean 사용가능 = false;
    static int[] karolo_data = new int[512];
    static void 잠깐기다리기() {
        for (int lokela = 0; lokela < 4; lokela++) sedirišwa_boleng.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Diriša = sedirišwa_boleng.밀리초();
        while (sedirišwa_boleng.밀리초() - Diriša < 500) {
            int boemo_boleng = sedirišwa_boleng.입출력바이트읽기(0x1f7);
            if (boemo_boleng == 0 || boemo_boleng == 255) return -19;
            if ((boemo_boleng & 128) == 0) {
                if ((boemo_boleng & 33) != 0) return -5;
                if (!자료필요 || (boemo_boleng & 8) != 0) return 0;
            }
            sedirišwa_boleng.잠시양보();
        }
        return -110;
    }
    static int 요청(int karolo_boleng, int Taelo) {
        if (karolo_boleng < 0 || karolo_boleng >= 2048) return -22;
        sedirišwa_boleng.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        sedirišwa_boleng.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        sedirišwa_boleng.입출력바이트쓰기(0x1f2, 1);
        sedirišwa_boleng.입출력바이트쓰기(0x1f3, karolo_boleng & 255);
        sedirišwa_boleng.입출력바이트쓰기(0x1f4, (karolo_boleng >>> 8) & 255);
        sedirišwa_boleng.입출력바이트쓰기(0x1f5, 0);
        sedirišwa_boleng.입출력바이트쓰기(0x1f7, Taelo); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Bala(int karolo_boleng) {
        int 결과 = 요청(karolo_boleng, 0x20);
        if (결과 < 0) return 결과;
        for (int lokela = 0; lokela < 256; lokela++) {
            int boleng = sedirišwa_boleng.입출력짧은수읽기(0x1f0);
            karolo_data[lokela * 2] = boleng & 255; karolo_data[lokela * 2 + 1] = boleng >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Ngwala(int karolo_boleng) {
        if (!사용가능 || karolo_boleng < 1 || karolo_boleng > 518) return -19;
        int 결과 = 요청(karolo_boleng, 0x30);
        if (결과 < 0) return 결과;
        for (int lokela = 0; lokela < 256; lokela++)
            sedirišwa_boleng.입출력짧은수쓰기(0x1f0, karolo_data[lokela * 2] | karolo_data[lokela * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        sedirišwa_boleng.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int ripaganya_palotlalo(int 위치) {
        return karolo_data[위치] | karolo_data[위치 + 1] << 8 | karolo_data[위치 + 2] << 16 | karolo_data[위치 + 3] << 24;
    }
    static void ngwala_palotlalo_boleng(int 위치, int boleng) {
        for (int lokela = 0; lokela < 4; lokela++) karolo_data[위치 + lokela] = (boleng >>> (lokela * 8)) & 255;
    }
}
