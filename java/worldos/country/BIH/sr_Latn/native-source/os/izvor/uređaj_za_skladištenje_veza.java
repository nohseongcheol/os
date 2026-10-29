// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 odeljak_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class uređaj_za_skladištenje_veza {
    static boolean informatičko_odeljenje_Aktivan_9e72441a = false;
    static int[] odeljak_podaci = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int koristiti = uređaj_VALUE.밀리초();
        while (uređaj_VALUE.밀리초() - koristiti < 500) {
            int Status_VALUE = uređaj_VALUE.입출력바이트읽기(0x1f7);
            if (Status_VALUE == 0 || Status_VALUE == 255) return -19;
            if ((Status_VALUE & 128) == 0) {
                if ((Status_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Status_VALUE & 8) != 0) return 0;
            }
            uređaj_VALUE.잠시양보();
        }
        return -110;
    }
    static int zahtev(int odeljak_VALUE, int komanda) {
        if (odeljak_VALUE < 0 || odeljak_VALUE >= 2048) return -22;
        uređaj_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ koristiti_VALUE 안 함
        uređaj_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int KR = 준비기다리기(false);
        if (KR < 0) return KR;
        uređaj_VALUE.입출력바이트쓰기(0x1f2, 1);
        uređaj_VALUE.입출력바이트쓰기(0x1f3, odeljak_VALUE & 255);
        uređaj_VALUE.입출력바이트쓰기(0x1f4, (odeljak_VALUE >>> 8) & 255);
        uređaj_VALUE.입출력바이트쓰기(0x1f5, 0);
        uređaj_VALUE.입출력바이트쓰기(0x1f7, komanda); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int odeljak_VALUE) {
        int KR = zahtev(odeljak_VALUE, 0x20);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = uređaj_VALUE.입출력짧은수읽기(0x1f0);
            odeljak_podaci[INDEX * 2] = VALUE & 255; odeljak_podaci[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 쓰기(int odeljak_VALUE) {
        if (!informatičko_odeljenje_Aktivan_9e72441a || odeljak_VALUE < 1 || odeljak_VALUE > 518) return -19;
        int KR = zahtev(odeljak_VALUE, 0x30);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            uređaj_VALUE.입출력짧은수쓰기(0x1f0, odeljak_podaci[INDEX * 2] | odeljak_podaci[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informatičko_odeljenje_Aktivan_9e72441a) return -19;
        uređaj_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int raščlaniti_ceo_broj(int pozicija) {
        return odeljak_podaci[pozicija] | odeljak_podaci[pozicija + 1] << 8 | odeljak_podaci[pozicija + 2] << 16 | odeljak_podaci[pozicija + 3] << 24;
    }
    static void 정수쓰기(int pozicija, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) odeljak_podaci[pozicija + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
