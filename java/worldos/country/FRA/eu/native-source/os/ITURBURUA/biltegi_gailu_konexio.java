// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sekzio_balio. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class biltegi_gailu_konexio {
    static boolean informatika_libre = false;
    static int[] sekzio_datuak = new int[512];
    static void 잠깐기다리기() {
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) gailu_balio.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Exekutatu_2 = gailu_balio.밀리초();
        while (gailu_balio.밀리초() - Exekutatu_2 < 500) {
            int Egoera_balio = gailu_balio.입출력바이트읽기(0x1f7);
            if (Egoera_balio == 0 || Egoera_balio == 255) return -19;
            if ((Egoera_balio & 128) == 0) {
                if ((Egoera_balio & 33) != 0) return -5;
                if (!자료필요 || (Egoera_balio & 8) != 0) return 0;
            }
            gailu_balio.잠시양보();
        }
        return -110;
    }
    static int eskaera(int sekzio_balio, int Komandoa) {
        if (sekzio_balio < 0 || sekzio_balio >= 2048) return -22;
        gailu_balio.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        gailu_balio.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int EMAITZA = 준비기다리기(false);
        if (EMAITZA < 0) return EMAITZA;
        gailu_balio.입출력바이트쓰기(0x1f2, 1);
        gailu_balio.입출력바이트쓰기(0x1f3, sekzio_balio & 255);
        gailu_balio.입출력바이트쓰기(0x1f4, (sekzio_balio >>> 8) & 255);
        gailu_balio.입출력바이트쓰기(0x1f5, 0);
        gailu_balio.입출력바이트쓰기(0x1f7, Komandoa); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Irakurri(int sekzio_balio) {
        int EMAITZA = eskaera(sekzio_balio, 0x20);
        if (EMAITZA < 0) return EMAITZA;
        for (int INDIZE = 0; INDIZE < 256; INDIZE++) {
            int balio = gailu_balio.입출력짧은수읽기(0x1f0);
            sekzio_datuak[INDIZE * 2] = balio & 255; sekzio_datuak[INDIZE * 2 + 1] = balio >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Idatzi(int sekzio_balio) {
        if (!informatika_libre || sekzio_balio < 1 || sekzio_balio > 518) return -19;
        int EMAITZA = eskaera(sekzio_balio, 0x30);
        if (EMAITZA < 0) return EMAITZA;
        for (int INDIZE = 0; INDIZE < 256; INDIZE++)
            gailu_balio.입출력짧은수쓰기(0x1f0, sekzio_datuak[INDIZE * 2] | sekzio_datuak[INDIZE * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informatika_libre) return -19;
        gailu_balio.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizatu_osoko_zenbaki(int Posizioa) {
        return sekzio_datuak[Posizioa] | sekzio_datuak[Posizioa + 1] << 8 | sekzio_datuak[Posizioa + 2] << 16 | sekzio_datuak[Posizioa + 3] << 24;
    }
    static void idatzi_osoko_zenbaki_balio(int Posizioa, int balio) {
        for (int INDIZE = 0; INDIZE < 4; INDIZE++) sekzio_datuak[Posizioa + INDIZE] = (balio >>> (INDIZE * 8)) & 255;
    }
}
