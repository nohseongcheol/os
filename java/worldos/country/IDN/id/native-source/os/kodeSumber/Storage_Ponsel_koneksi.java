// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 seksi_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Storage_Ponsel_koneksi {
    static boolean teknologi_informasi_Aktif_9e72441a = false;
    static int[] seksi_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) Ponsel_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int jalankan = Ponsel_VALUE.밀리초();
        while (Ponsel_VALUE.밀리초() - jalankan < 500) {
            int Status_VALUE = Ponsel_VALUE.입출력바이트읽기(0x1f7);
            if (Status_VALUE == 0 || Status_VALUE == 255) return -19;
            if ((Status_VALUE & 128) == 0) {
                if ((Status_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Status_VALUE & 8) != 0) return 0;
            }
            Ponsel_VALUE.잠시양보();
        }
        return -110;
    }
    static int permintaan(int seksi_VALUE, int perintah) {
        if (seksi_VALUE < 0 || seksi_VALUE >= 2048) return -22;
        Ponsel_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ gunakan_VALUE 안 함
        Ponsel_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int hasil = 준비기다리기(false);
        if (hasil < 0) return hasil;
        Ponsel_VALUE.입출력바이트쓰기(0x1f2, 1);
        Ponsel_VALUE.입출력바이트쓰기(0x1f3, seksi_VALUE & 255);
        Ponsel_VALUE.입출력바이트쓰기(0x1f4, (seksi_VALUE >>> 8) & 255);
        Ponsel_VALUE.입출력바이트쓰기(0x1f5, 0);
        Ponsel_VALUE.입출력바이트쓰기(0x1f7, perintah); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Baca(int seksi_VALUE) {
        int hasil = permintaan(seksi_VALUE, 0x20);
        if (hasil < 0) return hasil;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = Ponsel_VALUE.입출력짧은수읽기(0x1f0);
            seksi_data[INDEX * 2] = VALUE & 255; seksi_data[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Tulis(int seksi_VALUE) {
        if (!teknologi_informasi_Aktif_9e72441a || seksi_VALUE < 1 || seksi_VALUE > 518) return -19;
        int hasil = permintaan(seksi_VALUE, 0x30);
        if (hasil < 0) return hasil;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            Ponsel_VALUE.입출력짧은수쓰기(0x1f0, seksi_data[INDEX * 2] | seksi_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!teknologi_informasi_Aktif_9e72441a) return -19;
        Ponsel_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int urai_bilangan_bulat(int posisi) {
        return seksi_data[posisi] | seksi_data[posisi + 1] << 8 | seksi_data[posisi + 2] << 16 | seksi_data[posisi + 3] << 24;
    }
    static void tulis_bilangan_bulat_VALUE(int posisi, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) seksi_data[posisi + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
