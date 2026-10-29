// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int 칸 = 0;
    static int 색 = 7;

    static void Sediakan() {
        peranti_VALUE.입출력바이트쓰기(0x3f9, 0);
        peranti_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        peranti_VALUE.입출력바이트쓰기(0x3f8, 1);
        peranti_VALUE.입출력바이트쓰기(0x3f9, 0);
        peranti_VALUE.입출력바이트쓰기(0x3fb, 3);
        peranti_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        peranti_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        padam_pemasukan();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((peranti_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) peranti_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void padam_pemasukan() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            peranti_VALUE.tulis_Memori(0xb8000 + INDEX * 2, 32);
            peranti_VALUE.tulis_Memori(0xb8001 + INDEX * 2, 색);
        }
        칸 = 0;
        kursor_VALUE();
    }

    static void kursor_VALUE() {
        peranti_VALUE.입출력바이트쓰기(0x3d4, 14);
        peranti_VALUE.입출력바이트쓰기(0x3d5, 칸 >> 8);
        peranti_VALUE.입출력바이트쓰기(0x3d4, 15);
        peranti_VALUE.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (칸 > 0) {
                칸--;
                peranti_VALUE.tulis_Memori(0xb8000 + 칸 * 2, 32);
            }
        } else {
            peranti_VALUE.tulis_Memori(0xb8000 + 칸 * 2, VALUE < 128 ? VALUE : '?');
            peranti_VALUE.tulis_Memori(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                peranti_VALUE.tulis_Memori(0xb8000 + INDEX, peranti_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                peranti_VALUE.tulis_Memori(0xb8000 + INDEX * 2, 32);
                peranti_VALUE.tulis_Memori(0xb8001 + INDEX * 2, 색);
            }
            칸 = 1920;
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

    static void Tulis(String Kandungan_VALUE) {
        for (int INDEX = 0; INDEX < Kandungan_VALUE.length(); INDEX++) 문자(Kandungan_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int jawatan_INDEX = 1000000000;
        boolean Jalan = false;
        while (jawatan_INDEX > 0) {
            int digit_VALUE = -(VALUE / jawatan_INDEX);
            if (digit_VALUE != 0 || Jalan || jawatan_INDEX == 1) {
                문자('0' + digit_VALUE);
                Jalan = true;
            }
            VALUE %= jawatan_INDEX;
            jawatan_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((peranti_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return peranti_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
