// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Madhësi/홀수 gjatësi_VALUE 데이터그램으로 aktual_të_dhëna RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class rrjet_Loop {
    public static int Ekzekuto() {
        if (përdorues.인수개수() != 1) { përdorues.Shkrimi("Usage: run stress PORT\n"); return 2; }
        String Teksti = përdorues.Argumente(0);
        int portë_VALUE = 0;
        for (int INDEX = 0; INDEX < Teksti.length(); INDEX++) {
            if (Teksti.charAt(INDEX) < '0' || Teksti.charAt(INDEX) > '9' || portë_VALUE > 6553) return 2;
            portë_VALUE = portë_VALUE * 10 + Teksti.charAt(INDEX) - '0';
        }
        if (portë_VALUE < 1 || portë_VALUE > 65535) return 2;
        int dorezë_VALUE = përdorues.hap_rrjet(0);
        if (dorezë_VALUE < 0) return 3;
        int[] të_dhëna = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int gjatësi_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) të_dhëna[INDEX] = (INDEX + 회차) & 255;
            if (përdorues.dërgoj_të_dhëna(dorezë_VALUE, 0x0a000202, portë_VALUE, të_dhëna, gjatësi_VALUE) != gjatësi_VALUE) return 4;
            if (përdorues.자료받기(dorezë_VALUE, të_dhëna, 300) != gjatësi_VALUE) return 5;
            for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) if (të_dhëna[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        përdorues.mbyll_rrjet(dorezë_VALUE);
        përdorues.Shkrimi("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
