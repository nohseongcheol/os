// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int 칸 = 0;
    static int 색 = 7;

    static void Parnalli() {
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3f9, 0);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3fb, 0x80);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3f8, 1);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3f9, 0);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3fb, 3);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3fa, 0xc7);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int atuutilik) {
        int 횟수 = 100000;
        while ((sunakkutaaq_atuutilik.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) sunakkutaaq_atuutilik.입출력바이트쓰기(0x3f8, atuutilik);
    }

    static void 지우기() {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < 2000; nalunaiqsimavik++) {
            sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8000 + nalunaiqsimavik * 2, 32);
            sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8001 + nalunaiqsimavik * 2, 색);
        }
        칸 = 0;
        pigiarut_atuutilik();
    }

    static void pigiarut_atuutilik() {
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3d4, 14);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3d5, 칸 >> 8);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3d4, 15);
        sunakkutaaq_atuutilik.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int atuutilik) {
        if (atuutilik == 13) return;
        if (atuutilik == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (atuutilik == 8) {
            if (칸 > 0) {
                칸--;
                sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8000 + 칸 * 2, 32);
            }
        } else {
            sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8000 + 칸 * 2, atuutilik < 128 ? atuutilik : '?');
            sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < 3840; nalunaiqsimavik++)
                sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8000 + nalunaiqsimavik, sunakkutaaq_atuutilik.기억읽기(0xb80a0 + nalunaiqsimavik));
            for (int nalunaiqsimavik = 1920; nalunaiqsimavik < 2000; nalunaiqsimavik++) {
                sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8000 + nalunaiqsimavik * 2, 32);
                sunakkutaaq_atuutilik.titiraq_puigujjaikkut(0xb8001 + nalunaiqsimavik * 2, 색);
            }
            칸 = 1920;
        }
        pigiarut_atuutilik();
    }

    static void 문자(int atuutilik) {
        if (atuutilik < 128) {
            if (atuutilik == 10) 직렬바이트(13);
            직렬바이트(atuutilik);
        } else if (atuutilik < 2048) {
            직렬바이트(0xc0 | (atuutilik >> 6));
            직렬바이트(0x80 | (atuutilik & 63));
        } else {
            직렬바이트(0xe0 | (atuutilik >> 12));
            직렬바이트(0x80 | ((atuutilik >> 6) & 63));
            직렬바이트(0x80 | (atuutilik & 63));
        }
        화면문자(atuutilik);
    }

    static void titiraq(String Ilulingit_atuutilik) {
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < Ilulingit_atuutilik.length(); nalunaiqsimavik++) 문자(Ilulingit_atuutilik.charAt(nalunaiqsimavik));
    }

    static void 수쓰기(int atuutilik) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (atuutilik < 0) 문자('-');
        else atuutilik = -atuutilik;
        int 자리 = 1000000000;
        boolean 시작 = false;
        while (자리 > 0) {
            int 숫자 = -(atuutilik / 자리);
            if (숫자 != 0 || 시작 || 자리 == 1) {
                문자('0' + 숫자);
                시작 = true;
            }
            atuutilik %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((sunakkutaaq_atuutilik.입출력바이트읽기(0x3fd) & 1) != 0) return sunakkutaaq_atuutilik.입출력바이트읽기(0x3f8);
        return -1;
    }
}
