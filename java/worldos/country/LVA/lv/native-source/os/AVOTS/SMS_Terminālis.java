// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminālis {
    static int 칸 = 0;
    static int 색 = 7;

    static void Sagatavot() {
        ierīce_VALUE.입출력바이트쓰기(0x3f9, 0);
        ierīce_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        ierīce_VALUE.입출력바이트쓰기(0x3f8, 1);
        ierīce_VALUE.입출력바이트쓰기(0x3f9, 0);
        ierīce_VALUE.입출력바이트쓰기(0x3fb, 3);
        ierīce_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        ierīce_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        dzēst_ievade();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((ierīce_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) ierīce_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void dzēst_ievade() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            ierīce_VALUE.rakstīšana_atmiņa(0xb8000 + INDEX * 2, 32);
            ierīce_VALUE.rakstīšana_atmiņa(0xb8001 + INDEX * 2, 색);
        }
        칸 = 0;
        kursors_VALUE();
    }

    static void kursors_VALUE() {
        ierīce_VALUE.입출력바이트쓰기(0x3d4, 14);
        ierīce_VALUE.입출력바이트쓰기(0x3d5, 칸 >> 8);
        ierīce_VALUE.입출력바이트쓰기(0x3d4, 15);
        ierīce_VALUE.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (칸 > 0) {
                칸--;
                ierīce_VALUE.rakstīšana_atmiņa(0xb8000 + 칸 * 2, 32);
            }
        } else {
            ierīce_VALUE.rakstīšana_atmiņa(0xb8000 + 칸 * 2, VALUE < 128 ? VALUE : '?');
            ierīce_VALUE.rakstīšana_atmiņa(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                ierīce_VALUE.rakstīšana_atmiņa(0xb8000 + INDEX, ierīce_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                ierīce_VALUE.rakstīšana_atmiņa(0xb8000 + INDEX * 2, 32);
                ierīce_VALUE.rakstīšana_atmiņa(0xb8001 + INDEX * 2, 색);
            }
            칸 = 1920;
        }
        kursors_VALUE();
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

    static void Rakstīt(String Saturs_VALUE) {
        for (int INDEX = 0; INDEX < Saturs_VALUE.length(); INDEX++) 문자(Saturs_VALUE.charAt(INDEX));
    }

    static void rakstīšana_numurs(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int pozīcijas_indekss = 1000000000;
        boolean Palaist = false;
        while (pozīcijas_indekss > 0) {
            int cipars_VALUE = -(VALUE / pozīcijas_indekss);
            if (cipars_VALUE != 0 || Palaist || pozīcijas_indekss == 1) {
                문자('0' + cipars_VALUE);
                Palaist = true;
            }
            VALUE %= pozīcijas_indekss;
            pozīcijas_indekss /= 10;
        }
    }

    static int 직렬읽기() {
        if ((ierīce_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return ierīce_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
