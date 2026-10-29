// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class СМС_Терминал {
    static int оя_кертү = 0;
    static int 색 = 7;

    static void Әзерләү() {
        мобиль_VALUE.입출력바이트쓰기(0x3f9, 0);
        мобиль_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        мобиль_VALUE.입출력바이트쓰기(0x3f8, 1);
        мобиль_VALUE.입출력바이트쓰기(0x3f9, 0);
        мобиль_VALUE.입출력바이트쓰기(0x3fb, 3);
        мобиль_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        мобиль_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((мобиль_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) мобиль_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void 지우기() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            мобиль_VALUE.язу_Хәтер(0xb8000 + INDEX * 2, 32);
            мобиль_VALUE.язу_Хәтер(0xb8001 + INDEX * 2, 색);
        }
        оя_кертү = 0;
        курсор_VALUE();
    }

    static void курсор_VALUE() {
        мобиль_VALUE.입출력바이트쓰기(0x3d4, 14);
        мобиль_VALUE.입출력바이트쓰기(0x3d5, оя_кертү >> 8);
        мобиль_VALUE.입출력바이트쓰기(0x3d4, 15);
        мобиль_VALUE.입출력바이트쓰기(0x3d5, оя_кертү & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            оя_кертү = (оя_кертү / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (оя_кертү > 0) {
                оя_кертү--;
                мобиль_VALUE.язу_Хәтер(0xb8000 + оя_кертү * 2, 32);
            }
        } else {
            мобиль_VALUE.язу_Хәтер(0xb8000 + оя_кертү * 2, VALUE < 128 ? VALUE : '?');
            мобиль_VALUE.язу_Хәтер(0xb8001 + оя_кертү * 2, 색);
            оя_кертү++;
        }
        if (оя_кертү >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                мобиль_VALUE.язу_Хәтер(0xb8000 + INDEX, мобиль_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                мобиль_VALUE.язу_Хәтер(0xb8000 + INDEX * 2, 32);
                мобиль_VALUE.язу_Хәтер(0xb8001 + INDEX * 2, 색);
            }
            оя_кертү = 1920;
        }
        курсор_VALUE();
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

    static void язу(String Эчтәлек_VALUE) {
        for (int INDEX = 0; INDEX < Эчтәлек_VALUE.length(); INDEX++) 문자(Эчтәлек_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int урнаштыру_INDEX = 1000000000;
        boolean эшләтү = false;
        while (урнаштыру_INDEX > 0) {
            int сан_VALUE = -(VALUE / урнаштыру_INDEX);
            if (сан_VALUE != 0 || эшләтү || урнаштыру_INDEX == 1) {
                문자('0' + сан_VALUE);
                эшләтү = true;
            }
            VALUE %= урнаштыру_INDEX;
            урнаштыру_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((мобиль_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return мобиль_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
