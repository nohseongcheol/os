// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Méid/홀수 fad_VALUE 데이터그램으로 iarbhír_sonraí RTL8139 수신 lúb_VALUE 순환을 시험한다. */
public final class Líonra_lúb {
    public static int Rith_2() {
        if (úsáideoir.인수개수() != 1) { úsáideoir.Scríobh("Usage: run stress PORT\n"); return 2; }
        String Téacs = úsáideoir.Argóintí(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Téacs.length(); INDEX++) {
            if (Téacs.charAt(INDEX) < '0' || Téacs.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Téacs.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int hanla_VALUE = úsáideoir.oscail_Líonra(0);
        if (hanla_VALUE < 0) return 3;
        int[] sonraí = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int fad_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) sonraí[INDEX] = (INDEX + 회차) & 255;
            if (úsáideoir.seol_sonraí(hanla_VALUE, 0x0a000202, port_VALUE, sonraí, fad_VALUE) != fad_VALUE) return 4;
            if (úsáideoir.자료받기(hanla_VALUE, sonraí, 300) != fad_VALUE) return 5;
            for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) if (sonraí[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        úsáideoir.dún_Líonra(hanla_VALUE);
        úsáideoir.Scríobh("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
