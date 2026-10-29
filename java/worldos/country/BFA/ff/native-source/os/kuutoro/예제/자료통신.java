// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String binndi) {
        if (binndi == null || binndi.length() == 0) return -1;
        int 결과 = 0;
        for (int joopirdu = 0; joopirdu < binndi.length(); joopirdu++) {
            int njaru = binndi.charAt(joopirdu) - '0';
            if (njaru < 0 || njaru > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + njaru;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int ñiiɓirde(String binndi) {
        if (binndi == null) return 0;
        int njaru = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int joopirdu = 0; joopirdu <= binndi.length(); joopirdu++) {
            int 문자 = joopirdu == binndi.length() ? '.' : binndi.charAt(joopirdu);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | njaru; 부분++; njaru = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                njaru = njaru * 10 + 문자 - '0';
                if (++자릿수 > 3 || njaru > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int huutoraade() {
        if (kuutoro.인수개수() != 3) { kuutoro.winndude("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ñiiɓirde = ñiiɓirde(kuutoro.인수(0)), poor_njaru = 숫자(kuutoro.인수(1));
        String loowdi_njaru = kuutoro.인수(2);
        if (ñiiɓirde == 0 || poor_njaru < 1 || loowdi_njaru.length() > 1024) { kuutoro.winndude("Bad destination\n"); return 2; }
        int jaggoode_njaru = kuutoro.udditde_laylaytol(0);
        if (jaggoode_njaru < 0) { kuutoro.winndude("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] keɓe = new int[1024];
        for (int joopirdu = 0; joopirdu < loowdi_njaru.length(); joopirdu++) keɓe[joopirdu] = loowdi_njaru.charAt(joopirdu);
        if (kuutoro.neldude_keɓe(jaggoode_njaru, ñiiɓirde, poor_njaru, keɓe, loowdi_njaru.length()) < 0) {
            kuutoro.winndude("UDP SEND FAILED\n"); kuutoro.uddude_laylaytol(jaggoode_njaru); return 4;
        }
        kuutoro.winndude("UDP SENT\n");
        int 받은길이 = kuutoro.자료받기(jaggoode_njaru, keɓe, 1500);
        boolean 같음 = 받은길이 == loowdi_njaru.length() && kuutoro.보낸주소(jaggoode_njaru) == ñiiɓirde && kuutoro.보낸창구(jaggoode_njaru) == poor_njaru;
        if (같음) for (int joopirdu = 0; joopirdu < 받은길이; joopirdu++) if (keɓe[joopirdu] != loowdi_njaru.charAt(joopirdu)) 같음 = false;
        kuutoro.uddude_laylaytol(jaggoode_njaru);
        if (받은길이 < 0) { kuutoro.winndude("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        kuutoro.winndude(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
