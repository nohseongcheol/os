// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int rami_Mashigar_bayanai = 0;
    static int 색 = 7;

    static void Shirya() {
        na_ura_Daraja.입출력바이트쓰기(0x3f9, 0);
        na_ura_Daraja.입출력바이트쓰기(0x3fb, 0x80);
        na_ura_Daraja.입출력바이트쓰기(0x3f8, 1);
        na_ura_Daraja.입출력바이트쓰기(0x3f9, 0);
        na_ura_Daraja.입출력바이트쓰기(0x3fb, 3);
        na_ura_Daraja.입출력바이트쓰기(0x3fa, 0xc7);
        na_ura_Daraja.입출력바이트쓰기(0x3fc, 0x0b);
        share_Mashigar_bayanai();
    }

    static void 직렬바이트(int Daraja) {
        int 횟수 = 100000;
        while ((na_ura_Daraja.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) na_ura_Daraja.입출력바이트쓰기(0x3f8, Daraja);
    }

    static void share_Mashigar_bayanai() {
        for (int Indes = 0; Indes < 2000; Indes++) {
            na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8000 + Indes * 2, 32);
            na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8001 + Indes * 2, 색);
        }
        rami_Mashigar_bayanai = 0;
        Ɗan_jagora_Daraja();
    }

    static void Ɗan_jagora_Daraja() {
        na_ura_Daraja.입출력바이트쓰기(0x3d4, 14);
        na_ura_Daraja.입출력바이트쓰기(0x3d5, rami_Mashigar_bayanai >> 8);
        na_ura_Daraja.입출력바이트쓰기(0x3d4, 15);
        na_ura_Daraja.입출력바이트쓰기(0x3d5, rami_Mashigar_bayanai & 255);
    }

    static void 화면문자(int Daraja) {
        if (Daraja == 13) return;
        if (Daraja == 10) {
            rami_Mashigar_bayanai = (rami_Mashigar_bayanai / 80 + 1) * 80;
        } else if (Daraja == 8) {
            if (rami_Mashigar_bayanai > 0) {
                rami_Mashigar_bayanai--;
                na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8000 + rami_Mashigar_bayanai * 2, 32);
            }
        } else {
            na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8000 + rami_Mashigar_bayanai * 2, Daraja < 128 ? Daraja : '?');
            na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8001 + rami_Mashigar_bayanai * 2, 색);
            rami_Mashigar_bayanai++;
        }
        if (rami_Mashigar_bayanai >= 2000) {
            for (int Indes = 0; Indes < 3840; Indes++)
                na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8000 + Indes, na_ura_Daraja.기억읽기(0xb80a0 + Indes));
            for (int Indes = 1920; Indes < 2000; Indes++) {
                na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8000 + Indes * 2, 32);
                na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(0xb8001 + Indes * 2, 색);
            }
            rami_Mashigar_bayanai = 1920;
        }
        Ɗan_jagora_Daraja();
    }

    static void 문자(int Daraja) {
        if (Daraja < 128) {
            if (Daraja == 10) 직렬바이트(13);
            직렬바이트(Daraja);
        } else if (Daraja < 2048) {
            직렬바이트(0xc0 | (Daraja >> 6));
            직렬바이트(0x80 | (Daraja & 63));
        } else {
            직렬바이트(0xe0 | (Daraja >> 12));
            직렬바이트(0x80 | ((Daraja >> 6) & 63));
            직렬바이트(0x80 | (Daraja & 63));
        }
        화면문자(Daraja);
    }

    static void Yi_Rubutu(String kunshiya_Daraja) {
        for (int Indes = 0; Indes < kunshiya_Daraja.length(); Indes++) 문자(kunshiya_Daraja.charAt(Indes));
    }

    static void 수쓰기(int Daraja) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (Daraja < 0) 문자('-');
        else Daraja = -Daraja;
        int 자리 = 1000000000;
        boolean Tafiyar_da = false;
        while (자리 > 0) {
            int lamba_Daraja = -(Daraja / 자리);
            if (lamba_Daraja != 0 || Tafiyar_da || 자리 == 1) {
                문자('0' + lamba_Daraja);
                Tafiyar_da = true;
            }
            Daraja %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((na_ura_Daraja.입출력바이트읽기(0x3fd) & 1) != 0) return na_ura_Daraja.입출력바이트읽기(0x3f8);
        return -1;
    }
}
