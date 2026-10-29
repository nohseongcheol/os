// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 wāhanga_uara. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Rokiroki_pūkoro_hononga {
    static boolean 사용가능 = false;
    static int[] wāhanga_raraunga = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) pūkoro_uara.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int whakahaere = pūkoro_uara.밀리초();
        while (pūkoro_uara.밀리초() - whakahaere < 500) {
            int tūnga_uara = pūkoro_uara.입출력바이트읽기(0x1f7);
            if (tūnga_uara == 0 || tūnga_uara == 255) return -19;
            if ((tūnga_uara & 128) == 0) {
                if ((tūnga_uara & 33) != 0) return -5;
                if (!자료필요 || (tūnga_uara & 8) != 0) return 0;
            }
            pūkoro_uara.잠시양보();
        }
        return -110;
    }
    static int 요청(int wāhanga_uara, int tono) {
        if (wāhanga_uara < 0 || wāhanga_uara >= 2048) return -22;
        pūkoro_uara.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        pūkoro_uara.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int mēhua = 준비기다리기(false);
        if (mēhua < 0) return mēhua;
        pūkoro_uara.입출력바이트쓰기(0x1f2, 1);
        pūkoro_uara.입출력바이트쓰기(0x1f3, wāhanga_uara & 255);
        pūkoro_uara.입출력바이트쓰기(0x1f4, (wāhanga_uara >>> 8) & 255);
        pūkoro_uara.입출력바이트쓰기(0x1f5, 0);
        pūkoro_uara.입출력바이트쓰기(0x1f7, tono); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Pānuitia(int wāhanga_uara) {
        int mēhua = 요청(wāhanga_uara, 0x20);
        if (mēhua < 0) return mēhua;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int uara = pūkoro_uara.입출력짧은수읽기(0x1f0);
            wāhanga_raraunga[INDEX * 2] = uara & 255; wāhanga_raraunga[INDEX * 2 + 1] = uara >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Tuhia(int wāhanga_uara) {
        if (!사용가능 || wāhanga_uara < 1 || wāhanga_uara > 518) return -19;
        int mēhua = 요청(wāhanga_uara, 0x30);
        if (mēhua < 0) return mēhua;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            pūkoro_uara.입출력짧은수쓰기(0x1f0, wāhanga_raraunga[INDEX * 2] | wāhanga_raraunga[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        pūkoro_uara.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int poroporo_tau_tōpū(int tūranga) {
        return wāhanga_raraunga[tūranga] | wāhanga_raraunga[tūranga + 1] << 8 | wāhanga_raraunga[tūranga + 2] << 16 | wāhanga_raraunga[tūranga + 3] << 24;
    }
    static void tuhi_tau_tōpū_uara(int tūranga, int uara) {
        for (int INDEX = 0; INDEX < 4; INDEX++) wāhanga_raraunga[tūranga + INDEX] = (uara >>> (INDEX * 8)) & 255;
    }
}
