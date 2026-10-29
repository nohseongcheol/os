// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 igice_agaciro. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Ububiko_igendanwa_kwihuza {
    static boolean 사용가능 = false;
    static int[] igice_amakurushingiro = new int[512];
    static void 잠깐기다리기() {
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) igendanwa_agaciro.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int ihuriro = igendanwa_agaciro.밀리초();
        while (igendanwa_agaciro.밀리초() - ihuriro < 500) {
            int imimerere_agaciro = igendanwa_agaciro.입출력바이트읽기(0x1f7);
            if (imimerere_agaciro == 0 || imimerere_agaciro == 255) return -19;
            if ((imimerere_agaciro & 128) == 0) {
                if ((imimerere_agaciro & 33) != 0) return -5;
                if (!자료필요 || (imimerere_agaciro & 8) != 0) return 0;
            }
            igendanwa_agaciro.잠시양보();
        }
        return -110;
    }
    static int 요청(int igice_agaciro, int Icyo_wifuza) {
        if (igice_agaciro < 0 || igice_agaciro >= 2048) return -22;
        igendanwa_agaciro.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        igendanwa_agaciro.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int 결과 = 준비기다리기(false);
        if (결과 < 0) return 결과;
        igendanwa_agaciro.입출력바이트쓰기(0x1f2, 1);
        igendanwa_agaciro.입출력바이트쓰기(0x1f3, igice_agaciro & 255);
        igendanwa_agaciro.입출력바이트쓰기(0x1f4, (igice_agaciro >>> 8) & 255);
        igendanwa_agaciro.입출력바이트쓰기(0x1f5, 0);
        igendanwa_agaciro.입출력바이트쓰기(0x1f7, Icyo_wifuza); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int igice_agaciro) {
        int 결과 = 요청(igice_agaciro, 0x20);
        if (결과 < 0) return 결과;
        for (int umugerekashakiro = 0; umugerekashakiro < 256; umugerekashakiro++) {
            int agaciro = igendanwa_agaciro.입출력짧은수읽기(0x1f0);
            igice_amakurushingiro[umugerekashakiro * 2] = agaciro & 255; igice_amakurushingiro[umugerekashakiro * 2 + 1] = agaciro >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int kwandika(int igice_agaciro) {
        if (!사용가능 || igice_agaciro < 1 || igice_agaciro > 518) return -19;
        int 결과 = 요청(igice_agaciro, 0x30);
        if (결과 < 0) return 결과;
        for (int umugerekashakiro = 0; umugerekashakiro < 256; umugerekashakiro++)
            igendanwa_agaciro.입출력짧은수쓰기(0x1f0, igice_amakurushingiro[umugerekashakiro * 2] | igice_amakurushingiro[umugerekashakiro * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        igendanwa_agaciro.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int gusesengura_umubare_wuzuye(int 위치) {
        return igice_amakurushingiro[위치] | igice_amakurushingiro[위치 + 1] << 8 | igice_amakurushingiro[위치 + 2] << 16 | igice_amakurushingiro[위치 + 3] << 24;
    }
    static void kwandika_umubare_wuzuye_agaciro(int 위치, int agaciro) {
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) igice_amakurushingiro[위치 + umugerekashakiro] = (agaciro >>> (umugerekashakiro * 8)) & 255;
    }
}
