// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 lekanya/홀수 boleele_Boleng 데이터그램으로 tota_tshedimosetso RTL8139 수신 lupu_Boleng 순환을 시험한다. */
public final class Neteweke_lupu {
    public static int dirisa() {
        if (modirisi.인수개수() != 1) { modirisi.kwala("Usage: run stress PORT\n"); return 2; }
        String SMS = modirisi.인수(0);
        int gorogisetsa_Boleng = 0;
        for (int tshupane = 0; tshupane < SMS.length(); tshupane++) {
            if (SMS.charAt(tshupane) < '0' || SMS.charAt(tshupane) > '9' || gorogisetsa_Boleng > 6553) return 2;
            gorogisetsa_Boleng = gorogisetsa_Boleng * 10 + SMS.charAt(tshupane) - '0';
        }
        if (gorogisetsa_Boleng < 1 || gorogisetsa_Boleng > 65535) return 2;
        int mokgwakamogelo_Boleng = modirisi.bula_Neteweke(0);
        if (mokgwakamogelo_Boleng < 0) return 3;
        int[] tshedimosetso = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int boleele_Boleng = 1024 - (회차 & 1);
            for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) tshedimosetso[tshupane] = (tshupane + 회차) & 255;
            if (modirisi.romela_tshedimosetso(mokgwakamogelo_Boleng, 0x0a000202, gorogisetsa_Boleng, tshedimosetso, boleele_Boleng) != boleele_Boleng) return 4;
            if (modirisi.자료받기(mokgwakamogelo_Boleng, tshedimosetso, 300) != boleele_Boleng) return 5;
            for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) if (tshedimosetso[tshupane] != ((tshupane + 회차) & 255)) return 6;
        }
        modirisi.tswala_Neteweke(mokgwakamogelo_Boleng);
        modirisi.kwala("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
