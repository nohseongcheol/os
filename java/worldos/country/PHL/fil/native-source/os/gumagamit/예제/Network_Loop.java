// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 sukat_82232621/홀수 haba_VALUE 데이터그램으로 totoo_data RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Network_Loop {
    public static int run() {
        if (gumagamit.인수개수() != 1) { gumagamit.sumulat("Usage: run stress PORT\n"); return 2; }
        String SMS = gumagamit.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + SMS.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int hawakán_VALUE = gumagamit.buksan_Network(0);
        if (hawakán_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int haba_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (gumagamit.i_email_data(hawakán_VALUE, 0x0a000202, port_VALUE, data, haba_VALUE) != haba_VALUE) return 4;
            if (gumagamit.자료받기(hawakán_VALUE, data, 300) != haba_VALUE) return 5;
            for (int INDEX = 0; INDEX < haba_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        gumagamit.isara_Network(hawakán_VALUE);
        gumagamit.sumulat("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
