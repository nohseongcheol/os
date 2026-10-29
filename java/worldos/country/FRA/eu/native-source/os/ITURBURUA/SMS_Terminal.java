// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int 칸 = 0;
    static int 색 = 7;

    static void 준비() {
        gailu_balio.입출력바이트쓰기(0x3f9, 0);
        gailu_balio.입출력바이트쓰기(0x3fb, 0x80);
        gailu_balio.입출력바이트쓰기(0x3f8, 1);
        gailu_balio.입출력바이트쓰기(0x3f9, 0);
        gailu_balio.입출력바이트쓰기(0x3fb, 3);
        gailu_balio.입출력바이트쓰기(0x3fa, 0xc7);
        gailu_balio.입출력바이트쓰기(0x3fc, 0x0b);
        ezabatu_sarrera();
    }

    static void 직렬바이트(int balio) {
        int 횟수 = 100000;
        while ((gailu_balio.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) gailu_balio.입출력바이트쓰기(0x3f8, balio);
    }

    static void ezabatu_sarrera() {
        for (int INDIZE = 0; INDIZE < 2000; INDIZE++) {
            gailu_balio.idatzi_Memoria(0xb8000 + INDIZE * 2, 32);
            gailu_balio.idatzi_Memoria(0xb8001 + INDIZE * 2, 색);
        }
        칸 = 0;
        kurtsore_balio();
    }

    static void kurtsore_balio() {
        gailu_balio.입출력바이트쓰기(0x3d4, 14);
        gailu_balio.입출력바이트쓰기(0x3d5, 칸 >> 8);
        gailu_balio.입출력바이트쓰기(0x3d4, 15);
        gailu_balio.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int balio) {
        if (balio == 13) return;
        if (balio == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (balio == 8) {
            if (칸 > 0) {
                칸--;
                gailu_balio.idatzi_Memoria(0xb8000 + 칸 * 2, 32);
            }
        } else {
            gailu_balio.idatzi_Memoria(0xb8000 + 칸 * 2, balio < 128 ? balio : '?');
            gailu_balio.idatzi_Memoria(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int INDIZE = 0; INDIZE < 3840; INDIZE++)
                gailu_balio.idatzi_Memoria(0xb8000 + INDIZE, gailu_balio.기억읽기(0xb80a0 + INDIZE));
            for (int INDIZE = 1920; INDIZE < 2000; INDIZE++) {
                gailu_balio.idatzi_Memoria(0xb8000 + INDIZE * 2, 32);
                gailu_balio.idatzi_Memoria(0xb8001 + INDIZE * 2, 색);
            }
            칸 = 1920;
        }
        kurtsore_balio();
    }

    static void 문자(int balio) {
        if (balio < 128) {
            if (balio == 10) 직렬바이트(13);
            직렬바이트(balio);
        } else if (balio < 2048) {
            직렬바이트(0xc0 | (balio >> 6));
            직렬바이트(0x80 | (balio & 63));
        } else {
            직렬바이트(0xe0 | (balio >> 12));
            직렬바이트(0x80 | ((balio >> 6) & 63));
            직렬바이트(0x80 | (balio & 63));
        }
        화면문자(balio);
    }

    static void Idatzi(String eduki_balio) {
        for (int INDIZE = 0; INDIZE < eduki_balio.length(); INDIZE++) 문자(eduki_balio.charAt(INDIZE));
    }

    static void 수쓰기(int balio) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (balio < 0) 문자('-');
        else balio = -balio;
        int kargu_INDIZE = 1000000000;
        boolean Exekutatu_2 = false;
        while (kargu_INDIZE > 0) {
            int digitu_balio = -(balio / kargu_INDIZE);
            if (digitu_balio != 0 || Exekutatu_2 || kargu_INDIZE == 1) {
                문자('0' + digitu_balio);
                Exekutatu_2 = true;
            }
            balio %= kargu_INDIZE;
            kargu_INDIZE /= 10;
        }
    }

    static int 직렬읽기() {
        if ((gailu_balio.입출력바이트읽기(0x3fd) & 1) != 0) return gailu_balio.입출력바이트읽기(0x3f8);
        return -1;
    }
}
