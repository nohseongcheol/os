// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 bölmə_VALUE_366e0bfa. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Yaddaş_cihaz_qoşulma {
    static boolean 사용가능 = false;
    static int[] bölmə_verilənlər = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) cihaz_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int İcra_Et = cihaz_VALUE.밀리초();
        while (cihaz_VALUE.밀리초() - İcra_Et < 500) {
            int vəziyyət_VALUE = cihaz_VALUE.입출력바이트읽기(0x1f7);
            if (vəziyyət_VALUE == 0 || vəziyyət_VALUE == 255) return -19;
            if ((vəziyyət_VALUE & 128) == 0) {
                if ((vəziyyət_VALUE & 33) != 0) return -5;
                if (!자료필요 || (vəziyyət_VALUE & 8) != 0) return 0;
            }
            cihaz_VALUE.잠시양보();
        }
        return -110;
    }
    static int HTTP_sorğusu(int bölmə_VALUE_366e0bfa, int Əmr) {
        if (bölmə_VALUE_366e0bfa < 0 || bölmə_VALUE_366e0bfa >= 2048) return -22;
        cihaz_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        cihaz_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int ölçü = 준비기다리기(false);
        if (ölçü < 0) return ölçü;
        cihaz_VALUE.입출력바이트쓰기(0x1f2, 1);
        cihaz_VALUE.입출력바이트쓰기(0x1f3, bölmə_VALUE_366e0bfa & 255);
        cihaz_VALUE.입출력바이트쓰기(0x1f4, (bölmə_VALUE_366e0bfa >>> 8) & 255);
        cihaz_VALUE.입출력바이트쓰기(0x1f5, 0);
        cihaz_VALUE.입출력바이트쓰기(0x1f7, Əmr); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Oxuma(int bölmə_VALUE_366e0bfa) {
        int ölçü = HTTP_sorğusu(bölmə_VALUE_366e0bfa, 0x20);
        if (ölçü < 0) return ölçü;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = cihaz_VALUE.입출력짧은수읽기(0x1f0);
            bölmə_verilənlər[INDEX * 2] = VALUE & 255; bölmə_verilənlər[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Yazma(int bölmə_VALUE_366e0bfa) {
        if (!사용가능 || bölmə_VALUE_366e0bfa < 1 || bölmə_VALUE_366e0bfa > 518) return -19;
        int ölçü = HTTP_sorğusu(bölmə_VALUE_366e0bfa, 0x30);
        if (ölçü < 0) return ölçü;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            cihaz_VALUE.입출력짧은수쓰기(0x1f0, bölmə_verilənlər[INDEX * 2] | bölmə_verilənlər[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        cihaz_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int parselləmək_tam_ədəd(int yerinə_qoymaq) {
        return bölmə_verilənlər[yerinə_qoymaq] | bölmə_verilənlər[yerinə_qoymaq + 1] << 8 | bölmə_verilənlər[yerinə_qoymaq + 2] << 16 | bölmə_verilənlər[yerinə_qoymaq + 3] << 24;
    }
    static void yazmaq_tam_ədəd_VALUE(int yerinə_qoymaq, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) bölmə_verilənlər[yerinə_qoymaq + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
