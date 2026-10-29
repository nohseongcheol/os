// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 daqqas/홀수 tul_VALUE 데이터그램으로 attwali_data RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class netwerk_Loop {
    public static int serje() {
        if (utent.인수개수() != 1) { utent.kiteb("Usage: run stress PORT\n"); return 2; }
        String SMS = utent.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + SMS.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int handle_VALUE = utent.fetaħ_netwerk(0);
        if (handle_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int tul_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (utent.bagħat_data(handle_VALUE, 0x0a000202, port_VALUE, data, tul_VALUE) != tul_VALUE) return 4;
            if (utent.자료받기(handle_VALUE, data, 300) != tul_VALUE) return 5;
            for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        utent.agħlaq_netwerk(handle_VALUE);
        utent.kiteb("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
