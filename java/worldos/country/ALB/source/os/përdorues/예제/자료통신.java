// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int shifër_VALUE(String Teksti) {
        if (Teksti == null || Teksti.length() == 0) return -1;
        int llogaritje = 0;
        for (int INDEX = 0; INDEX < Teksti.length(); INDEX++) {
            int VALUE = Teksti.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || llogaritje > 6553) return -1;
            llogaritje = llogaritje * 10 + VALUE;
            if (llogaritje > 65535) return -1;
        }
        return llogaritje;
    }
    static int email(String Teksti) {
        if (Teksti == null) return 0;
        int VALUE = 0, llogaritje = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Teksti.length(); INDEX++) {
            int 문자 = INDEX == Teksti.length() ? '.' : Teksti.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                llogaritje = (llogaritje << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? llogaritje : 0;
    }
    public static int Ekzekuto() {
        if (përdorues.인수개수() != 3) { përdorues.Shkrimi("Usage: run udp IP PORT TEXT\n"); return 2; }
        int email = email(përdorues.Argumente(0)), portë_VALUE = shifër_VALUE(përdorues.Argumente(1));
        String Përmbajtje_VALUE = përdorues.Argumente(2);
        if (email == 0 || portë_VALUE < 1 || Përmbajtje_VALUE.length() > 1024) { përdorues.Shkrimi("Bad destination\n"); return 2; }
        int dorezë_VALUE = përdorues.hap_rrjet(0);
        if (dorezë_VALUE < 0) { përdorues.Shkrimi("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] të_dhëna = new int[1024];
        for (int INDEX = 0; INDEX < Përmbajtje_VALUE.length(); INDEX++) të_dhëna[INDEX] = Përmbajtje_VALUE.charAt(INDEX);
        if (përdorues.dërgoj_të_dhëna(dorezë_VALUE, email, portë_VALUE, të_dhëna, Përmbajtje_VALUE.length()) < 0) {
            përdorues.Shkrimi("UDP SEND FAILED\n"); përdorues.mbyll_rrjet(dorezë_VALUE); return 4;
        }
        përdorues.Shkrimi("UDP SENT\n");
        int RECEIVED_gjatësi = përdorues.자료받기(dorezë_VALUE, të_dhëna, 1500);
        boolean 같음 = RECEIVED_gjatësi == Përmbajtje_VALUE.length() && përdorues.보낸주소(dorezë_VALUE) == email && përdorues.보낸창구(dorezë_VALUE) == portë_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_gjatësi; INDEX++) if (të_dhëna[INDEX] != Përmbajtje_VALUE.charAt(INDEX)) 같음 = false;
        përdorues.mbyll_rrjet(dorezë_VALUE);
        if (RECEIVED_gjatësi < 0) { përdorues.Shkrimi("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        përdorues.Shkrimi(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
