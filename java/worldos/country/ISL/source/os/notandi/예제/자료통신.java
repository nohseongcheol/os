// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int tölustafur_VALUE(String Texti) {
        if (Texti == null || Texti.length() == 0) return -1;
        int NIÐURSTAÐA = 0;
        for (int INDEX = 0; INDEX < Texti.length(); INDEX++) {
            int VALUE = Texti.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || NIÐURSTAÐA > 6553) return -1;
            NIÐURSTAÐA = NIÐURSTAÐA * 10 + VALUE;
            if (NIÐURSTAÐA > 65535) return -1;
        }
        return NIÐURSTAÐA;
    }
    static int slóð(String Texti) {
        if (Texti == null) return 0;
        int VALUE = 0, NIÐURSTAÐA = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Texti.length(); INDEX++) {
            int 문자 = INDEX == Texti.length() ? '.' : Texti.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                NIÐURSTAÐA = (NIÐURSTAÐA << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? NIÐURSTAÐA : 0;
    }
    public static int Keyra_2() {
        if (notandi.인수개수() != 3) { notandi.Skrift("Usage: run udp IP PORT TEXT\n"); return 2; }
        int slóð = slóð(notandi.Viðföng(0)), gátt_VALUE = tölustafur_VALUE(notandi.Viðföng(1));
        String Efni_VALUE = notandi.Viðföng(2);
        if (slóð == 0 || gátt_VALUE < 1 || Efni_VALUE.length() > 1024) { notandi.Skrift("Bad destination\n"); return 2; }
        int hald_VALUE = notandi.opið_Net(0);
        if (hald_VALUE < 0) { notandi.Skrift("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] gögn = new int[1024];
        for (int INDEX = 0; INDEX < Efni_VALUE.length(); INDEX++) gögn[INDEX] = Efni_VALUE.charAt(INDEX);
        if (notandi.senda_gögn(hald_VALUE, slóð, gátt_VALUE, gögn, Efni_VALUE.length()) < 0) {
            notandi.Skrift("UDP SEND FAILED\n"); notandi.loka_Net(hald_VALUE); return 4;
        }
        notandi.Skrift("UDP SENT\n");
        int RECEIVED_lengd = notandi.자료받기(hald_VALUE, gögn, 1500);
        boolean 같음 = RECEIVED_lengd == Efni_VALUE.length() && notandi.보낸주소(hald_VALUE) == slóð && notandi.보낸창구(hald_VALUE) == gátt_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_lengd; INDEX++) if (gögn[INDEX] != Efni_VALUE.charAt(INDEX)) 같음 = false;
        notandi.loka_Net(hald_VALUE);
        if (RECEIVED_lengd < 0) { notandi.Skrift("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        notandi.Skrift(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
