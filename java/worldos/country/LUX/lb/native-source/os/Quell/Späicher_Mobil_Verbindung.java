// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 Beräich_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class Späicher_Mobil_Verbindung {
    static boolean 사용가능 = false;
    static int[] Beräich_Daten = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) Mobil_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Laf = Mobil_VALUE.밀리초();
        while (Mobil_VALUE.밀리초() - Laf < 500) {
            int Status_VALUE = Mobil_VALUE.입출력바이트읽기(0x1f7);
            if (Status_VALUE == 0 || Status_VALUE == 255) return -19;
            if ((Status_VALUE & 128) == 0) {
                if ((Status_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Status_VALUE & 8) != 0) return 0;
            }
            Mobil_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int Beräich_VALUE, int Befeel) {
        if (Beräich_VALUE < 0 || Beräich_VALUE >= 2048) return -22;
        Mobil_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        Mobil_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int Mooss = 준비기다리기(false);
        if (Mooss < 0) return Mooss;
        Mobil_VALUE.입출력바이트쓰기(0x1f2, 1);
        Mobil_VALUE.입출력바이트쓰기(0x1f3, Beräich_VALUE & 255);
        Mobil_VALUE.입출력바이트쓰기(0x1f4, (Beräich_VALUE >>> 8) & 255);
        Mobil_VALUE.입출력바이트쓰기(0x1f5, 0);
        Mobil_VALUE.입출력바이트쓰기(0x1f7, Befeel); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int 읽기(int Beräich_VALUE) {
        int Mooss = 요청(Beräich_VALUE, 0x20);
        if (Mooss < 0) return Mooss;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = Mobil_VALUE.입출력짧은수읽기(0x1f0);
            Beräich_Daten[INDEX * 2] = VALUE & 255; Beräich_Daten[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int schreiwen(int Beräich_VALUE) {
        if (!사용가능 || Beräich_VALUE < 1 || Beräich_VALUE > 518) return -19;
        int Mooss = 요청(Beräich_VALUE, 0x30);
        if (Mooss < 0) return Mooss;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            Mobil_VALUE.입출력짧은수쓰기(0x1f0, Beräich_Daten[INDEX * 2] | Beräich_Daten[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!사용가능) return -19;
        Mobil_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analyséieren_Ganzzuel(int positionéieren) {
        return Beräich_Daten[positionéieren] | Beräich_Daten[positionéieren + 1] << 8 | Beräich_Daten[positionéieren + 2] << 16 | Beräich_Daten[positionéieren + 3] << 24;
    }
    static void schreiwen_Ganzzuel_VALUE(int positionéieren, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) Beräich_Daten[positionéieren + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
