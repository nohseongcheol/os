// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int 칸 = 0;
    static int 색 = 7;

    static void Prepara() {
        dispositiu_VALOR.입출력바이트쓰기(0x3f9, 0);
        dispositiu_VALOR.입출력바이트쓰기(0x3fb, 0x80);
        dispositiu_VALOR.입출력바이트쓰기(0x3f8, 1);
        dispositiu_VALOR.입출력바이트쓰기(0x3f9, 0);
        dispositiu_VALOR.입출력바이트쓰기(0x3fb, 3);
        dispositiu_VALOR.입출력바이트쓰기(0x3fa, 0xc7);
        dispositiu_VALOR.입출력바이트쓰기(0x3fc, 0x0b);
        esborrar_introducció();
    }

    static void 직렬바이트(int VALOR) {
        int 횟수 = 100000;
        while ((dispositiu_VALOR.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) dispositiu_VALOR.입출력바이트쓰기(0x3f8, VALOR);
    }

    static void esborrar_introducció() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            dispositiu_VALOR.escriure_Memòria(0xb8000 + INDEX * 2, 32);
            dispositiu_VALOR.escriure_Memòria(0xb8001 + INDEX * 2, 색);
        }
        칸 = 0;
        cursor_VALOR();
    }

    static void cursor_VALOR() {
        dispositiu_VALOR.입출력바이트쓰기(0x3d4, 14);
        dispositiu_VALOR.입출력바이트쓰기(0x3d5, 칸 >> 8);
        dispositiu_VALOR.입출력바이트쓰기(0x3d4, 15);
        dispositiu_VALOR.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int VALOR) {
        if (VALOR == 13) return;
        if (VALOR == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (VALOR == 8) {
            if (칸 > 0) {
                칸--;
                dispositiu_VALOR.escriure_Memòria(0xb8000 + 칸 * 2, 32);
            }
        } else {
            dispositiu_VALOR.escriure_Memòria(0xb8000 + 칸 * 2, VALOR < 128 ? VALOR : '?');
            dispositiu_VALOR.escriure_Memòria(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                dispositiu_VALOR.escriure_Memòria(0xb8000 + INDEX, dispositiu_VALOR.tancar_Memòria(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                dispositiu_VALOR.escriure_Memòria(0xb8000 + INDEX * 2, 32);
                dispositiu_VALOR.escriure_Memòria(0xb8001 + INDEX * 2, 색);
            }
            칸 = 1920;
        }
        cursor_VALOR();
    }

    static void 문자(int VALOR) {
        if (VALOR < 128) {
            if (VALOR == 10) 직렬바이트(13);
            직렬바이트(VALOR);
        } else if (VALOR < 2048) {
            직렬바이트(0xc0 | (VALOR >> 6));
            직렬바이트(0x80 | (VALOR & 63));
        } else {
            직렬바이트(0xe0 | (VALOR >> 12));
            직렬바이트(0x80 | ((VALOR >> 6) & 63));
            직렬바이트(0x80 | (VALOR & 63));
        }
        화면문자(VALOR);
    }

    static void Escriptura(String contingut_VALOR) {
        for (int INDEX = 0; INDEX < contingut_VALOR.length(); INDEX++) 문자(contingut_VALOR.charAt(INDEX));
    }

    static void 수쓰기(int VALOR) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALOR < 0) 문자('-');
        else VALOR = -VALOR;
        int càrrec_INDEX = 1000000000;
        boolean Executa_2 = false;
        while (càrrec_INDEX > 0) {
            int dígit_VALOR = -(VALOR / càrrec_INDEX);
            if (dígit_VALOR != 0 || Executa_2 || càrrec_INDEX == 1) {
                문자('0' + dígit_VALOR);
                Executa_2 = true;
            }
            VALOR %= càrrec_INDEX;
            càrrec_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((dispositiu_VALOR.입출력바이트읽기(0x3fd) & 1) != 0) return dispositiu_VALOR.입출력바이트읽기(0x3f8);
        return -1;
    }
}
