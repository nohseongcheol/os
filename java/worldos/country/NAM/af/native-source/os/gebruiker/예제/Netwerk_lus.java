// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Grootte/홀수 lengte_VALUE 데이터그램으로 werklik_data RTL8139 수신 lus_VALUE 순환을 시험한다. */
public final class Netwerk_lus {
    public static int Loop() {
        if (gebruiker.인수개수() != 1) { gebruiker.Skryf("Usage: run stress PORT\n"); return 2; }
        String Teks = gebruiker.인수(0);
        int ombou_VALUE = 0;
        for (int INDEX = 0; INDEX < Teks.length(); INDEX++) {
            if (Teks.charAt(INDEX) < '0' || Teks.charAt(INDEX) > '9' || ombou_VALUE > 6553) return 2;
            ombou_VALUE = ombou_VALUE * 10 + Teks.charAt(INDEX) - '0';
        }
        if (ombou_VALUE < 1 || ombou_VALUE > 65535) return 2;
        int handvatsel_VALUE = gebruiker.skep_Netwerk(0);
        if (handvatsel_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int lengte_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (gebruiker.e_pos_data(handvatsel_VALUE, 0x0a000202, ombou_VALUE, data, lengte_VALUE) != lengte_VALUE) return 4;
            if (gebruiker.자료받기(handvatsel_VALUE, data, 300) != lengte_VALUE) return 5;
            for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        gebruiker.sluit_Netwerk(handvatsel_VALUE);
        gebruiker.Skryf("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
