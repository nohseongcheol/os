// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 scherm. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class sms_Terminal {
    static int sleuf_invoer = 0;
    static int 색 = 7;

    static void Bereid_voor() {
        mobiel_WAARDE.입출력바이트쓰기(0x3f9, 0);
        mobiel_WAARDE.입출력바이트쓰기(0x3fb, 0x80);
        mobiel_WAARDE.입출력바이트쓰기(0x3f8, 1);
        mobiel_WAARDE.입출력바이트쓰기(0x3f9, 0);
        mobiel_WAARDE.입출력바이트쓰기(0x3fb, 3);
        mobiel_WAARDE.입출력바이트쓰기(0x3fa, 0xc7);
        mobiel_WAARDE.입출력바이트쓰기(0x3fc, 0x0b);
        wissen_invoer();
    }

    static void 직렬바이트(int WAARDE) {
        int herhaling_AANTAL = 100000;
        while ((mobiel_WAARDE.입출력바이트읽기(0x3fd) & 0x20) == 0 && herhaling_AANTAL > 0) herhaling_AANTAL--;
        if (herhaling_AANTAL > 0) mobiel_WAARDE.입출력바이트쓰기(0x3f8, WAARDE);
    }

    static void wissen_invoer() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            mobiel_WAARDE.schrijven_Geheugen(0xb8000 + INDEX * 2, 32);
            mobiel_WAARDE.schrijven_Geheugen(0xb8001 + INDEX * 2, 색);
        }
        sleuf_invoer = 0;
        cursor_WAARDE();
    }

    static void cursor_WAARDE() {
        mobiel_WAARDE.입출력바이트쓰기(0x3d4, 14);
        mobiel_WAARDE.입출력바이트쓰기(0x3d5, sleuf_invoer >> 8);
        mobiel_WAARDE.입출력바이트쓰기(0x3d4, 15);
        mobiel_WAARDE.입출력바이트쓰기(0x3d5, sleuf_invoer & 255);
    }

    static void scherm_teken(int WAARDE) {
        if (WAARDE == 13) return;
        if (WAARDE == 10) {
            sleuf_invoer = (sleuf_invoer / 80 + 1) * 80;
        } else if (WAARDE == 8) {
            if (sleuf_invoer > 0) {
                sleuf_invoer--;
                mobiel_WAARDE.schrijven_Geheugen(0xb8000 + sleuf_invoer * 2, 32);
            }
        } else {
            mobiel_WAARDE.schrijven_Geheugen(0xb8000 + sleuf_invoer * 2, WAARDE < 128 ? WAARDE : '?');
            mobiel_WAARDE.schrijven_Geheugen(0xb8001 + sleuf_invoer * 2, 색);
            sleuf_invoer++;
        }
        if (sleuf_invoer >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                mobiel_WAARDE.schrijven_Geheugen(0xb8000 + INDEX, mobiel_WAARDE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                mobiel_WAARDE.schrijven_Geheugen(0xb8000 + INDEX * 2, 32);
                mobiel_WAARDE.schrijven_Geheugen(0xb8001 + INDEX * 2, 색);
            }
            sleuf_invoer = 1920;
        }
        cursor_WAARDE();
    }

    static void 문자(int WAARDE) {
        if (WAARDE < 128) {
            if (WAARDE == 10) 직렬바이트(13);
            직렬바이트(WAARDE);
        } else if (WAARDE < 2048) {
            직렬바이트(0xc0 | (WAARDE >> 6));
            직렬바이트(0x80 | (WAARDE & 63));
        } else {
            직렬바이트(0xe0 | (WAARDE >> 12));
            직렬바이트(0x80 | ((WAARDE >> 6) & 63));
            직렬바이트(0x80 | (WAARDE & 63));
        }
        scherm_teken(WAARDE);
    }

    static void Schrijven(String Inhoud_WAARDE) {
        for (int INDEX = 0; INDEX < Inhoud_WAARDE.length(); INDEX++) 문자(Inhoud_WAARDE.charAt(INDEX));
    }

    static void schrijven_nummer(int WAARDE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (WAARDE < 0) 문자('-');
        else WAARDE = -WAARDE;
        int plaatsingsindex = 1000000000;
        boolean starten = false;
        while (plaatsingsindex > 0) {
            int cijfer_WAARDE = -(WAARDE / plaatsingsindex);
            if (cijfer_WAARDE != 0 || starten || plaatsingsindex == 1) {
                문자('0' + cijfer_WAARDE);
                starten = true;
            }
            WAARDE %= plaatsingsindex;
            plaatsingsindex /= 10;
        }
    }

    static int 직렬읽기() {
        if ((mobiel_WAARDE.입출력바이트읽기(0x3fd) & 1) != 0) return mobiel_WAARDE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
