// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int oghere_ndebà = 0;
    static int 색 = 7;

    static void Kwado() {
        njìarụ_valuu.입출력바이트쓰기(0x3f9, 0);
        njìarụ_valuu.입출력바이트쓰기(0x3fb, 0x80);
        njìarụ_valuu.입출력바이트쓰기(0x3f8, 1);
        njìarụ_valuu.입출력바이트쓰기(0x3f9, 0);
        njìarụ_valuu.입출력바이트쓰기(0x3fb, 3);
        njìarụ_valuu.입출력바이트쓰기(0x3fa, 0xc7);
        njìarụ_valuu.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int valuu) {
        int 횟수 = 100000;
        while ((njìarụ_valuu.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) njìarụ_valuu.입출력바이트쓰기(0x3f8, valuu);
    }

    static void 지우기() {
        for (int indèks = 0; indèks < 2000; indèks++) {
            njìarụ_valuu.dee_memọrị(0xb8000 + indèks * 2, 32);
            njìarụ_valuu.dee_memọrị(0xb8001 + indèks * 2, 색);
        }
        oghere_ndebà = 0;
        akàran̄ziebe_valuu();
    }

    static void akàran̄ziebe_valuu() {
        njìarụ_valuu.입출력바이트쓰기(0x3d4, 14);
        njìarụ_valuu.입출력바이트쓰기(0x3d5, oghere_ndebà >> 8);
        njìarụ_valuu.입출력바이트쓰기(0x3d4, 15);
        njìarụ_valuu.입출력바이트쓰기(0x3d5, oghere_ndebà & 255);
    }

    static void 화면문자(int valuu) {
        if (valuu == 13) return;
        if (valuu == 10) {
            oghere_ndebà = (oghere_ndebà / 80 + 1) * 80;
        } else if (valuu == 8) {
            if (oghere_ndebà > 0) {
                oghere_ndebà--;
                njìarụ_valuu.dee_memọrị(0xb8000 + oghere_ndebà * 2, 32);
            }
        } else {
            njìarụ_valuu.dee_memọrị(0xb8000 + oghere_ndebà * 2, valuu < 128 ? valuu : '?');
            njìarụ_valuu.dee_memọrị(0xb8001 + oghere_ndebà * 2, 색);
            oghere_ndebà++;
        }
        if (oghere_ndebà >= 2000) {
            for (int indèks = 0; indèks < 3840; indèks++)
                njìarụ_valuu.dee_memọrị(0xb8000 + indèks, njìarụ_valuu.기억읽기(0xb80a0 + indèks));
            for (int indèks = 1920; indèks < 2000; indèks++) {
                njìarụ_valuu.dee_memọrị(0xb8000 + indèks * 2, 32);
                njìarụ_valuu.dee_memọrị(0xb8001 + indèks * 2, 색);
            }
            oghere_ndebà = 1920;
        }
        akàran̄ziebe_valuu();
    }

    static void 문자(int valuu) {
        if (valuu < 128) {
            if (valuu == 10) 직렬바이트(13);
            직렬바이트(valuu);
        } else if (valuu < 2048) {
            직렬바이트(0xc0 | (valuu >> 6));
            직렬바이트(0x80 | (valuu & 63));
        } else {
            직렬바이트(0xe0 | (valuu >> 12));
            직렬바이트(0x80 | ((valuu >> 6) & 63));
            직렬바이트(0x80 | (valuu & 63));
        }
        화면문자(valuu);
    }

    static void Chekwaa_ozi(String ndịnà_valuu) {
        for (int indèks = 0; indèks < ndịnà_valuu.length(); indèks++) 문자(ndịnà_valuu.charAt(indèks));
    }

    static void 수쓰기(int valuu) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (valuu < 0) 문자('-');
        else valuu = -valuu;
        int 자리 = 1000000000;
        boolean Bido = false;
        while (자리 > 0) {
            int ọbula_valuu = -(valuu / 자리);
            if (ọbula_valuu != 0 || Bido || 자리 == 1) {
                문자('0' + ọbula_valuu);
                Bido = true;
            }
            valuu %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((njìarụ_valuu.입출력바이트읽기(0x3fd) & 1) != 0) return njìarụ_valuu.입출력바이트읽기(0x3f8);
        return -1;
    }
}
