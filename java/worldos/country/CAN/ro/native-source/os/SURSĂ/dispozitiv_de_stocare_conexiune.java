// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 IDE 장치의 512바이트 논리 secțiune_VALUE. 이 계층은 포맷을 만들거나 임의 장치를 지우지 않는다. */
public final class dispozitiv_de_stocare_conexiune {
    static boolean sisteme_de_informații_Activ_9e72441a = false;
    static int[] secțiune_date = new int[512];
    static void 잠깐기다리기() {
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_VALUE.입출력바이트읽기(0x3f6);
    }
    static int 준비기다리기(boolean 자료필요) {
        int Pornește = mobil_VALUE.밀리초();
        while (mobil_VALUE.밀리초() - Pornește < 500) {
            int Stare_VALUE = mobil_VALUE.입출력바이트읽기(0x1f7);
            if (Stare_VALUE == 0 || Stare_VALUE == 255) return -19;
            if ((Stare_VALUE & 128) == 0) {
                if ((Stare_VALUE & 33) != 0) return -5;
                if (!자료필요 || (Stare_VALUE & 8) != 0) return 0;
            }
            mobil_VALUE.잠시양보();
        }
        return -110;
    }
    static int cerere(int secțiune_VALUE, int Comandă) {
        if (secțiune_VALUE < 0 || secțiune_VALUE >= 2048) return -22;
        mobil_VALUE.입출력바이트쓰기(0x3f6, 2); // polling; IDE IRQ utiliza_VALUE 안 함
        mobil_VALUE.입출력바이트쓰기(0x1f6, 0xe0); 잠깐기다리기();
        int KR = 준비기다리기(false);
        if (KR < 0) return KR;
        mobil_VALUE.입출력바이트쓰기(0x1f2, 1);
        mobil_VALUE.입출력바이트쓰기(0x1f3, secțiune_VALUE & 255);
        mobil_VALUE.입출력바이트쓰기(0x1f4, (secțiune_VALUE >>> 8) & 255);
        mobil_VALUE.입출력바이트쓰기(0x1f5, 0);
        mobil_VALUE.입출력바이트쓰기(0x1f7, Comandă); 잠깐기다리기();
        return 준비기다리기(true);
    }
    static int Citire(int secțiune_VALUE) {
        int KR = cerere(secțiune_VALUE, 0x20);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++) {
            int VALUE = mobil_VALUE.입출력짧은수읽기(0x1f0);
            secțiune_date[INDEX * 2] = VALUE & 255; secțiune_date[INDEX * 2 + 1] = VALUE >>> 8;
        }
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int Scriere(int secțiune_VALUE) {
        if (!sisteme_de_informații_Activ_9e72441a || secțiune_VALUE < 1 || secțiune_VALUE > 518) return -19;
        int KR = cerere(secțiune_VALUE, 0x30);
        if (KR < 0) return KR;
        for (int INDEX = 0; INDEX < 256; INDEX++)
            mobil_VALUE.입출력짧은수쓰기(0x1f0, secțiune_date[INDEX * 2] | secțiune_date[INDEX * 2 + 1] << 8);
        잠깐기다리기(); return 준비기다리기(false);
    }
    static int 밀어쓰기() {
        if (!sisteme_de_informații_Activ_9e72441a) return -19;
        mobil_VALUE.입출력바이트쓰기(0x1f7, 0xe7); 잠깐기다리기();
        return 준비기다리기(false);
    }
    static int analiza_întreg(int Poziție) {
        return secțiune_date[Poziție] | secțiune_date[Poziție + 1] << 8 | secțiune_date[Poziție + 2] << 16 | secțiune_date[Poziție + 3] << 24;
    }
    static void scriere_întreg_VALUE(int Poziție, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) secțiune_date[Poziție + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
}
