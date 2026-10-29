// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Tamaina/홀수 luzera_balio 데이터그램으로 benetako_datuak RTL8139 수신 Loop_balio 순환을 시험한다. */
public final class sare_Loop {
    public static int Exekutatu_2() {
        if (erabiltzaile.인수개수() != 1) { erabiltzaile.Idatzi("Usage: run stress PORT\n"); return 2; }
        String Testua = erabiltzaile.Argumentuak(0);
        int ataka_balio = 0;
        for (int INDIZE = 0; INDIZE < Testua.length(); INDIZE++) {
            if (Testua.charAt(INDIZE) < '0' || Testua.charAt(INDIZE) > '9' || ataka_balio > 6553) return 2;
            ataka_balio = ataka_balio * 10 + Testua.charAt(INDIZE) - '0';
        }
        if (ataka_balio < 1 || ataka_balio > 65535) return 2;
        int helduleku_balio = erabiltzaile.ireki_sare(0);
        if (helduleku_balio < 0) return 3;
        int[] datuak = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int luzera_balio = 1024 - (회차 & 1);
            for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) datuak[INDIZE] = (INDIZE + 회차) & 255;
            if (erabiltzaile.bidali_datuak(helduleku_balio, 0x0a000202, ataka_balio, datuak, luzera_balio) != luzera_balio) return 4;
            if (erabiltzaile.자료받기(helduleku_balio, datuak, 300) != luzera_balio) return 5;
            for (int INDIZE = 0; INDIZE < luzera_balio; INDIZE++) if (datuak[INDIZE] != ((INDIZE + 회차) & 255)) return 6;
        }
        erabiltzaile.itxi_sare(helduleku_balio);
        erabiltzaile.Idatzi("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
