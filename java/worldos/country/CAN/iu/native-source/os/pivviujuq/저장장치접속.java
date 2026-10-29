// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sukuttia_atuutilik. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class 저장장치접속 {
    static boolean 사용가능 = false;
    static int[] sukuttia_titiqqat = new int[512];
    static void 잠깐기다리기() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) sunakkutaaq_atuutilik.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int 시작 = sunakkutaaq_atuutilik.밀리초();
        while (sunakkutaaq_atuutilik.밀리초() - 시작 < 500) {
            int qanuilinganiq_atuutilik = sunakkutaaq_atuutilik.입출력바이트읽기(0x1f7);
            if (qanuilinganiq_atuutilik == 0 || qanuilinganiq_atuutilik == 255) return -19;
            if ((qanuilinganiq_atuutilik & 128) == 0) {
                if ((qanuilinganiq_atuutilik & 33) != 0) return -5;
                if (!자료필요 || (qanuilinganiq_atuutilik & 8) != 0) return 0;
            }
            sunakkutaaq_atuutilik.잠시양보();
        }
        return -110;
    }
    static int 요청(int sukuttia_atuutilik, int piqujijjut) {
        if (sukuttia_atuutilik < 0 || sukuttia_atuutilik >= 2048) return -22;
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f2, 1);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f3, sukuttia_atuutilik & 255);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f4, (sukuttia_atuutilik >>> 8) & 255);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f5, 0);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f7, piqujijjut); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int sukuttia_atuutilik) {
        int 결과 = 요청(sukuttia_atuutilik, 0x20);
        if (결과 < 0) return 결과;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 256; nalunaiqsimavik++) {
            int atuutilik = sunakkutaaq_atuutilik.입출력짧은수읽기(0x1f0);
            sukuttia_titiqqat[nalunaiqsimavik * 2] = atuutilik & 255; sukuttia_titiqqat[nalunaiqsimavik * 2 + 1] = atuutilik >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int titiraq(int sukuttia_atuutilik) {
        if (!사용가능 || sukuttia_atuutilik < 1 || sukuttia_atuutilik > 518) return -19;
        int 결과 = 요청(sukuttia_atuutilik, 0x30);
        if (결과 < 0) return 결과;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 256; nalunaiqsimavik++)
            sunakkutaaq_atuutilik.입출력짧은수쓰기(0x1f0, sukuttia_titiqqat[nalunaiqsimavik * 2] | sukuttia_titiqqat[nalunaiqsimavik * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int agguqtuut_naasaut(int 위치) {
        return sukuttia_titiqqat[위치] | sukuttia_titiqqat[위치 + 1] << 8 | sukuttia_titiqqat[위치 + 2] << 16 | sukuttia_titiqqat[위치 + 3] << 24;
    }
    static void titiraq_naasaut_atuutilik(int 위치, int atuutilik) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 4; nalunaiqsimavik++) sukuttia_titiqqat[위치 + nalunaiqsimavik] = (atuutilik >>> (nalunaiqsimavik * 8)) & 255;
    }
}
