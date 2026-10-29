// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Storleik/홀수 lengd_VALUE 데이터그램으로 faktisk_data RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Nettverk_Loop {
    public static int Køyr_2() {
        if (brukar.인수개수() != 1) { brukar.Skriv("Usage: run stress PORT\n"); return 2; }
        String Tekst = brukar.Argument(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            if (Tekst.charAt(INDEX) < '0' || Tekst.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Tekst.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int handtak_VALUE = brukar.opne_Nettverk(0);
        if (handtak_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int lengd_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (brukar.sende_data(handtak_VALUE, 0x0a000202, port_VALUE, data, lengd_VALUE) != lengd_VALUE) return 4;
            if (brukar.자료받기(handtak_VALUE, data, 300) != lengd_VALUE) return 5;
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        brukar.Lukk_Nettverk(handtak_VALUE);
        brukar.Skriv("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
