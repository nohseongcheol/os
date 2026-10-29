// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 avsnitt_värde. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class lagringsenhet_kontakt {
    static boolean informationsteknik_Aktiv_9e72441a = false;
    static int[] avsnitt_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) enhet_värde.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Kör = enhet_värde.밀리초();
        while (enhet_värde.밀리초() - Kör < 500) {
            int status_värde = enhet_värde.입출력바이트읽기(0x1f7);
            if (status_värde == 0 || status_värde == 255) return -19;
            if ((status_värde & 128) == 0) {
                if ((status_värde & 33) != 0) return -5;
                if (!자료필요 || (status_värde & 8) != 0) return 0;
            }
            enhet_värde.잠시양보();
        }
        return -110;
    }
    static int begäran(int avsnitt_värde, int kommando) {
        if (avsnitt_värde < 0 || avsnitt_värde >= 2048) return -22;
        enhet_värde.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ använda_värde 안 함
        enhet_värde.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int RESULTAT = 준비기다리기(false);
        if (RESULTAT < 0) return RESULTAT;
        enhet_värde.입출력바이트쓰기(0x1f2, 1);
        enhet_värde.입출력바이트쓰기(0x1f3, avsnitt_värde & 255);
        enhet_värde.입출력바이트쓰기(0x1f4, (avsnitt_värde >>> 8) & 255);
        enhet_värde.입출력바이트쓰기(0x1f5, 0);
        enhet_värde.입출력바이트쓰기(0x1f7, kommando); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Läs(int avsnitt_värde) {
        int RESULTAT = begäran(avsnitt_värde, 0x20);
        if (RESULTAT < 0) return RESULTAT;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int värde = enhet_värde.입출력짧은수읽기(0x1f0);
            avsnitt_data[INDEX * 2] = värde & 255; avsnitt_data[INDEX * 2 + 1] = värde >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Skriv(int avsnitt_värde) {
        if (!informationsteknik_Aktiv_9e72441a || avsnitt_värde < 1 || avsnitt_värde > 518) return -19;
        int RESULTAT = begäran(avsnitt_värde, 0x30);
        if (RESULTAT < 0) return RESULTAT;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            enhet_värde.입출력짧은수쓰기(0x1f0, avsnitt_data[INDEX * 2] | avsnitt_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int tömma_utleverans() {
        if (!informationsteknik_Aktiv_9e72441a) return -19;
        enhet_värde.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int parsa_heltal(int position) {
        return avsnitt_data[position] | avsnitt_data[position + 1] << 8 | avsnitt_data[position + 2] << 16 | avsnitt_data[position + 3] << 24;
    }
    static void skriva_heltal_värde(int position, int värde) {
        for (int INDEX = 0; INDEX < 4; INDEX++) avsnitt_data[position + INDEX] = (värde >>> (INDEX * 8)) & 255;
    }
}
