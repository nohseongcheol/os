// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int 칸 = 0;
    static int 색 = 7;

    static void 준비() {
        dispositivo_VALOR.입출력바이트쓰기(0x3f9, 0);
        dispositivo_VALOR.입출력바이트쓰기(0x3fb, 0x80);
        dispositivo_VALOR.입출력바이트쓰기(0x3f8, 1);
        dispositivo_VALOR.입출력바이트쓰기(0x3f9, 0);
        dispositivo_VALOR.입출력바이트쓰기(0x3fb, 3);
        dispositivo_VALOR.입출력바이트쓰기(0x3fa, 0xc7);
        dispositivo_VALOR.입출력바이트쓰기(0x3fc, 0x0b);
        borrar_introdución();
    }

    static void 직렬바이트(int VALOR) {
        int 횟수 = 100000;
        while ((dispositivo_VALOR.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) dispositivo_VALOR.입출력바이트쓰기(0x3f8, VALOR);
    }

    static void borrar_introdución() {
        for (int ÍNDICE = 0; ÍNDICE < 2000; ÍNDICE++) {
            dispositivo_VALOR.escribir_Memoria(0xb8000 + ÍNDICE * 2, 32);
            dispositivo_VALOR.escribir_Memoria(0xb8001 + ÍNDICE * 2, 색);
        }
        칸 = 0;
        cursor_VALOR();
    }

    static void cursor_VALOR() {
        dispositivo_VALOR.입출력바이트쓰기(0x3d4, 14);
        dispositivo_VALOR.입출력바이트쓰기(0x3d5, 칸 >> 8);
        dispositivo_VALOR.입출력바이트쓰기(0x3d4, 15);
        dispositivo_VALOR.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int VALOR) {
        if (VALOR == 13) return;
        if (VALOR == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (VALOR == 8) {
            if (칸 > 0) {
                칸--;
                dispositivo_VALOR.escribir_Memoria(0xb8000 + 칸 * 2, 32);
            }
        } else {
            dispositivo_VALOR.escribir_Memoria(0xb8000 + 칸 * 2, VALOR < 128 ? VALOR : '?');
            dispositivo_VALOR.escribir_Memoria(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int ÍNDICE = 0; ÍNDICE < 3840; ÍNDICE++)
                dispositivo_VALOR.escribir_Memoria(0xb8000 + ÍNDICE, dispositivo_VALOR.기억읽기(0xb80a0 + ÍNDICE));
            for (int ÍNDICE = 1920; ÍNDICE < 2000; ÍNDICE++) {
                dispositivo_VALOR.escribir_Memoria(0xb8000 + ÍNDICE * 2, 32);
                dispositivo_VALOR.escribir_Memoria(0xb8001 + ÍNDICE * 2, 색);
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

    static void Escritura(String Contido_VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < Contido_VALOR.length(); ÍNDICE++) 문자(Contido_VALOR.charAt(ÍNDICE));
    }

    static void 수쓰기(int VALOR) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALOR < 0) 문자('-');
        else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000;
        boolean Executar_2 = false;
        while (cargo_ÍNDICE > 0) {
            int díxito_VALOR = -(VALOR / cargo_ÍNDICE);
            if (díxito_VALOR != 0 || Executar_2 || cargo_ÍNDICE == 1) {
                문자('0' + díxito_VALOR);
                Executar_2 = true;
            }
            VALOR %= cargo_ÍNDICE;
            cargo_ÍNDICE /= 10;
        }
    }

    static int 직렬읽기() {
        if ((dispositivo_VALOR.입출력바이트읽기(0x3fd) & 1) != 0) return dispositivo_VALOR.입출력바이트읽기(0x3f8);
        return -1;
    }
}
