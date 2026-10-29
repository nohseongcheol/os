// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminál {
    static int tárolóhely_bejegyzés = 0;
    static int 색 = 7;

    static void Előkészítés() {
        mobil_ÉRTÉK.입출력바이트쓰기(0x3f9, 0);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3fb, 0x80);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3f8, 1);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3f9, 0);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3fb, 3);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3fa, 0xc7);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3fc, 0x0b);
        töröl_bejegyzés();
    }

    static void 직렬바이트(int ÉRTÉK) {
        int 횟수 = 100000;
        while ((mobil_ÉRTÉK.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) mobil_ÉRTÉK.입출력바이트쓰기(0x3f8, ÉRTÉK);
    }

    static void töröl_bejegyzés() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            mobil_ÉRTÉK.ír_Memória(0xb8000 + INDEX * 2, 32);
            mobil_ÉRTÉK.ír_Memória(0xb8001 + INDEX * 2, 색);
        }
        tárolóhely_bejegyzés = 0;
        kurzor_ÉRTÉK();
    }

    static void kurzor_ÉRTÉK() {
        mobil_ÉRTÉK.입출력바이트쓰기(0x3d4, 14);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3d5, tárolóhely_bejegyzés >> 8);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3d4, 15);
        mobil_ÉRTÉK.입출력바이트쓰기(0x3d5, tárolóhely_bejegyzés & 255);
    }

    static void 화면문자(int ÉRTÉK) {
        if (ÉRTÉK == 13) return;
        if (ÉRTÉK == 10) {
            tárolóhely_bejegyzés = (tárolóhely_bejegyzés / 80 + 1) * 80;
        } else if (ÉRTÉK == 8) {
            if (tárolóhely_bejegyzés > 0) {
                tárolóhely_bejegyzés--;
                mobil_ÉRTÉK.ír_Memória(0xb8000 + tárolóhely_bejegyzés * 2, 32);
            }
        } else {
            mobil_ÉRTÉK.ír_Memória(0xb8000 + tárolóhely_bejegyzés * 2, ÉRTÉK < 128 ? ÉRTÉK : '?');
            mobil_ÉRTÉK.ír_Memória(0xb8001 + tárolóhely_bejegyzés * 2, 색);
            tárolóhely_bejegyzés++;
        }
        if (tárolóhely_bejegyzés >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                mobil_ÉRTÉK.ír_Memória(0xb8000 + INDEX, mobil_ÉRTÉK.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                mobil_ÉRTÉK.ír_Memória(0xb8000 + INDEX * 2, 32);
                mobil_ÉRTÉK.ír_Memória(0xb8001 + INDEX * 2, 색);
            }
            tárolóhely_bejegyzés = 1920;
        }
        kurzor_ÉRTÉK();
    }

    static void 문자(int ÉRTÉK) {
        if (ÉRTÉK < 128) {
            if (ÉRTÉK == 10) 직렬바이트(13);
            직렬바이트(ÉRTÉK);
        } else if (ÉRTÉK < 2048) {
            직렬바이트(0xc0 | (ÉRTÉK >> 6));
            직렬바이트(0x80 | (ÉRTÉK & 63));
        } else {
            직렬바이트(0xe0 | (ÉRTÉK >> 12));
            직렬바이트(0x80 | ((ÉRTÉK >> 6) & 63));
            직렬바이트(0x80 | (ÉRTÉK & 63));
        }
        화면문자(ÉRTÉK);
    }

    static void Írás(String Tartalom_ÉRTÉK) {
        for (int INDEX = 0; INDEX < Tartalom_ÉRTÉK.length(); INDEX++) 문자(Tartalom_ÉRTÉK.charAt(INDEX));
    }

    static void ír_szám(int ÉRTÉK) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (ÉRTÉK < 0) 문자('-');
        else ÉRTÉK = -ÉRTÉK;
        int helyzetindex = 1000000000;
        boolean Futtatás = false;
        while (helyzetindex > 0) {
            int számjegy_ÉRTÉK = -(ÉRTÉK / helyzetindex);
            if (számjegy_ÉRTÉK != 0 || Futtatás || helyzetindex == 1) {
                문자('0' + számjegy_ÉRTÉK);
                Futtatás = true;
            }
            ÉRTÉK %= helyzetindex;
            helyzetindex /= 10;
        }
    }

    static int 직렬읽기() {
        if ((mobil_ÉRTÉK.입출력바이트읽기(0x3fd) & 1) != 0) return mobil_ÉRTÉK.입출력바이트읽기(0x3f8);
        return -1;
    }
}
