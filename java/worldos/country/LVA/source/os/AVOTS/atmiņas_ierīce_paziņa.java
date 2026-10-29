// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sadaļa_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class atmiņas_ierīce_paziņa {
    static boolean informācijas_tehnoloģija_Aktīvs_9e72441a = false;
    static int[] sadaļa_dati = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) ierīce_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Palaist = ierīce_VALUE.밀리초();
        while (ierīce_VALUE.밀리초() - Palaist < 500) {
            int Statuss_VALUE = ierīce_VALUE.입출력바이트읽기(0x1f7);
            if (Statuss_VALUE == 0 || Statuss_VALUE == 255) return -19;
            if ((Statuss_VALUE & 128) == 0) {
                if ((Statuss_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Statuss_VALUE & 8) != 0) return 0;
            }
            ierīce_VALUE.잠시양보();
        }
        return -110;
    }
    static int pieprasījums(int sadaļa_VALUE, int Komanda) {
        if (sadaļa_VALUE < 0 || sadaļa_VALUE >= 2048) return -22;
        ierīce_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ lietot_VALUE 안 함
        ierīce_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int mērs = 준비기다리기(false);
        if (mērs < 0) return mērs;
        ierīce_VALUE.입출력바이트쓰기(0x1f2, 1);
        ierīce_VALUE.입출력바이트쓰기(0x1f3, sadaļa_VALUE & 255);
        ierīce_VALUE.입출력바이트쓰기(0x1f4, (sadaļa_VALUE >>> 8) & 255);
        ierīce_VALUE.입출력바이트쓰기(0x1f5, 0);
        ierīce_VALUE.입출력바이트쓰기(0x1f7, Komanda); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Lasīt(int sadaļa_VALUE) {
        int mērs = pieprasījums(sadaļa_VALUE, 0x20);
        if (mērs < 0) return mērs;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = ierīce_VALUE.입출력짧은수읽기(0x1f0);
            sadaļa_dati[INDEX * 2] = VALUE & 255; sadaļa_dati[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Rakstīt(int sadaļa_VALUE) {
        if (!informācijas_tehnoloģija_Aktīvs_9e72441a || sadaļa_VALUE < 1 || sadaļa_VALUE > 518) return -19;
        int mērs = pieprasījums(sadaļa_VALUE, 0x30);
        if (mērs < 0) return mērs;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            ierīce_VALUE.입출력짧은수쓰기(0x1f0, sadaļa_dati[INDEX * 2] | sadaļa_dati[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informācijas_tehnoloģija_Aktīvs_9e72441a) return -19;
        ierīce_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int parsēt_vesels_skaitlis(int Novietojums) {
        return sadaļa_dati[Novietojums] | sadaļa_dati[Novietojums + 1] << 8 | sadaļa_dati[Novietojums + 2] << 16 | sadaļa_dati[Novietojums + 3] << 24;
    }
    static void rakstīšana_vesels_skaitlis_VALUE(int Novietojums, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) sadaļa_dati[Novietojums + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
