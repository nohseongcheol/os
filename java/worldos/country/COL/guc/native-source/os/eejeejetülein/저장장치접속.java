// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 alüjalee_ajutuu. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class 저장장치접속 {
    static boolean 사용가능 = false;
    static int[] alüjalee_atijaaya = new int[512];
    static void 잠깐기다리기() {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) serulaalü_ajutuu.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int 시작 = serulaalü_ajutuu.밀리초();
        while (serulaalü_ajutuu.밀리초() - 시작 < 500) {
            int jamakua_iparülein_ajutuu = serulaalü_ajutuu.입출력바이트읽기(0x1f7);
            if (jamakua_iparülein_ajutuu == 0 || jamakua_iparülein_ajutuu == 255) return -19;
            if ((jamakua_iparülein_ajutuu & 128) == 0) {
                if ((jamakua_iparülein_ajutuu & 33) != 0) return -5;
                if (!자료필요 || (jamakua_iparülein_ajutuu & 8) != 0) return 0;
            }
            serulaalü_ajutuu.잠시양보();
        }
        return -110;
    }
    static int 요청(int alüjalee_ajutuu, int aluwataaya) {
        if (alüjalee_ajutuu < 0 || alüjalee_ajutuu >= 2048) return -22;
        serulaalü_ajutuu.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        serulaalü_ajutuu.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        serulaalü_ajutuu.입출력바이트쓰기(0x1f2, 1);
        serulaalü_ajutuu.입출력바이트쓰기(0x1f3, alüjalee_ajutuu & 255);
        serulaalü_ajutuu.입출력바이트쓰기(0x1f4, (alüjalee_ajutuu >>> 8) & 255);
        serulaalü_ajutuu.입출력바이트쓰기(0x1f5, 0);
        serulaalü_ajutuu.입출력바이트쓰기(0x1f7, aluwataaya); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int alüjalee_ajutuu) {
        int 결과 = 요청(alüjalee_ajutuu, 0x20);
        if (결과 < 0) return 결과;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 256; ee_iyatialujuna++) {
            int ajutuu = serulaalü_ajutuu.입출력짧은수읽기(0x1f0);
            alüjalee_atijaaya[ee_iyatialujuna * 2] = ajutuu & 255; alüjalee_atijaaya[ee_iyatialujuna * 2 + 1] = ajutuu >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int ashajaa(int alüjalee_ajutuu) {
        if (!사용가능 || alüjalee_ajutuu < 1 || alüjalee_ajutuu > 518) return -19;
        int 결과 = 요청(alüjalee_ajutuu, 0x30);
        if (결과 < 0) return 결과;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 256; ee_iyatialujuna++)
            serulaalü_ajutuu.입출력짧은수쓰기(0x1f0, alüjalee_atijaaya[ee_iyatialujuna * 2] | alüjalee_atijaaya[ee_iyatialujuna * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        serulaalü_ajutuu.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int akatajaa_waneepiasü(int 위치) {
        return alüjalee_atijaaya[위치] | alüjalee_atijaaya[위치 + 1] << 8 | alüjalee_atijaaya[위치 + 2] << 16 | alüjalee_atijaaya[위치 + 3] << 24;
    }
    static void ashajaa_waneepiasü_ajutuu(int 위치, int ajutuu) {
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 4; ee_iyatialujuna++) alüjalee_atijaaya[위치 + ee_iyatialujuna] = (ajutuu >>> (ee_iyatialujuna * 8)) & 255;
    }
}
