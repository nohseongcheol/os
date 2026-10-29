// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 d_Gréisst_veränneren/홀수 Längt_VALUE 데이터그램으로 aktuell_Daten RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class Reseau_Loop {
    public static int Laf() {
        if (Benotzer.인수개수() != 1) { Benotzer.schreiwen("Usage: run stress PORT\n"); return 2; }
        String SMS = Benotzer.인수(0);
        int Port_VALUE = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || Port_VALUE > 6553) return 2;
            Port_VALUE = Port_VALUE * 10 + SMS.charAt(INDEX) - '0';
        }
        if (Port_VALUE < 1 || Port_VALUE > 65535) return 2;
        int Handle_VALUE = Benotzer.ariichten_Reseau(0);
        if (Handle_VALUE < 0) return 3;
        int[] Daten = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int Längt_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Daten[INDEX] = (INDEX + 회차) & 255;
            if (Benotzer.mailen_Daten(Handle_VALUE, 0x0a000202, Port_VALUE, Daten, Längt_VALUE) != Längt_VALUE) return 4;
            if (Benotzer.자료받기(Handle_VALUE, Daten, 300) != Längt_VALUE) return 5;
            for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) if (Daten[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        Benotzer.Clôture_Reseau(Handle_VALUE);
        Benotzer.schreiwen("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
