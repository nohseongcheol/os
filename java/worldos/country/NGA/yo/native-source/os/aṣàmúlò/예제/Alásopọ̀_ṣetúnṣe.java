// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ìwọ̀n/홀수 gígùn_iye 데이터그램으로 gangan_détà RTL8139 수신 ṣetúnṣe_iye 순환을 시험한다. */
public final class Alásopọ̀_ṣetúnṣe {
    public static int Rọ́ọ̀nù() {
        if (aṣàmúlò.인수개수() != 1) { aṣàmúlò.Kọ("Usage: run stress PORT\n"); return 2; }
        String SMS = aṣàmúlò.인수(0);
        int ojú_iye = 0;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < SMS.length(); wá_atọ̀ka_àkóónú++) {
            if (SMS.charAt(wá_atọ̀ka_àkóónú) < '0' || SMS.charAt(wá_atọ̀ka_àkóónú) > '9' || ojú_iye > 6553) return 2;
            ojú_iye = ojú_iye * 10 + SMS.charAt(wá_atọ̀ka_àkóónú) - '0';
        }
        if (ojú_iye < 1 || ojú_iye > 65535) return 2;
        int èkù_iye = aṣàmúlò.ṣí_Alásopọ̀(0);
        if (èkù_iye < 0) return 3;
        int[] détà = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int gígùn_iye = 1024 - (회차 & 1);
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) détà[wá_atọ̀ka_àkóónú] = (wá_atọ̀ka_àkóónú + 회차) & 255;
            if (aṣàmúlò.í_meèlì_détà(èkù_iye, 0x0a000202, ojú_iye, détà, gígùn_iye) != gígùn_iye) return 4;
            if (aṣàmúlò.자료받기(èkù_iye, détà, 300) != gígùn_iye) return 5;
            for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < gígùn_iye; wá_atọ̀ka_àkóónú++) if (détà[wá_atọ̀ka_àkóónú] != ((wá_atọ̀ka_àkóónú + 회차) & 255)) return 6;
        }
        aṣàmúlò.pa_dé_Alásopọ̀(èkù_iye);
        aṣàmúlò.Kọ("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
