// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 atharraich_am_meud/홀수 faid_VALUE 데이터그램으로 dearbh_dàta RTL8139 수신 lùb_VALUE 순환을 시험한다. */
public final class lìonra_lùb {
    public static int ruith() {
        if (cleachdaiche.인수개수() != 1) { cleachdaiche.sgrìobh("Usage: run stress PORT\n"); return 2; }
        String SMS = cleachdaiche.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + SMS.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int làmhrachan_VALUE = cleachdaiche.fosgail_lìonra(0);
        if (làmhrachan_VALUE < 0) return 3;
        int[] dàta = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int faid_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) dàta[INDEX] = (INDEX + 회차) & 255;
            if (cleachdaiche.cuir_dàta(làmhrachan_VALUE, 0x0a000202, port_VALUE, dàta, faid_VALUE) != faid_VALUE) return 4;
            if (cleachdaiche.자료받기(làmhrachan_VALUE, dàta, 300) != faid_VALUE) return 5;
            for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) if (dàta[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        cleachdaiche.dùin_lìonra(làmhrachan_VALUE);
        cleachdaiche.sgrìobh("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
