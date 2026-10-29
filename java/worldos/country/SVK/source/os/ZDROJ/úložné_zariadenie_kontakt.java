// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 sekcia_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class úložné_zariadenie_kontakt {
    static boolean Informačné_systémy_Aktívny_9e72441a = false;
    static int[] sekcia_údaje = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) telefón_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Spustiť_2 = telefón_VALUE.밀리초();
        while (telefón_VALUE.밀리초() - Spustiť_2 < 500) {
            int Stav_VALUE = telefón_VALUE.입출력바이트읽기(0x1f7);
            if (Stav_VALUE == 0 || Stav_VALUE == 255) return -19;
            if ((Stav_VALUE & 128) == 0) {
                if ((Stav_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Stav_VALUE & 8) != 0) return 0;
            }
            telefón_VALUE.잠시양보();
        }
        return -110;
    }
    static int požiadavka(int sekcia_VALUE, int Príkaz) {
        if (sekcia_VALUE < 0 || sekcia_VALUE >= 2048) return -22;
        telefón_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ používať_VALUE 안 함
        telefón_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int KR = 준비기다리기(false);
        if (KR < 0) return KR;
        telefón_VALUE.입출력바이트쓰기(0x1f2, 1);
        telefón_VALUE.입출력바이트쓰기(0x1f3, sekcia_VALUE & 255);
        telefón_VALUE.입출력바이트쓰기(0x1f4, (sekcia_VALUE >>> 8) & 255);
        telefón_VALUE.입출력바이트쓰기(0x1f5, 0);
        telefón_VALUE.입출력바이트쓰기(0x1f7, Príkaz); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Čítanie(int sekcia_VALUE) {
        int KR = požiadavka(sekcia_VALUE, 0x20);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = telefón_VALUE.입출력짧은수읽기(0x1f0);
            sekcia_údaje[INDEX * 2] = VALUE & 255; sekcia_údaje[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Zápis(int sekcia_VALUE) {
        if (!Informačné_systémy_Aktívny_9e72441a || sekcia_VALUE < 1 || sekcia_VALUE > 518) return -19;
        int KR = požiadavka(sekcia_VALUE, 0x30);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            telefón_VALUE.입출력짧은수쓰기(0x1f0, sekcia_údaje[INDEX * 2] | sekcia_údaje[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!Informačné_systémy_Aktívny_9e72441a) return -19;
        telefón_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analyzovať_celé_číslo(int Pozícia) {
        return sekcia_údaje[Pozícia] | sekcia_údaje[Pozícia + 1] << 8 | sekcia_údaje[Pozícia + 2] << 16 | sekcia_údaje[Pozícia + 3] << 24;
    }
    static void zapísať_celé_číslo_VALUE(int Pozícia, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) sekcia_údaje[Pozícia + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
