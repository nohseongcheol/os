// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminaal {
    static int gleuf_inskrywing = 0;
    static int 색 = 7;

    static void Maak_gereed() {
        mobiel_VALUE.입출력바이트쓰기(0x3f9, 0);
        mobiel_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        mobiel_VALUE.입출력바이트쓰기(0x3f8, 1);
        mobiel_VALUE.입출력바이트쓰기(0x3f9, 0);
        mobiel_VALUE.입출력바이트쓰기(0x3fb, 3);
        mobiel_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        mobiel_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        vee_uit_inskrywing();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((mobiel_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) mobiel_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void vee_uit_inskrywing() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            mobiel_VALUE.skryf_Geheue(0xb8000 + INDEX * 2, 32);
            mobiel_VALUE.skryf_Geheue(0xb8001 + INDEX * 2, 색);
        }
        gleuf_inskrywing = 0;
        loper_VALUE();
    }

    static void loper_VALUE() {
        mobiel_VALUE.입출력바이트쓰기(0x3d4, 14);
        mobiel_VALUE.입출력바이트쓰기(0x3d5, gleuf_inskrywing >> 8);
        mobiel_VALUE.입출력바이트쓰기(0x3d4, 15);
        mobiel_VALUE.입출력바이트쓰기(0x3d5, gleuf_inskrywing & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            gleuf_inskrywing = (gleuf_inskrywing / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (gleuf_inskrywing > 0) {
                gleuf_inskrywing--;
                mobiel_VALUE.skryf_Geheue(0xb8000 + gleuf_inskrywing * 2, 32);
            }
        } else {
            mobiel_VALUE.skryf_Geheue(0xb8000 + gleuf_inskrywing * 2, VALUE < 128 ? VALUE : '?');
            mobiel_VALUE.skryf_Geheue(0xb8001 + gleuf_inskrywing * 2, 색);
            gleuf_inskrywing++;
        }
        if (gleuf_inskrywing >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                mobiel_VALUE.skryf_Geheue(0xb8000 + INDEX, mobiel_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                mobiel_VALUE.skryf_Geheue(0xb8000 + INDEX * 2, 32);
                mobiel_VALUE.skryf_Geheue(0xb8001 + INDEX * 2, 색);
            }
            gleuf_inskrywing = 1920;
        }
        loper_VALUE();
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

    static void Skryf(String Inhoud_VALUE) {
        for (int INDEX = 0; INDEX < Inhoud_VALUE.length(); INDEX++) 문자(Inhoud_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int plaas_INDEX = 1000000000;
        boolean Loop = false;
        while (plaas_INDEX > 0) {
            int syfer_VALUE = -(VALUE / plaas_INDEX);
            if (syfer_VALUE != 0 || Loop || plaas_INDEX == 1) {
                문자('0' + syfer_VALUE);
                Loop = true;
            }
            VALUE %= plaas_INDEX;
            plaas_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((mobiel_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return mobiel_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
