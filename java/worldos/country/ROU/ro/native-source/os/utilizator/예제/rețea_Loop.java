// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Mărime/홀수 lungime_VALUE 데이터그램으로 real_date RTL8139 primi_VALUE Loop_VALUE 순환을 시험한다. */
public final class rețea_Loop {
    public static int Pornește() {
        if (utilizator.인수개수() != 1) { utilizator.Scriere("Usage: run stress PORT\n"); return 2; }
        String SMS = utilizator.Argumente(0);
        int muta_VALUE = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || muta_VALUE > 6553) return 2;
            muta_VALUE = muta_VALUE * 10 + SMS.charAt(INDEX) - '0';
        }
        if (muta_VALUE < 1 || muta_VALUE > 65535) return 2;
        int handle_VALUE = utilizator.crea_rețea(0);
        if (handle_VALUE < 0) return 3;
        int[] date = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int lungime_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) date[INDEX] = (INDEX + 회차) & 255;
            if (utilizator.trimite_date(handle_VALUE, 0x0a000202, muta_VALUE, date, lungime_VALUE) != lungime_VALUE) return 4;
            if (utilizator.primi_date(handle_VALUE, date, 300) != lungime_VALUE) return 5;
            for (int INDEX = 0; INDEX < lungime_VALUE; INDEX++) if (date[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        utilizator.închide_rețea(handle_VALUE);
        utilizator.Scriere("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
