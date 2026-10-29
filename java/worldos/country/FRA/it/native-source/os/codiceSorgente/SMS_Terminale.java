// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 seriale_VALORE 출력과 VGA 80x25 문자 schermata. 한글은 seriale_VALORE 단말에 UTF-8로 출력한다. */
public final class SMS_Terminale {
    static int slot_voce = 0;
    static int 색 = 7;

    static void Prepara() {
        cellulare_VALORE.입출력바이트쓰기(0x3f9, 0);
        cellulare_VALORE.입출력바이트쓰기(0x3fb, 0x80);
        cellulare_VALORE.입출력바이트쓰기(0x3f8, 1);
        cellulare_VALORE.입출력바이트쓰기(0x3f9, 0);
        cellulare_VALORE.입출력바이트쓰기(0x3fb, 3);
        cellulare_VALORE.입출력바이트쓰기(0x3fa, 0xc7);
        cellulare_VALORE.입출력바이트쓰기(0x3fc, 0x0b);
        cancellare_voce();
    }

    static void seriale_byte(int VALORE) {
        int ripetizione_CONTA_NUMERI = 100000;
        while ((cellulare_VALORE.입출력바이트읽기(0x3fd) & 0x20) == 0 && ripetizione_CONTA_NUMERI > 0) ripetizione_CONTA_NUMERI--;
        if (ripetizione_CONTA_NUMERI > 0) cellulare_VALORE.입출력바이트쓰기(0x3f8, VALORE);
    }

    static void cancellare_voce() {
        for (int INDICE = 0; INDICE < 2000; INDICE++) {
            cellulare_VALORE.scrivere_Memoria(0xb8000 + INDICE * 2, 32);
            cellulare_VALORE.scrivere_Memoria(0xb8001 + INDICE * 2, 색);
        }
        slot_voce = 0;
        cursore_VALORE();
    }

    static void cursore_VALORE() {
        cellulare_VALORE.입출력바이트쓰기(0x3d4, 14);
        cellulare_VALORE.입출력바이트쓰기(0x3d5, slot_voce >> 8);
        cellulare_VALORE.입출력바이트쓰기(0x3d4, 15);
        cellulare_VALORE.입출력바이트쓰기(0x3d5, slot_voce & 255);
    }

    static void schermata_carattere(int VALORE) {
        if (VALORE == 13) return;
        if (VALORE == 10) {
            slot_voce = (slot_voce / 80 + 1) * 80;
        } else if (VALORE == 8) {
            if (slot_voce > 0) {
                slot_voce--;
                cellulare_VALORE.scrivere_Memoria(0xb8000 + slot_voce * 2, 32);
            }
        } else {
            cellulare_VALORE.scrivere_Memoria(0xb8000 + slot_voce * 2, VALORE < 128 ? VALORE : '?');
            cellulare_VALORE.scrivere_Memoria(0xb8001 + slot_voce * 2, 색);
            slot_voce++;
        }
        if (slot_voce >= 2000) {
            for (int INDICE = 0; INDICE < 3840; INDICE++)
                cellulare_VALORE.scrivere_Memoria(0xb8000 + INDICE, cellulare_VALORE.기억읽기(0xb80a0 + INDICE));
            for (int INDICE = 1920; INDICE < 2000; INDICE++) {
                cellulare_VALORE.scrivere_Memoria(0xb8000 + INDICE * 2, 32);
                cellulare_VALORE.scrivere_Memoria(0xb8001 + INDICE * 2, 색);
            }
            slot_voce = 1920;
        }
        cursore_VALORE();
    }

    static void 문자(int VALORE) {
        if (VALORE < 128) {
            if (VALORE == 10) seriale_byte(13);
            seriale_byte(VALORE);
        } else if (VALORE < 2048) {
            seriale_byte(0xc0 | (VALORE >> 6));
            seriale_byte(0x80 | (VALORE & 63));
        } else {
            seriale_byte(0xe0 | (VALORE >> 12));
            seriale_byte(0x80 | ((VALORE >> 6) & 63));
            seriale_byte(0x80 | (VALORE & 63));
        }
        schermata_carattere(VALORE);
    }

    static void Scrittura(String Contenuto_VALORE) {
        for (int INDICE = 0; INDICE < Contenuto_VALORE.length(); INDICE++) 문자(Contenuto_VALORE.charAt(INDICE));
    }

    static void scrivere_numero(int VALORE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALORE < 0) 문자('-');
        else VALORE = -VALORE;
        int funzione_INDICE = 1000000000;
        boolean avvia = false;
        while (funzione_INDICE > 0) {
            int cifra_VALORE = -(VALORE / funzione_INDICE);
            if (cifra_VALORE != 0 || avvia || funzione_INDICE == 1) {
                문자('0' + cifra_VALORE);
                avvia = true;
            }
            VALORE %= funzione_INDICE;
            funzione_INDICE /= 10;
        }
    }

    static int 직렬읽기() {
        if ((cellulare_VALORE.입출력바이트읽기(0x3fd) & 1) != 0) return cellulare_VALORE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
