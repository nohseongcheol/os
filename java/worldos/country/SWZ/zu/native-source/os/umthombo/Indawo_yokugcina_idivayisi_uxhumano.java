// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 isigaba_inani. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Indawo_yokugcina_idivayisi_uxhumano {
    static boolean 사용가능 = false;
    static int[] isigaba_imininingwane = new int[512];
    static void 잠깐기다리기() {
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) idivayisi_inani.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Sebenzisa = idivayisi_inani.밀리초();
        while (idivayisi_inani.밀리초() - Sebenzisa < 500) {
            int isimo_inani = idivayisi_inani.입출력바이트읽기(0x1f7);
            if (isimo_inani == 0 || isimo_inani == 255) return -19;
            if ((isimo_inani & 128) == 0) {
                if ((isimo_inani & 33) != 0) return -5;
                if (!자료필요 || (isimo_inani & 8) != 0) return 0;
            }
            idivayisi_inani.잠시양보();
        }
        return -110;
    }
    static int 요청(int isigaba_inani, int Umlayelo) {
        if (isigaba_inani < 0 || isigaba_inani >= 2048) return -22;
        idivayisi_inani.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        idivayisi_inani.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        idivayisi_inani.입출력바이트쓰기(0x1f2, 1);
        idivayisi_inani.입출력바이트쓰기(0x1f3, isigaba_inani & 255);
        idivayisi_inani.입출력바이트쓰기(0x1f4, (isigaba_inani >>> 8) & 255);
        idivayisi_inani.입출력바이트쓰기(0x1f5, 0);
        idivayisi_inani.입출력바이트쓰기(0x1f7, Umlayelo); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Funda(int isigaba_inani) {
        int 결과 = 요청(isigaba_inani, 0x20);
        if (결과 < 0) return 결과;
        for (int thola_inkomba = 0; thola_inkomba < 256; thola_inkomba++) {
            int inani = idivayisi_inani.입출력짧은수읽기(0x1f0);
            isigaba_imininingwane[thola_inkomba * 2] = inani & 255; isigaba_imininingwane[thola_inkomba * 2 + 1] = inani >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Bhala(int isigaba_inani) {
        if (!사용가능 || isigaba_inani < 1 || isigaba_inani > 518) return -19;
        int 결과 = 요청(isigaba_inani, 0x30);
        if (결과 < 0) return 결과;
        for (int thola_inkomba = 0; thola_inkomba < 256; thola_inkomba++)
            idivayisi_inani.입출력짧은수쓰기(0x1f0, isigaba_imininingwane[thola_inkomba * 2] | isigaba_imininingwane[thola_inkomba * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        idivayisi_inani.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int zawula_inamba(int 위치) {
        return isigaba_imininingwane[위치] | isigaba_imininingwane[위치 + 1] << 8 | isigaba_imininingwane[위치 + 2] << 16 | isigaba_imininingwane[위치 + 3] << 24;
    }
    static void bhala_inamba_inani(int 위치, int inani) {
        for (int thola_inkomba = 0; thola_inkomba < 4; thola_inkomba++) isigaba_imininingwane[위치 + thola_inkomba] = (inani >>> (thola_inkomba * 8)) & 255;
    }
}
