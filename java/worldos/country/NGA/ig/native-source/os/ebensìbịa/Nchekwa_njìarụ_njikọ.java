// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 nkebì_valuu. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Nchekwa_njìarụ_njikọ {
    static boolean 사용가능 = false;
    static int[] nkebì_datà = new int[512];
    static void 잠깐기다리기() {
        for (int indèks = 0; indèks < 4; indèks++) njìarụ_valuu.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Bido = njìarụ_valuu.밀리초();
        while (njìarụ_valuu.밀리초() - Bido < 500) {
            int ọnọdụ_valuu = njìarụ_valuu.입출력바이트읽기(0x1f7);
            if (ọnọdụ_valuu == 0 || ọnọdụ_valuu == 255) return -19;
            if ((ọnọdụ_valuu & 128) == 0) {
                if ((ọnọdụ_valuu & 33) != 0) return -5;
                if (!자료필요 || (ọnọdụ_valuu & 8) != 0) return 0;
            }
            njìarụ_valuu.잠시양보();
        }
        return -110;
    }
    static int 요청(int nkebì_valuu, int Ntiiwu) {
        if (nkebì_valuu < 0 || nkebì_valuu >= 2048) return -22;
        njìarụ_valuu.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        njìarụ_valuu.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        njìarụ_valuu.입출력바이트쓰기(0x1f2, 1);
        njìarụ_valuu.입출력바이트쓰기(0x1f3, nkebì_valuu & 255);
        njìarụ_valuu.입출력바이트쓰기(0x1f4, (nkebì_valuu >>> 8) & 255);
        njìarụ_valuu.입출력바이트쓰기(0x1f5, 0);
        njìarụ_valuu.입출력바이트쓰기(0x1f7, Ntiiwu); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Wepụta_ọzi(int nkebì_valuu) {
        int 결과 = 요청(nkebì_valuu, 0x20);
        if (결과 < 0) return 결과;
        for (int indèks = 0; indèks < 256; indèks++) {
            int valuu = njìarụ_valuu.입출력짧은수읽기(0x1f0);
            nkebì_datà[indèks * 2] = valuu & 255; nkebì_datà[indèks * 2 + 1] = valuu >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Chekwaa_ozi(int nkebì_valuu) {
        if (!사용가능 || nkebì_valuu < 1 || nkebì_valuu > 518) return -19;
        int 결과 = 요청(nkebì_valuu, 0x30);
        if (결과 < 0) return 결과;
        for (int indèks = 0; indèks < 256; indèks++)
            njìarụ_valuu.입출력짧은수쓰기(0x1f0, nkebì_datà[indèks * 2] | nkebì_datà[indèks * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        njìarụ_valuu.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int kerìsịa_ọnụọgụ_nzùrùòkè(int 위치) {
        return nkebì_datà[위치] | nkebì_datà[위치 + 1] << 8 | nkebì_datà[위치 + 2] << 16 | nkebì_datà[위치 + 3] << 24;
    }
    static void dee_ọnụọgụ_nzùrùòkè_valuu(int 위치, int valuu) {
        for (int indèks = 0; indèks < 4; indèks++) nkebì_datà[위치 + indèks] = (valuu >>> (indèks * 8)) & 255;
    }
}
