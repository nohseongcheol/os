// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int 칸 = 0;
    static int 색 = 7;

    static void Heblu() {
        kaɓirgal_njaru.입출력바이트쓰기(0x3f9, 0);
        kaɓirgal_njaru.입출력바이트쓰기(0x3fb, 0x80);
        kaɓirgal_njaru.입출력바이트쓰기(0x3f8, 1);
        kaɓirgal_njaru.입출력바이트쓰기(0x3f9, 0);
        kaɓirgal_njaru.입출력바이트쓰기(0x3fb, 3);
        kaɓirgal_njaru.입출력바이트쓰기(0x3fa, 0xc7);
        kaɓirgal_njaru.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int njaru) {
        int 횟수 = 100000;
        while ((kaɓirgal_njaru.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) kaɓirgal_njaru.입출력바이트쓰기(0x3f8, njaru);
    }

    static void 지우기() {
        for (int joopirdu = 0; joopirdu < 2000; joopirdu++) {
            kaɓirgal_njaru.winndude_teskordu(0xb8000 + joopirdu * 2, 32);
            kaɓirgal_njaru.winndude_teskordu(0xb8001 + joopirdu * 2, 색);
        }
        칸 = 0;
        kirseer_njaru();
    }

    static void kirseer_njaru() {
        kaɓirgal_njaru.입출력바이트쓰기(0x3d4, 14);
        kaɓirgal_njaru.입출력바이트쓰기(0x3d5, 칸 >> 8);
        kaɓirgal_njaru.입출력바이트쓰기(0x3d4, 15);
        kaɓirgal_njaru.입출력바이트쓰기(0x3d5, 칸 & 255);
    }

    static void 화면문자(int njaru) {
        if (njaru == 13) return;
        if (njaru == 10) {
            칸 = (칸 / 80 + 1) * 80;
        } else if (njaru == 8) {
            if (칸 > 0) {
                칸--;
                kaɓirgal_njaru.winndude_teskordu(0xb8000 + 칸 * 2, 32);
            }
        } else {
            kaɓirgal_njaru.winndude_teskordu(0xb8000 + 칸 * 2, njaru < 128 ? njaru : '?');
            kaɓirgal_njaru.winndude_teskordu(0xb8001 + 칸 * 2, 색);
            칸++;
        }
        if (칸 >= 2000) {
            for (int joopirdu = 0; joopirdu < 3840; joopirdu++)
                kaɓirgal_njaru.winndude_teskordu(0xb8000 + joopirdu, kaɓirgal_njaru.기억읽기(0xb80a0 + joopirdu));
            for (int joopirdu = 1920; joopirdu < 2000; joopirdu++) {
                kaɓirgal_njaru.winndude_teskordu(0xb8000 + joopirdu * 2, 32);
                kaɓirgal_njaru.winndude_teskordu(0xb8001 + joopirdu * 2, 색);
            }
            칸 = 1920;
        }
        kirseer_njaru();
    }

    static void 문자(int njaru) {
        if (njaru < 128) {
            if (njaru == 10) 직렬바이트(13);
            직렬바이트(njaru);
        } else if (njaru < 2048) {
            직렬바이트(0xc0 | (njaru >> 6));
            직렬바이트(0x80 | (njaru & 63));
        } else {
            직렬바이트(0xe0 | (njaru >> 12));
            직렬바이트(0x80 | ((njaru >> 6) & 63));
            직렬바이트(0x80 | (njaru & 63));
        }
        화면문자(njaru);
    }

    static void winndude(String loowdi_njaru) {
        for (int joopirdu = 0; joopirdu < loowdi_njaru.length(); joopirdu++) 문자(loowdi_njaru.charAt(joopirdu));
    }

    static void 수쓰기(int njaru) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (njaru < 0) 문자('-');
        else njaru = -njaru;
        int 자리 = 1000000000;
        boolean huutoraade = false;
        while (자리 > 0) {
            int 숫자 = -(njaru / 자리);
            if (숫자 != 0 || huutoraade || 자리 == 1) {
                문자('0' + 숫자);
                huutoraade = true;
            }
            njaru %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((kaɓirgal_njaru.입출력바이트읽기(0x3fd) & 1) != 0) return kaɓirgal_njaru.입출력바이트읽기(0x3f8);
        return -1;
    }
}
