// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int díjììtì_iye(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int 결과 = 0;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < SMS.length(); wá_atọ̀ka_àkóónú++) {
            int iye = SMS.charAt(wá_atọ̀ka_àkóónú) - '0';
            if (iye < 0 || iye > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + iye;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int àdírẹ́ẹ̀sì(String SMS) {
        if (SMS == null) return 0;
        int iye = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú <= SMS.length(); wá_atọ̀ka_àkóónú++) {
            int 문자 = wá_atọ̀ka_àkóónú == SMS.length() ? '.' : SMS.charAt(wá_atọ̀ka_àkóónú);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | iye; 부분++; iye = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                iye = iye * 10 + 문자 - '0';
                if (++자릿수 > 3 || iye > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Rọ́ọ̀nù() {
        if (aṣàmúlò.인수개수() != 3) { aṣàmúlò.Kọ("Usage: run udp IP PORT TEXT\n"); return 2; }
        int àdírẹ́ẹ̀sì = àdírẹ́ẹ̀sì(aṣàmúlò.인수(0)), ojú_iye = díjììtì_iye(aṣàmúlò.인수(1));
        String Àkóónú_iye = aṣàmúlò.인수(2);
        if (àdírẹ́ẹ̀sì == 0 || ojú_iye < 1 || Àkóónú_iye.length() > 1024) { aṣàmúlò.Kọ("Bad destination\n"); return 2; }
        int èkù_iye = aṣàmúlò.ṣí_Alásopọ̀(0);
        if (èkù_iye < 0) { aṣàmúlò.Kọ("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] détà = new int[1024];
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < Àkóónú_iye.length(); wá_atọ̀ka_àkóónú++) détà[wá_atọ̀ka_àkóónú] = Àkóónú_iye.charAt(wá_atọ̀ka_àkóónú);
        if (aṣàmúlò.í_meèlì_détà(èkù_iye, àdírẹ́ẹ̀sì, ojú_iye, détà, Àkóónú_iye.length()) < 0) {
            aṣàmúlò.Kọ("UDP SEND FAILED\n"); aṣàmúlò.pa_dé_Alásopọ̀(èkù_iye); return 4;
        }
        aṣàmúlò.Kọ("UDP SENT\n");
        int 받은길이 = aṣàmúlò.자료받기(èkù_iye, détà, 1500);
        boolean 같음 = 받은길이 == Àkóónú_iye.length() && aṣàmúlò.보낸주소(èkù_iye) == àdírẹ́ẹ̀sì && aṣàmúlò.보낸창구(èkù_iye) == ojú_iye;
        if (같음) for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 받은길이; wá_atọ̀ka_àkóónú++) if (détà[wá_atọ̀ka_àkóónú] != Àkóónú_iye.charAt(wá_atọ̀ka_àkóónú)) 같음 = false;
        aṣàmúlò.pa_dé_Alásopọ̀(èkù_iye);
        if (받은길이 < 0) { aṣàmúlò.Kọ("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        aṣàmúlò.Kọ(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
