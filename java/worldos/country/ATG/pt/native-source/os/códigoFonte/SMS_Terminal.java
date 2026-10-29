// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 tela. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class SMS_Terminal {
    static int slot_entrada = 0;
    static int 색 = 7;

    static void Preparar() {
        celular_VALOR.입출력바이트쓰기(0x3f9, 0);
        celular_VALOR.입출력바이트쓰기(0x3fb, 0x80);
        celular_VALOR.입출력바이트쓰기(0x3f8, 1);
        celular_VALOR.입출력바이트쓰기(0x3f9, 0);
        celular_VALOR.입출력바이트쓰기(0x3fb, 3);
        celular_VALOR.입출력바이트쓰기(0x3fa, 0xc7);
        celular_VALOR.입출력바이트쓰기(0x3fc, 0x0b);
        apagar_entrada();
    }

    static void 직렬바이트(int VALOR) {
        int repetição_CONT_NÚM = 100000;
        while ((celular_VALOR.입출력바이트읽기(0x3fd) & 0x20) == 0 && repetição_CONT_NÚM > 0) repetição_CONT_NÚM--;
        if (repetição_CONT_NÚM > 0) celular_VALOR.입출력바이트쓰기(0x3f8, VALOR);
    }

    static void apagar_entrada() {
        for (int ÍNDICE = 0; ÍNDICE < 2000; ÍNDICE++) {
            celular_VALOR.gravar_Memória(0xb8000 + ÍNDICE * 2, 32);
            celular_VALOR.gravar_Memória(0xb8001 + ÍNDICE * 2, 색);
        }
        slot_entrada = 0;
        cursor_VALOR();
    }

    static void cursor_VALOR() {
        celular_VALOR.입출력바이트쓰기(0x3d4, 14);
        celular_VALOR.입출력바이트쓰기(0x3d5, slot_entrada >> 8);
        celular_VALOR.입출력바이트쓰기(0x3d4, 15);
        celular_VALOR.입출력바이트쓰기(0x3d5, slot_entrada & 255);
    }

    static void tela_caractere(int VALOR) {
        if (VALOR == 13) return;
        if (VALOR == 10) {
            slot_entrada = (slot_entrada / 80 + 1) * 80;
        } else if (VALOR == 8) {
            if (slot_entrada > 0) {
                slot_entrada--;
                celular_VALOR.gravar_Memória(0xb8000 + slot_entrada * 2, 32);
            }
        } else {
            celular_VALOR.gravar_Memória(0xb8000 + slot_entrada * 2, VALOR < 128 ? VALOR : '?');
            celular_VALOR.gravar_Memória(0xb8001 + slot_entrada * 2, 색);
            slot_entrada++;
        }
        if (slot_entrada >= 2000) {
            for (int ÍNDICE = 0; ÍNDICE < 3840; ÍNDICE++)
                celular_VALOR.gravar_Memória(0xb8000 + ÍNDICE, celular_VALOR.leitura_Memória(0xb80a0 + ÍNDICE));
            for (int ÍNDICE = 1920; ÍNDICE < 2000; ÍNDICE++) {
                celular_VALOR.gravar_Memória(0xb8000 + ÍNDICE * 2, 32);
                celular_VALOR.gravar_Memória(0xb8001 + ÍNDICE * 2, 색);
            }
            slot_entrada = 1920;
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
        tela_caractere(VALOR);
    }

    static void Escrita(String Conteúdo_VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < Conteúdo_VALOR.length(); ÍNDICE++) 문자(Conteúdo_VALOR.charAt(ÍNDICE));
    }

    static void gravar_número(int VALOR) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALOR < 0) 문자('-');
        else VALOR = -VALOR;
        int cargo_ÍNDICE = 1000000000;
        boolean iniciar = false;
        while (cargo_ÍNDICE > 0) {
            int dígito_VALOR = -(VALOR / cargo_ÍNDICE);
            if (dígito_VALOR != 0 || iniciar || cargo_ÍNDICE == 1) {
                문자('0' + dígito_VALOR);
                iniciar = true;
            }
            VALOR %= cargo_ÍNDICE;
            cargo_ÍNDICE /= 10;
        }
    }

    static int 직렬읽기() {
        if ((celular_VALOR.입출력바이트읽기(0x3fd) & 1) != 0) return celular_VALOR.입출력바이트읽기(0x3f8);
        return -1;
    }
}
