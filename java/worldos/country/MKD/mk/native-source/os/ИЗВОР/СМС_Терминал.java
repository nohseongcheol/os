// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class СМС_Терминал {
    static int отвор_внес = 0;
    static int 색 = 7;

    static void Подготви() {
        уред_VALUE.입출력바이트쓰기(0x3f9, 0);
        уред_VALUE.입출력바이트쓰기(0x3fb, 0x80);
        уред_VALUE.입출력바이트쓰기(0x3f8, 1);
        уред_VALUE.입출력바이트쓰기(0x3f9, 0);
        уред_VALUE.입출력바이트쓰기(0x3fb, 3);
        уред_VALUE.입출력바이트쓰기(0x3fa, 0xc7);
        уред_VALUE.입출력바이트쓰기(0x3fc, 0x0b);
        избриши_внес();
    }

    static void 직렬바이트(int VALUE) {
        int 횟수 = 100000;
        while ((уред_VALUE.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) уред_VALUE.입출력바이트쓰기(0x3f8, VALUE);
    }

    static void избриши_внес() {
        for (int INDEX = 0; INDEX < 2000; INDEX++) {
            уред_VALUE.запиши_Меморија(0xb8000 + INDEX * 2, 32);
            уред_VALUE.запиши_Меморија(0xb8001 + INDEX * 2, 색);
        }
        отвор_внес = 0;
        покажувач_VALUE();
    }

    static void покажувач_VALUE() {
        уред_VALUE.입출력바이트쓰기(0x3d4, 14);
        уред_VALUE.입출력바이트쓰기(0x3d5, отвор_внес >> 8);
        уред_VALUE.입출력바이트쓰기(0x3d4, 15);
        уред_VALUE.입출력바이트쓰기(0x3d5, отвор_внес & 255);
    }

    static void 화면문자(int VALUE) {
        if (VALUE == 13) return;
        if (VALUE == 10) {
            отвор_внес = (отвор_внес / 80 + 1) * 80;
        } else if (VALUE == 8) {
            if (отвор_внес > 0) {
                отвор_внес--;
                уред_VALUE.запиши_Меморија(0xb8000 + отвор_внес * 2, 32);
            }
        } else {
            уред_VALUE.запиши_Меморија(0xb8000 + отвор_внес * 2, VALUE < 128 ? VALUE : '?');
            уред_VALUE.запиши_Меморија(0xb8001 + отвор_внес * 2, 색);
            отвор_внес++;
        }
        if (отвор_внес >= 2000) {
            for (int INDEX = 0; INDEX < 3840; INDEX++)
                уред_VALUE.запиши_Меморија(0xb8000 + INDEX, уред_VALUE.기억읽기(0xb80a0 + INDEX));
            for (int INDEX = 1920; INDEX < 2000; INDEX++) {
                уред_VALUE.запиши_Меморија(0xb8000 + INDEX * 2, 32);
                уред_VALUE.запиши_Меморија(0xb8001 + INDEX * 2, 색);
            }
            отвор_внес = 1920;
        }
        покажувач_VALUE();
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

    static void Запиши(String Содржина_VALUE) {
        for (int INDEX = 0; INDEX < Содржина_VALUE.length(); INDEX++) 문자(Содржина_VALUE.charAt(INDEX));
    }

    static void 수쓰기(int VALUE) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (VALUE < 0) 문자('-');
        else VALUE = -VALUE;
        int позиционирање_INDEX = 1000000000;
        boolean Изврши_2 = false;
        while (позиционирање_INDEX > 0) {
            int цифра_VALUE = -(VALUE / позиционирање_INDEX);
            if (цифра_VALUE != 0 || Изврши_2 || позиционирање_INDEX == 1) {
                문자('0' + цифра_VALUE);
                Изврши_2 = true;
            }
            VALUE %= позиционирање_INDEX;
            позиционирање_INDEX /= 10;
        }
    }

    static int 직렬읽기() {
        if ((уред_VALUE.입출력바이트읽기(0x3fd) & 1) != 0) return уред_VALUE.입출력바이트읽기(0x3f8);
        return -1;
    }
}
