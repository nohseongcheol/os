// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Maint/홀수 hyd_VALUE 데이터그램으로 go_iawn_data RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Rhwydwaith_Loop {
    public static int Gweithredu_2() {
        if (defnyddiwr.인수개수() != 1) { defnyddiwr.Ysgrifennu("Usage: run stress PORT\n"); return 2; }
        String Testun = defnyddiwr.인수(0);
        int porth_VALUE = 0;
        for (int INDEX = 0; INDEX < Testun.length(); INDEX++) {
            if (Testun.charAt(INDEX) < '0' || Testun.charAt(INDEX) > '9' || porth_VALUE > 6553) return 2;
            porth_VALUE = porth_VALUE * 10 + Testun.charAt(INDEX) - '0';
        }
        if (porth_VALUE < 1 || porth_VALUE > 65535) return 2;
        int dolen_VALUE = defnyddiwr.agor_Rhwydwaith(0);
        if (dolen_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int hyd_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (defnyddiwr.anfon_data(dolen_VALUE, 0x0a000202, porth_VALUE, data, hyd_VALUE) != hyd_VALUE) return 4;
            if (defnyddiwr.자료받기(dolen_VALUE, data, 300) != hyd_VALUE) return 5;
            for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        defnyddiwr.cau_Rhwydwaith(dolen_VALUE);
        defnyddiwr.Ysgrifennu("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
