// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** COM1 직렬 출력과 VGA 80x25 문자 화면. 한글은 직렬 단말에 UTF-8로 출력한다. */
public final class 문자단말 {
    static int ààyè_ìfàyọkàsí_ìgbéwọlé = 0;
    static int 색 = 7;

    static void gbaradì() {
        ohun_èlò_iye.입출력바이트쓰기(0x3f9, 0);
        ohun_èlò_iye.입출력바이트쓰기(0x3fb, 0x80);
        ohun_èlò_iye.입출력바이트쓰기(0x3f8, 1);
        ohun_èlò_iye.입출력바이트쓰기(0x3f9, 0);
        ohun_èlò_iye.입출력바이트쓰기(0x3fb, 3);
        ohun_èlò_iye.입출력바이트쓰기(0x3fa, 0xc7);
        ohun_èlò_iye.입출력바이트쓰기(0x3fc, 0x0b);
        지우기();
    }

    static void 직렬바이트(int iye) {
        int 횟수 = 100000;
        while ((ohun_èlò_iye.입출력바이트읽기(0x3fd) & 0x20) == 0 && 횟수 > 0) 횟수--;
        if (횟수 > 0) ohun_èlò_iye.입출력바이트쓰기(0x3f8, iye);
    }

    static void 지우기() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 2000; wá_atọ̀ka_àkóónú++) {
            ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8000 + wá_atọ̀ka_àkóónú * 2, 32);
            ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8001 + wá_atọ̀ka_àkóónú * 2, 색);
        }
        ààyè_ìfàyọkàsí_ìgbéwọlé = 0;
        kọ́sọ̀_iye();
    }

    static void kọ́sọ̀_iye() {
        ohun_èlò_iye.입출력바이트쓰기(0x3d4, 14);
        ohun_èlò_iye.입출력바이트쓰기(0x3d5, ààyè_ìfàyọkàsí_ìgbéwọlé >> 8);
        ohun_èlò_iye.입출력바이트쓰기(0x3d4, 15);
        ohun_èlò_iye.입출력바이트쓰기(0x3d5, ààyè_ìfàyọkàsí_ìgbéwọlé & 255);
    }

    static void 화면문자(int iye) {
        if (iye == 13) return;
        if (iye == 10) {
            ààyè_ìfàyọkàsí_ìgbéwọlé = (ààyè_ìfàyọkàsí_ìgbéwọlé / 80 + 1) * 80;
        } else if (iye == 8) {
            if (ààyè_ìfàyọkàsí_ìgbéwọlé > 0) {
                ààyè_ìfàyọkàsí_ìgbéwọlé--;
                ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8000 + ààyè_ìfàyọkàsí_ìgbéwọlé * 2, 32);
            }
        } else {
            ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8000 + ààyè_ìfàyọkàsí_ìgbéwọlé * 2, iye < 128 ? iye : '?');
            ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8001 + ààyè_ìfàyọkàsí_ìgbéwọlé * 2, 색);
            ààyè_ìfàyọkàsí_ìgbéwọlé++;
        }
        if (ààyè_ìfàyọkàsí_ìgbéwọlé >= 2000) {
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 3840; wá_atọ̀ka_àkóónú++)
                ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8000 + wá_atọ̀ka_àkóónú, ohun_èlò_iye.기억읽기(0xb80a0 + wá_atọ̀ka_àkóónú));
            for (int wá_atọ̀ka_àkóónú = 1920; wá_atọ̀ka_àkóónú < 2000; wá_atọ̀ka_àkóónú++) {
                ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8000 + wá_atọ̀ka_àkóónú * 2, 32);
                ohun_èlò_iye.kọ_ibi_ìpamọ́(0xb8001 + wá_atọ̀ka_àkóónú * 2, 색);
            }
            ààyè_ìfàyọkàsí_ìgbéwọlé = 1920;
        }
        kọ́sọ̀_iye();
    }

    static void 문자(int iye) {
        if (iye < 128) {
            if (iye == 10) 직렬바이트(13);
            직렬바이트(iye);
        } else if (iye < 2048) {
            직렬바이트(0xc0 | (iye >> 6));
            직렬바이트(0x80 | (iye & 63));
        } else {
            직렬바이트(0xe0 | (iye >> 12));
            직렬바이트(0x80 | ((iye >> 6) & 63));
            직렬바이트(0x80 | (iye & 63));
        }
        화면문자(iye);
    }

    static void Kọ(String Àkóónú_iye) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < Àkóónú_iye.length(); wá_atọ̀ka_àkóónú++) 문자(Àkóónú_iye.charAt(wá_atọ̀ka_àkóónú));
    }

    static void 수쓰기(int iye) {
        // 양수로 바꾸지 않으므로 Integer.MIN_VALUE도 안전하다.
        if (iye < 0) 문자('-');
        else iye = -iye;
        int 자리 = 1000000000;
        boolean Rọ́ọ̀nù = false;
        while (자리 > 0) {
            int díjììtì_iye = -(iye / 자리);
            if (díjììtì_iye != 0 || Rọ́ọ̀nù || 자리 == 1) {
                문자('0' + díjììtì_iye);
                Rọ́ọ̀nù = true;
            }
            iye %= 자리;
            자리 /= 10;
        }
    }

    static int 직렬읽기() {
        if ((ohun_èlò_iye.입출력바이트읽기(0x3fd) & 1) != 0) return ohun_èlò_iye.입출력바이트읽기(0x3f8);
        return -1;
    }
}
