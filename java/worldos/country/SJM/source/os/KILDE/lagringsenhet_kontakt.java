// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 inndeling_VERDI. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class lagringsenhet_kontakt {
    static boolean informasjonssystemer_Aktiv_9e72441a = false;
    static int[] inndeling_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) enhet_VERDI.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Kjør_2 = enhet_VERDI.밀리초();
        while (enhet_VERDI.밀리초() - Kjør_2 < 500) {
            int status_VERDI = enhet_VERDI.입출력바이트읽기(0x1f7);
            if (status_VERDI == 0 || status_VERDI == 255) return -19;
            if ((status_VERDI & 128) == 0) {
                if ((status_VERDI & 33) != 0) return -5;
                if (!자료필요 || (status_VERDI & 8) != 0) return 0;
            }
            enhet_VERDI.잠시양보();
        }
        return -110;
    }
    static int forespørsel(int inndeling_VERDI, int Kommando) {
        if (inndeling_VERDI < 0 || inndeling_VERDI >= 2048) return -22;
        enhet_VERDI.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ bruk_VERDI 안 함
        enhet_VERDI.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int KR = 준비기다리기(false);
        if (KR < 0) return KR;
        enhet_VERDI.입출력바이트쓰기(0x1f2, 1);
        enhet_VERDI.입출력바이트쓰기(0x1f3, inndeling_VERDI & 255);
        enhet_VERDI.입출력바이트쓰기(0x1f4, (inndeling_VERDI >>> 8) & 255);
        enhet_VERDI.입출력바이트쓰기(0x1f5, 0);
        enhet_VERDI.입출력바이트쓰기(0x1f7, Kommando); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Les(int inndeling_VERDI) {
        int KR = forespørsel(inndeling_VERDI, 0x20);
        if (KR < 0) return KR;
        for (int INDEKS = 0; INDEKS < 256; INDEKS++) {
            int VERDI = enhet_VERDI.입출력짧은수읽기(0x1f0);
            inndeling_data[INDEKS * 2] = VERDI & 255; inndeling_data[INDEKS * 2 + 1] = VERDI >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Skriv(int inndeling_VERDI) {
        if (!informasjonssystemer_Aktiv_9e72441a || inndeling_VERDI < 1 || inndeling_VERDI > 518) return -19;
        int KR = forespørsel(inndeling_VERDI, 0x30);
        if (KR < 0) return KR;
        for (int INDEKS = 0; INDEKS < 256; INDEKS++)
            enhet_VERDI.입출력짧은수쓰기(0x1f0, inndeling_data[INDEKS * 2] | inndeling_data[INDEKS * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informasjonssystemer_Aktiv_9e72441a) return -19;
        enhet_VERDI.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int dele_opp_heltall(int Posisjon) {
        return inndeling_data[Posisjon] | inndeling_data[Posisjon + 1] << 8 | inndeling_data[Posisjon + 2] << 16 | inndeling_data[Posisjon + 3] << 24;
    }
    static void skrive_heltall_VERDI(int Posisjon, int VERDI) {
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) inndeling_data[Posisjon + INDEKS] = (VERDI >>> (INDEKS * 8)) & 255;
    }
}
