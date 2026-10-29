// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Bogolo/홀수 botelele_boleng 데이터그램으로 kgonthe_data RTL8139 수신 ditaelopoeletšwa_boleng 순환을 시험한다. */
public final class Netweke_ditaelopoeletšwa {
    public static int Diriša() {
        if (mošomiši.인수개수() != 1) { mošomiši.Ngwala("Usage: run stress PORT\n"); return 2; }
        String Sengwalwa = mošomiši.인수(0);
        int phote_boleng = 0;
        for (int lokela = 0; lokela < Sengwalwa.length(); lokela++) {
            if (Sengwalwa.charAt(lokela) < '0' || Sengwalwa.charAt(lokela) > '9' || phote_boleng > 6553) return 2;
            phote_boleng = phote_boleng * 10 + Sengwalwa.charAt(lokela) - '0';
        }
        if (phote_boleng < 1 || phote_boleng > 65535) return 2;
        int tshwaro_boleng = mošomiši.bula_Netweke(0);
        if (tshwaro_boleng < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int botelele_boleng = 1024 - (회차 & 1);
            for (int lokela = 0; lokela < botelele_boleng; lokela++) data[lokela] = (lokela + 회차) & 255;
            if (mošomiši.Romela_data(tshwaro_boleng, 0x0a000202, phote_boleng, data, botelele_boleng) != botelele_boleng) return 4;
            if (mošomiši.자료받기(tshwaro_boleng, data, 300) != botelele_boleng) return 5;
            for (int lokela = 0; lokela < botelele_boleng; lokela++) if (data[lokela] != ((lokela + 회차) & 255)) return 6;
        }
        mošomiši.tswalela_Netweke(tshwaro_boleng);
        mošomiši.Ngwala("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
