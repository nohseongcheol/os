// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int sekgobana_go_tsenya_tshedimošo = 0;
    static int 색 = 7;

    static void Lokišetša() {
        sedirišwa_boleng.입출력바이트쓰기(0x3f9, 0);
        sedirišwa_boleng.입출력바이트쓰기(0x3fb, 0x80);
        sedirišwa_boleng.입출력바이트쓰기(0x3f8, 1);
        sedirišwa_boleng.입출력바이트쓰기(0x3f9, 0);
        sedirišwa_boleng.입출력바이트쓰기(0x3fb, 3);
        sedirišwa_boleng.입출력바이트쓰기(0x3fa, 0xc7);
        sedirišwa_boleng.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int boleng) {
        int 횟수 = 100000;
        while ((sedirišwa_boleng.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) sedirišwa_boleng.입출력바이트쓰기(0x3f8, boleng);
    }

    static void 지우기() {
        for (int lokela = 0; lokela < 2000; lokela++) {
            sedirišwa_boleng.ngwala_memori(0xb8000 + lokela * 2, 32);
            sedirišwa_boleng.ngwala_memori(0xb8001 + lokela * 2, 색);
        }
        sekgobana_go_tsenya_tshedimošo = 0;
        kheusa_boleng();
    }

    static void kheusa_boleng() {
        sedirišwa_boleng.입출력바이트쓰기(0x3d4, 14);
        sedirišwa_boleng.입출력바이트쓰기(0x3d5, sekgobana_go_tsenya_tshedimošo >> 8);
        sedirišwa_boleng.입출력바이트쓰기(0x3d4, 15);
        sedirišwa_boleng.입출력바이트쓰기(0x3d5, sekgobana_go_tsenya_tshedimošo & 255);
    }

    static void 화면문자(int boleng) {
        if (boleng == 13) return;
        if (boleng == 10) {
            sekgobana_go_tsenya_tshedimošo = (sekgobana_go_tsenya_tshedimošo / 80 + 1) * 80;
        } else if (boleng == 8) {
            if (sekgobana_go_tsenya_tshedimošo > 0) {
                sekgobana_go_tsenya_tshedimošo--;
                sedirišwa_boleng.ngwala_memori(0xb8000 + sekgobana_go_tsenya_tshedimošo * 2, 32);
            }
        } else {
            sedirišwa_boleng.ngwala_memori(0xb8000 + sekgobana_go_tsenya_tshedimošo * 2, boleng < 128 ? boleng : '?');
            sedirišwa_boleng.ngwala_memori(0xb8001 + sekgobana_go_tsenya_tshedimošo * 2, 색);
            sekgobana_go_tsenya_tshedimošo++;
        }
        if (sekgobana_go_tsenya_tshedimošo >= 2000) {
            for (int lokela = 0; lokela < 3840; lokela++)
                sedirišwa_boleng.ngwala_memori(0xb8000 + lokela, sedirišwa_boleng.기억읽기(0xb80a0 + lokela));
            for (int lokela = 1920; lokela < 2000; lokela++) {
                sedirišwa_boleng.ngwala_memori(0xb8000 + lokela * 2, 32);
                sedirišwa_boleng.ngwala_memori(0xb8001 + lokela * 2, 색);
            }
            sekgobana_go_tsenya_tshedimošo = 1920;
        }
        kheusa_boleng();
    }

    static void 문자(int boleng) {
        if (boleng < 128) {
            if (boleng == 10) 직렬바이트(13);
            직렬바이트(boleng);
        } else if (boleng < 2048) {
            직렬바이트(0xc0 | (boleng >> 6));
            직렬바이트(0x80 | (boleng & 63));
        } else {
            직렬바이트(0xe0 | (boleng >> 12));
            직렬바이트(0x80 | ((boleng >> 6) & 63));
            직렬바이트(0x80 | (boleng & 63));
        }
        화면문자(boleng);
    }

    static void Ngwala(String Diteng_boleng) {
        for (int lokela = 0; lokela < Diteng_boleng.length(); lokela++) 문자(Diteng_boleng.charAt(lokela));
    }

    static void 수쓰기(int boleng) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (boleng < 0) 문자('-');
        else boleng = -boleng;
        int 자리 = 1000000000;
        boolean Diriša = false;
        while (자리 > 0) {
            int 숫자 = -(boleng / 자리);
            if (숫자 != 0 || Diriša || 자리 == 1) {
                문자('0' + 숫자);
                Diriša = true;
            }
            boleng %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((sedirišwa_boleng.입출력바이트읽기(0x3fd) & 1) != 0) return sedirišwa_boleng.입출력바이트읽기(0x3f8);
        return -1;
    }
}
