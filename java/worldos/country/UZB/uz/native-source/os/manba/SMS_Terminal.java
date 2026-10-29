// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int in_kiritish = 0;
    static int 색 = 7;

    static void Tayyorlamoq() {
        qurilma_VALUE.입출력바이트쓰기(0x3f9, 0);
        qurilma_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        qurilma_VALUE.입출력바이트쓰기(0x3f8, 1);
        qurilma_VALUE.입출력바이트쓰기(0x3f9, 0);
        qurilma_VALUE.입출력바이트쓰기(0x3fb, 3);
        qurilma_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        qurilma_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        tozalash_kiritish();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((qurilma_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) qurilma_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void tozalash_kiritish() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            qurilma_VALUE.yozmoq_Xotira(0xb8000 + INDEX * 2, 32);
            qurilma_VALUE.yozmoq_Xotira(0xb8001 + INDEX * 2, 색);
        }
        in_kiritish = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        qurilma_VALUE.입출력바이트쓰기(0x3d4, 14);
        qurilma_VALUE.입출력바이트쓰기(0x3d5, in_kiritish >> 8);
        qurilma_VALUE.입출력바이트쓰기(0x3d4, 15);
        qurilma_VALUE.입출력바이트쓰기(0x3d5, in_kiritish & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            in_kiritish = (in_kiritish / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (in_kiritish > 0) {
                in_kiritish--;
                qurilma_VALUE.yozmoq_Xotira(0xb8000 + in_kiritish * 2, 32);
            }
        } else {
            qurilma_VALUE.yozmoq_Xotira(0xb8000 + in_kiritish * 2, VALUE < 128 ? VALUE : '?');
            qurilma_VALUE.yozmoq_Xotira(0xb8001 + in_kiritish * 2, 색);
            in_kiritish++;
        }
        if (in_kiritish >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                qurilma_VALUE.yozmoq_Xotira(0xb8000 + INDEX, qurilma_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                qurilma_VALUE.yozmoq_Xotira(0xb8000 + INDEX * 2, 32);
                qurilma_VALUE.yozmoq_Xotira(0xb8001 + INDEX * 2, 색);
            }
            in_kiritish = 1920;
        }
        kursor_VALUE();
    }

    static void 문자(int VALUE) {
        if (VALUE < 128) {
            if (VALUE == 10) 직렬바이트(13);
            직렬바이트(VALUE);
        } else if (VALUE < 2048) {
            직렬바이트(0xc0 | (VALUE >> 6));
            직렬바이트(0x80 | (VALUE & 63));
        } else {
            직렬바이트(0xe0 | (VALUE >> 12));
            직렬바이트(0x80 | ((VALUE >> 6) & 63));
            직렬바이트(0x80 | (VALUE & 63));
        }
        화면문자(VALUE);
    }

    static void Yozish(String tarkib_VALUE) {
        for (int INDEX = 0; INDEX < tarkib_VALUE.length(); INDEX++) 문자(tarkib_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int holat_INDEX = 1000000000;
        boolean Bajarish = false;
        while (holat_INDEX > 0) {
            int raqam_VALUE = -(VALUE / holat_INDEX);
            if (raqam_VALUE != 0 || Bajarish || holat_INDEX == 1) {
                문자('0' + raqam_VALUE);
                Bajarish = true;
            }
            VALUE %= holat_INDEX;
            holat_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((qurilma_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return qurilma_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
