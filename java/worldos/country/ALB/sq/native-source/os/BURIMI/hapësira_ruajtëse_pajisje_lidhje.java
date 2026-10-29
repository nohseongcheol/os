// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 seksion_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class hapësira_ruajtëse_pajisje_lidhje {
    static boolean teknologjia_e_informacionit_Aktiv_9e72441a = false;
    static int[] seksion_të_dhëna = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) pajisje_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Ekzekuto = pajisje_VALUE.밀리초();
        while (pajisje_VALUE.밀리초() - Ekzekuto < 500) {
            int status_VALUE = pajisje_VALUE.입출력바이트읽기(0x1f7);
            if (status_VALUE == 0 || status_VALUE == 255) return -19;
            if ((status_VALUE & 128) == 0) {
                if ((status_VALUE & 33) != 0) return -5;
                if (!자료필요 || (status_VALUE & 8) != 0) return 0;
            }
            pajisje_VALUE.잠시양보();
        }
        return -110;
    }
    static int 요청(int seksion_VALUE, int Komanda) {
        if (seksion_VALUE < 0 || seksion_VALUE >= 2048) return -22;
        pajisje_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ 사용 안 함
        pajisje_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int llogaritje = 준비기다리기(false);
        if (llogaritje < 0) return llogaritje;
        pajisje_VALUE.입출력바이트쓰기(0x1f2, 1);
        pajisje_VALUE.입출력바이트쓰기(0x1f3, seksion_VALUE & 255);
        pajisje_VALUE.입출력바이트쓰기(0x1f4, (seksion_VALUE >>> 8) & 255);
        pajisje_VALUE.입출력바이트쓰기(0x1f5, 0);
        pajisje_VALUE.입출력바이트쓰기(0x1f7, Komanda); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Leximi(int seksion_VALUE) {
        int llogaritje = 요청(seksion_VALUE, 0x20);
        if (llogaritje < 0) return llogaritje;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = pajisje_VALUE.입출력짧은수읽기(0x1f0);
            seksion_të_dhëna[INDEX * 2] = VALUE & 255; seksion_të_dhëna[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Shkrimi(int seksion_VALUE) {
        if (!teknologjia_e_informacionit_Aktiv_9e72441a || seksion_VALUE < 1 || seksion_VALUE > 518) return -19;
        int llogaritje = 요청(seksion_VALUE, 0x30);
        if (llogaritje < 0) return llogaritje;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            pajisje_VALUE.입출력짧은수쓰기(0x1f0, seksion_të_dhëna[INDEX * 2] | seksion_të_dhëna[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!teknologjia_e_informacionit_Aktiv_9e72441a) return -19;
        pajisje_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analizoj_numër_i_plotë(int Pozicioni) {
        return seksion_të_dhëna[Pozicioni] | seksion_të_dhëna[Pozicioni + 1] << 8 | seksion_të_dhëna[Pozicioni + 2] << 16 | seksion_të_dhëna[Pozicioni + 3] << 24;
    }
    static void shkruaj_numër_i_plotë_VALUE(int Pozicioni, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) seksion_të_dhëna[Pozicioni + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
