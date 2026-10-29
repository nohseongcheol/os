// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 seksyen_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Storan_peranti_hubungan {
    static boolean teknologi_maklumat_Ada_9e72441a = false;
    static int[] seksyen_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) peranti_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Jalan = peranti_VALUE.밀리초();
        while (peranti_VALUE.밀리초() - Jalan < 500) {
            int status_VALUE = peranti_VALUE.입출력바이트읽기(0x1f7);
            if (status_VALUE == 0 || status_VALUE == 255) return -19;
            if ((status_VALUE & 128) == 0) {
                if ((status_VALUE & 33) != 0) return -5;
                if (!자료필요 || (status_VALUE & 8) != 0) return 0;
            }
            peranti_VALUE.잠시양보();
        }
        return -110;
    }
    static int permintaan(int seksyen_VALUE, int Perintah) {
        if (seksyen_VALUE < 0 || seksyen_VALUE >= 2048) return -22;
        peranti_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        peranti_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int ukuran = 준비기다리기(false);
        if (ukuran < 0) return ukuran;
        peranti_VALUE.입출력바이트쓰기(0x1f2, 1);
        peranti_VALUE.입출력바이트쓰기(0x1f3, seksyen_VALUE & 255);
        peranti_VALUE.입출력바이트쓰기(0x1f4, (seksyen_VALUE >>> 8) & 255);
        peranti_VALUE.입출력바이트쓰기(0x1f5, 0);
        peranti_VALUE.입출력바이트쓰기(0x1f7, Perintah); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Baca(int seksyen_VALUE) {
        int ukuran = permintaan(seksyen_VALUE, 0x20);
        if (ukuran < 0) return ukuran;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = peranti_VALUE.입출력짧은수읽기(0x1f0);
            seksyen_data[INDEX * 2] = VALUE & 255; seksyen_data[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Tulis(int seksyen_VALUE) {
        if (!teknologi_maklumat_Ada_9e72441a || seksyen_VALUE < 1 || seksyen_VALUE > 518) return -19;
        int ukuran = permintaan(seksyen_VALUE, 0x30);
        if (ukuran < 0) return ukuran;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            peranti_VALUE.입출력짧은수쓰기(0x1f0, seksyen_data[INDEX * 2] | seksyen_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!teknologi_maklumat_Ada_9e72441a) return -19;
        peranti_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int hurai_integer(int Kedudukan) {
        return seksyen_data[Kedudukan] | seksyen_data[Kedudukan + 1] << 8 | seksyen_data[Kedudukan + 2] << 16 | seksyen_data[Kedudukan + 3] << 24;
    }
    static void tulis_integer_VALUE(int Kedudukan, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) seksyen_data[Kedudukan + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
