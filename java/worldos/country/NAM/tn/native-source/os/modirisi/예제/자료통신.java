// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int dijite_Boleng(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int 결과 = 0;
        for (int tshupane = 0; tshupane < SMS.length(); tshupane++) {
            int Boleng = SMS.charAt(tshupane) - '0';
            if (Boleng < 0 || Boleng > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + Boleng;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int aterese(String SMS) {
        if (SMS == null) return 0;
        int Boleng = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int tshupane = 0; tshupane <= SMS.length(); tshupane++) {
            int 문자 = tshupane == SMS.length() ? '.' : SMS.charAt(tshupane);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | Boleng; 부분++; Boleng = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                Boleng = Boleng * 10 + 문자 - '0';
                if (++자릿수 > 3 || Boleng > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int dirisa() {
        if (modirisi.인수개수() != 3) { modirisi.kwala("Usage: run udp IP PORT TEXT\n"); return 2; }
        int aterese = aterese(modirisi.인수(0)), gorogisetsa_Boleng = dijite_Boleng(modirisi.인수(1));
        String Diteng_Boleng = modirisi.인수(2);
        if (aterese == 0 || gorogisetsa_Boleng < 1 || Diteng_Boleng.length() > 1024) { modirisi.kwala("Bad destination\n"); return 2; }
        int mokgwakamogelo_Boleng = modirisi.bula_Neteweke(0);
        if (mokgwakamogelo_Boleng < 0) { modirisi.kwala("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] tshedimosetso = new int[1024];
        for (int tshupane = 0; tshupane < Diteng_Boleng.length(); tshupane++) tshedimosetso[tshupane] = Diteng_Boleng.charAt(tshupane);
        if (modirisi.romela_tshedimosetso(mokgwakamogelo_Boleng, aterese, gorogisetsa_Boleng, tshedimosetso, Diteng_Boleng.length()) < 0) {
            modirisi.kwala("UDP SEND FAILED\n"); modirisi.tswala_Neteweke(mokgwakamogelo_Boleng); return 4;
        }
        modirisi.kwala("UDP SENT\n");
        int 받은길이 = modirisi.자료받기(mokgwakamogelo_Boleng, tshedimosetso, 1500);
        boolean 같음 = 받은길이 == Diteng_Boleng.length() && modirisi.보낸주소(mokgwakamogelo_Boleng) == aterese && modirisi.보낸창구(mokgwakamogelo_Boleng) == gorogisetsa_Boleng;
        if (같음) for (int tshupane = 0; tshupane < 받은길이; tshupane++) if (tshedimosetso[tshupane] != Diteng_Boleng.charAt(tshupane)) 같음 = false;
        modirisi.tswala_Neteweke(mokgwakamogelo_Boleng);
        if (받은길이 < 0) { modirisi.kwala("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        modirisi.kwala(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
