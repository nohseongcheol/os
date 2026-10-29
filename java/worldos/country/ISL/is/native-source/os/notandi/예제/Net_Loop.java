// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Stærð/홀수 lengd_VALUE 데이터그램으로 raun_gögn RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Net_Loop {
    public static int Keyra_2() {
        if (notandi.인수개수() != 1) { notandi.Skrift("Usage: run stress PORT\n"); return 2; }
        String Texti = notandi.Viðföng(0);
        int gátt_VALUE = 0;
        for (int INDEX = 0; INDEX < Texti.length(); INDEX++) {
            if (Texti.charAt(INDEX) < '0' || Texti.charAt(INDEX) > '9' || gátt_VALUE > 6553) return 2;
            gátt_VALUE = gátt_VALUE * 10 + Texti.charAt(INDEX) - '0';
        }
        if (gátt_VALUE < 1 || gátt_VALUE > 65535) return 2;
        int hald_VALUE = notandi.opið_Net(0);
        if (hald_VALUE < 0) return 3;
        int[] gögn = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int lengd_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) gögn[INDEX] = (INDEX + 회차) & 255;
            if (notandi.senda_gögn(hald_VALUE, 0x0a000202, gátt_VALUE, gögn, lengd_VALUE) != lengd_VALUE) return 4;
            if (notandi.자료받기(hald_VALUE, gögn, 300) != lengd_VALUE) return 5;
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) if (gögn[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        notandi.loka_Net(hald_VALUE);
        notandi.Skrift("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
