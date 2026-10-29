// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int sebaka_tsenyo = 0;
    static int 색 = 7;

    static void Baakanya() {
        mobaele_Boleng.입출력바이트쓰기(0x3f9, 0);
        mobaele_Boleng.입출력바이트쓰기(0x3fb, 0x80);
        mobaele_Boleng.입출력바이트쓰기(0x3f8, 1);
        mobaele_Boleng.입출력바이트쓰기(0x3f9, 0);
        mobaele_Boleng.입출력바이트쓰기(0x3fb, 3);
        mobaele_Boleng.입출력바이트쓰기(0x3fa, 0xc7);
        mobaele_Boleng.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int Boleng) {
        int 횟수 = 100000;
        while ((mobaele_Boleng.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) mobaele_Boleng.입출력바이트쓰기(0x3f8, Boleng);
    }

    static void 지우기() {
        for (int tshupane = 0; tshupane < 2000; tshupane++) {
            mobaele_Boleng.kwala_memori(0xb8000 + tshupane * 2, 32);
            mobaele_Boleng.kwala_memori(0xb8001 + tshupane * 2, 색);
        }
        sebaka_tsenyo = 0;
        khesara_Boleng();
    }

    static void khesara_Boleng() {
        mobaele_Boleng.입출력바이트쓰기(0x3d4, 14);
        mobaele_Boleng.입출력바이트쓰기(0x3d5, sebaka_tsenyo >> 8);
        mobaele_Boleng.입출력바이트쓰기(0x3d4, 15);
        mobaele_Boleng.입출력바이트쓰기(0x3d5, sebaka_tsenyo & 255);
    }

    static void 화면문자(int Boleng) {
        if (Boleng == 13) return;
        if (Boleng == 10) {
            sebaka_tsenyo = (sebaka_tsenyo / 80 + 1) * 80;
        } else if (Boleng == 8) {
            if (sebaka_tsenyo > 0) {
                sebaka_tsenyo--;
                mobaele_Boleng.kwala_memori(0xb8000 + sebaka_tsenyo * 2, 32);
            }
        } else {
            mobaele_Boleng.kwala_memori(0xb8000 + sebaka_tsenyo * 2, Boleng < 128 ? Boleng : '?');
            mobaele_Boleng.kwala_memori(0xb8001 + sebaka_tsenyo * 2, 색);
            sebaka_tsenyo++;
        }
        if (sebaka_tsenyo >= 2000) {
            for (int tshupane = 0; tshupane < 3840; tshupane++)
                mobaele_Boleng.kwala_memori(0xb8000 + tshupane, mobaele_Boleng.기억읽기(0xb80a0 + tshupane));
            for (int tshupane = 1920; tshupane < 2000; tshupane++) {
                mobaele_Boleng.kwala_memori(0xb8000 + tshupane * 2, 32);
                mobaele_Boleng.kwala_memori(0xb8001 + tshupane * 2, 색);
            }
            sebaka_tsenyo = 1920;
        }
        khesara_Boleng();
    }

    static void 문자(int Boleng) {
        if (Boleng < 128) {
            if (Boleng == 10) 직렬바이트(13);
            직렬바이트(Boleng);
        } else if (Boleng < 2048) {
            직렬바이트(0xc0 | (Boleng >> 6));
            직렬바이트(0x80 | (Boleng & 63));
        } else {
            직렬바이트(0xe0 | (Boleng >> 12));
            직렬바이트(0x80 | ((Boleng >> 6) & 63));
            직렬바이트(0x80 | (Boleng & 63));
        }
        화면문자(Boleng);
    }

    static void kwala(String Diteng_Boleng) {
        for (int tshupane = 0; tshupane < Diteng_Boleng.length(); tshupane++) 문자(Diteng_Boleng.charAt(tshupane));
    }

    static void 수쓰기(int Boleng) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (Boleng < 0) 문자('-');
        else Boleng = -Boleng;
        int 자리 = 1000000000;
        boolean dirisa = false;
        while (자리 > 0) {
            int dijite_Boleng = -(Boleng / 자리);
            if (dijite_Boleng != 0 || dirisa || 자리 == 1) {
                문자('0' + dijite_Boleng);
                dirisa = true;
            }
            Boleng %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((mobaele_Boleng.입출력바이트읽기(0x3fd) & 1) != 0) return mobaele_Boleng.입출력바이트읽기(0x3f8);
        return -1;
    }
}
