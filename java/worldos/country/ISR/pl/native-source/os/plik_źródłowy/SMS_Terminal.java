// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int gniazdo_wpis = 0;
    static int 색 = 7;

    static void Przygotuj() {
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3f9, 0);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3fb, 0x80);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3f8, 1);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3f9, 0);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3fb, 3);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3fa, 0xc7);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3fc, 0x0b);
        usunąć_wpis();
    }

    static void 직렬바이트(int WARTOŚĆ) {
        int powtórzenie_ILE_LICZB = 100000;
        while ((urządzenie_WARTOŚĆ.입출력바이트읽기(0x3fd) & 0x20) == 0 && powtórzenie_ILE_LICZB > 0) powtórzenie_ILE_LICZB--;
        if (powtórzenie_ILE_LICZB > 0) urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3f8, WARTOŚĆ);
    }

    static void usunąć_wpis() {
        for (int INDEKS = 0; INDEKS < 2000; INDEKS++) {
            urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8000 + INDEKS * 2, 32);
            urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8001 + INDEKS * 2, 색);
        }
        gniazdo_wpis = 0;
        kursor_WARTOŚĆ();
    }

    static void kursor_WARTOŚĆ() {
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3d4, 14);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3d5, gniazdo_wpis >> 8);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3d4, 15);
        urządzenie_WARTOŚĆ.입출력바이트쓰기(0x3d5, gniazdo_wpis & 255);
    }

    static void 화면문자(int WARTOŚĆ) {
        if (WARTOŚĆ == 13) return;
        if (WARTOŚĆ == 10) {
            gniazdo_wpis = (gniazdo_wpis / 80 + 1) * 80;
        } else if (WARTOŚĆ == 8) {
            if (gniazdo_wpis > 0) {
                gniazdo_wpis--;
                urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8000 + gniazdo_wpis * 2, 32);
            }
        } else {
            urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8000 + gniazdo_wpis * 2, WARTOŚĆ < 128 ? WARTOŚĆ : '?');
            urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8001 + gniazdo_wpis * 2, 색);
            gniazdo_wpis++;
        }
        if (gniazdo_wpis >= 2000) {
            for (int INDEKS = 0; INDEKS < 3840; INDEKS++)
                urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8000 + INDEKS, urządzenie_WARTOŚĆ.기억읽기(0xb80a0 + INDEKS));
            for (int INDEKS = 1920; INDEKS < 2000; INDEKS++) {
                urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8000 + INDEKS * 2, 32);
                urządzenie_WARTOŚĆ.zapis_Pamięć(0xb8001 + INDEKS * 2, 색);
            }
            gniazdo_wpis = 1920;
        }
        kursor_WARTOŚĆ();
    }

    static void 문자(int WARTOŚĆ) {
        if (WARTOŚĆ < 128) {
            if (WARTOŚĆ == 10) 직렬바이트(13);
            직렬바이트(WARTOŚĆ);
        } else if (WARTOŚĆ < 2048) {
            직렬바이트(0xc0 | (WARTOŚĆ >> 6));
            직렬바이트(0x80 | (WARTOŚĆ & 63));
        } else {
            직렬바이트(0xe0 | (WARTOŚĆ >> 12));
            직렬바이트(0x80 | ((WARTOŚĆ >> 6) & 63));
            직렬바이트(0x80 | (WARTOŚĆ & 63));
        }
        화면문자(WARTOŚĆ);
    }

    static void Zapis(String treść_WARTOŚĆ_cb0f2404) {
        for (int INDEKS = 0; INDEKS < treść_WARTOŚĆ_cb0f2404.length(); INDEKS++) 문자(treść_WARTOŚĆ_cb0f2404.charAt(INDEKS));
    }

    static void zapis_identyfikator(int WARTOŚĆ) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (WARTOŚĆ < 0) 문자('-');
        else WARTOŚĆ = -WARTOŚĆ;
        int indeks_pozycji = 1000000000;
        boolean Uruchom_2 = false;
        while (indeks_pozycji > 0) {
            int cyfra_WARTOŚĆ = -(WARTOŚĆ / indeks_pozycji);
            if (cyfra_WARTOŚĆ != 0 || Uruchom_2 || indeks_pozycji == 1) {
                문자('0' + cyfra_WARTOŚĆ);
                Uruchom_2 = true;
            }
            WARTOŚĆ %= indeks_pozycji;
            indeks_pozycji /= 10;
        }
    }

    static int 직렬읽기() {
        if ((urządzenie_WARTOŚĆ.입출력바이트읽기(0x3fd) & 1) != 0) return urządzenie_WARTOŚĆ.입출력바이트읽기(0x3f8);
        return -1;
    }
}
