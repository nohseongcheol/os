// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 karolo_Boleng. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Polokelo_mobaele_Kgolagano {
    static boolean 사용가능 = false;
    static int[] karolo_tshedimosetso_93985c38 = new int[512];
    static void 잠깐기다리기() {
        for (int tshupane = 0; tshupane < 4; tshupane++) mobaele_Boleng.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int dirisa = mobaele_Boleng.밀리초();
        while (mobaele_Boleng.밀리초() - dirisa < 500) {
            int kemo_Boleng = mobaele_Boleng.입출력바이트읽기(0x1f7);
            if (kemo_Boleng == 0 || kemo_Boleng == 255) return -19;
            if ((kemo_Boleng & 128) == 0) {
                if ((kemo_Boleng & 33) != 0) return -5;
                if (!자료필요 || (kemo_Boleng & 8) != 0) return 0;
            }
            mobaele_Boleng.잠시양보();
        }
        return -110;
    }
    static int 요청(int karolo_Boleng, int Taelo) {
        if (karolo_Boleng < 0 || karolo_Boleng >= 2048) return -22;
        mobaele_Boleng.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        mobaele_Boleng.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        mobaele_Boleng.입출력바이트쓰기(0x1f2, 1);
        mobaele_Boleng.입출력바이트쓰기(0x1f3, karolo_Boleng & 255);
        mobaele_Boleng.입출력바이트쓰기(0x1f4, (karolo_Boleng >>> 8) & 255);
        mobaele_Boleng.입출력바이트쓰기(0x1f5, 0);
        mobaele_Boleng.입출력바이트쓰기(0x1f7, Taelo); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int karolo_Boleng) {
        int 결과 = 요청(karolo_Boleng, 0x20);
        if (결과 < 0) return 결과;
        for (int tshupane = 0; tshupane < 256; tshupane++) {
            int Boleng = mobaele_Boleng.입출력짧은수읽기(0x1f0);
            karolo_tshedimosetso_93985c38[tshupane * 2] = Boleng & 255; karolo_tshedimosetso_93985c38[tshupane * 2 + 1] = Boleng >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int kwala(int karolo_Boleng) {
        if (!사용가능 || karolo_Boleng < 1 || karolo_Boleng > 518) return -19;
        int 결과 = 요청(karolo_Boleng, 0x30);
        if (결과 < 0) return 결과;
        for (int tshupane = 0; tshupane < 256; tshupane++)
            mobaele_Boleng.입출력짧은수쓰기(0x1f0, karolo_tshedimosetso_93985c38[tshupane * 2] | karolo_tshedimosetso_93985c38[tshupane * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        mobaele_Boleng.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int go_lokolola_Palotlalo(int 위치) {
        return karolo_tshedimosetso_93985c38[위치] | karolo_tshedimosetso_93985c38[위치 + 1] << 8 | karolo_tshedimosetso_93985c38[위치 + 2] << 16 | karolo_tshedimosetso_93985c38[위치 + 3] << 24;
    }
    static void kwala_Palotlalo_Boleng(int 위치, int Boleng) {
        for (int tshupane = 0; tshupane < 4; tshupane++) karolo_tshedimosetso_93985c38[위치 + tshupane] = (Boleng >>> (tshupane * 8)) & 255;
    }
}
