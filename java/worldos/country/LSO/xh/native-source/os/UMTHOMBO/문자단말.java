// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int isithuba_ufako_nkcukacha = 0;
    static int 색 = 7;

    static void lungisa() {
        isixhobo_ixabiso.입출력바이트쓰기(0x3f9, 0);
        isixhobo_ixabiso.입출력바이트쓰기(0x3fb, 0x80);
        isixhobo_ixabiso.입출력바이트쓰기(0x3f8, 1);
        isixhobo_ixabiso.입출력바이트쓰기(0x3f9, 0);
        isixhobo_ixabiso.입출력바이트쓰기(0x3fb, 3);
        isixhobo_ixabiso.입출력바이트쓰기(0x3fa, 0xc7);
        isixhobo_ixabiso.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int ixabiso) {
        int 횟수 = 100000;
        while ((isixhobo_ixabiso.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) isixhobo_ixabiso.입출력바이트쓰기(0x3f8, ixabiso);
    }

    static void 지우기() {
        for (int indeksa = 0; indeksa < 2000; indeksa++) {
            isixhobo_ixabiso.bhala_imemori(0xb8000 + indeksa * 2, 32);
            isixhobo_ixabiso.bhala_imemori(0xb8001 + indeksa * 2, 색);
        }
        isithuba_ufako_nkcukacha = 0;
        ikhesa_ixabiso();
    }

    static void ikhesa_ixabiso() {
        isixhobo_ixabiso.입출력바이트쓰기(0x3d4, 14);
        isixhobo_ixabiso.입출력바이트쓰기(0x3d5, isithuba_ufako_nkcukacha >> 8);
        isixhobo_ixabiso.입출력바이트쓰기(0x3d4, 15);
        isixhobo_ixabiso.입출력바이트쓰기(0x3d5, isithuba_ufako_nkcukacha & 255);
    }

    static void 화면문자(int ixabiso) {
        if (ixabiso == 13) return;
        if (ixabiso == 10) {
            isithuba_ufako_nkcukacha = (isithuba_ufako_nkcukacha / 80 + 1) * 80;
        } else if (ixabiso == 8) {
            if (isithuba_ufako_nkcukacha > 0) {
                isithuba_ufako_nkcukacha--;
                isixhobo_ixabiso.bhala_imemori(0xb8000 + isithuba_ufako_nkcukacha * 2, 32);
            }
        } else {
            isixhobo_ixabiso.bhala_imemori(0xb8000 + isithuba_ufako_nkcukacha * 2, ixabiso < 128 ? ixabiso : '?');
            isixhobo_ixabiso.bhala_imemori(0xb8001 + isithuba_ufako_nkcukacha * 2, 색);
            isithuba_ufako_nkcukacha++;
        }
        if (isithuba_ufako_nkcukacha >= 2000) {
            for (int indeksa = 0; indeksa < 3840; indeksa++)
                isixhobo_ixabiso.bhala_imemori(0xb8000 + indeksa, isixhobo_ixabiso.기억읽기(0xb80a0 + indeksa));
            for (int indeksa = 1920; indeksa < 2000; indeksa++) {
                isixhobo_ixabiso.bhala_imemori(0xb8000 + indeksa * 2, 32);
                isixhobo_ixabiso.bhala_imemori(0xb8001 + indeksa * 2, 색);
            }
            isithuba_ufako_nkcukacha = 1920;
        }
        ikhesa_ixabiso();
    }

    static void 문자(int ixabiso) {
        if (ixabiso < 128) {
            if (ixabiso == 10) 직렬바이트(13);
            직렬바이트(ixabiso);
        } else if (ixabiso < 2048) {
            직렬바이트(0xc0 | (ixabiso >> 6));
            직렬바이트(0x80 | (ixabiso & 63));
        } else {
            직렬바이트(0xe0 | (ixabiso >> 12));
            직렬바이트(0x80 | ((ixabiso >> 6) & 63));
            직렬바이트(0x80 | (ixabiso & 63));
        }
        화면문자(ixabiso);
    }

    static void Bhala(String Isiqulatho_ixabiso) {
        for (int indeksa = 0; indeksa < Isiqulatho_ixabiso.length(); indeksa++) 문자(Isiqulatho_ixabiso.charAt(indeksa));
    }

    static void 수쓰기(int ixabiso) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (ixabiso < 0) 문자('-');
        else ixabiso = -ixabiso;
        int 자리 = 1000000000;
        boolean Phumeza = false;
        while (자리 > 0) {
            int inani_ixabiso = -(ixabiso / 자리);
            if (inani_ixabiso != 0 || Phumeza || 자리 == 1) {
                문자('0' + inani_ixabiso);
                Phumeza = true;
            }
            ixabiso %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((isixhobo_ixabiso.입출력바이트읽기(0x3fd) & 1) != 0) return isixhobo_ixabiso.입출력바이트읽기(0x3f8);
        return -1;
    }
}
