// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 del_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Lagring_mobil_kontakt {
    static boolean informasjonsteknologi_barn = false;
    static int[] del_data = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Køyr_2 = mobil_VALUE.밀리초();
        while (mobil_VALUE.밀리초() - Køyr_2 < 500) {
            int status_VALUE = mobil_VALUE.입출력바이트읽기(0x1f7);
            if (status_VALUE == 0 || status_VALUE == 255) return -19;
            if ((status_VALUE & 128) == 0) {
                if ((status_VALUE & 33) != 0) return -5;
                if (!자료필요 || (status_VALUE & 8) != 0) return 0;
            }
            mobil_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int del_VALUE, int Kommando) {
        if (del_VALUE < 0 || del_VALUE >= 2048) return -22;
        mobil_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        mobil_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int forretningsmål = 준비기다리기(false);
        if (forretningsmål < 0) return forretningsmål;
        mobil_VALUE.입출력바이트쓰기(0x1f2, 1);
        mobil_VALUE.입출력바이트쓰기(0x1f3, del_VALUE & 255);
        mobil_VALUE.입출력바이트쓰기(0x1f4, (del_VALUE >>> 8) & 255);
        mobil_VALUE.입출력바이트쓰기(0x1f5, 0);
        mobil_VALUE.입출력바이트쓰기(0x1f7, Kommando); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Les(int del_VALUE) {
        int forretningsmål = 요청(del_VALUE, 0x20);
        if (forretningsmål < 0) return forretningsmål;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = mobil_VALUE.입출력짧은수읽기(0x1f0);
            del_data[INDEX * 2] = VALUE & 255; del_data[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Skriv(int del_VALUE) {
        if (!informasjonsteknologi_barn || del_VALUE < 1 || del_VALUE > 518) return -19;
        int forretningsmål = 요청(del_VALUE, 0x30);
        if (forretningsmål < 0) return forretningsmål;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mobil_VALUE.입출력짧은수쓰기(0x1f0, del_data[INDEX * 2] | del_data[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!informasjonsteknologi_barn) return -19;
        mobil_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int dele_opp_heiltal(int Posisjon) {
        return del_data[Posisjon] | del_data[Posisjon + 1] << 8 | del_data[Posisjon + 2] << 16 | del_data[Posisjon + 3] << 24;
    }
    static void skrive_heiltal_VALUE(int Posisjon, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) del_data[Posisjon + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
