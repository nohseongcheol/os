// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class adat_kommunikáció {
    static int számjegy_ÉRTÉK(String Szöveg) {
        if (Szöveg == null || Szöveg.length() == 0) return -1;
        int KR = 0;
        for (int INDEX = 0; INDEX < Szöveg.length(); INDEX++) {
            int ÉRTÉK = Szöveg.charAt(INDEX) - '0';
            if (ÉRTÉK < 0 || ÉRTÉK > 9 || KR > 6553) return -1;
            KR = KR * 10 + ÉRTÉK;
            if (KR > 65535) return -1;
        }
        return KR;
    }
    static int CÍM(String Szöveg) {
        if (Szöveg == null) return 0;
        int ÉRTÉK = 0, KR = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Szöveg.length(); INDEX++) {
            int 문자 = INDEX == Szöveg.length() ? '.' : Szöveg.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                KR = (KR << 8) | ÉRTÉK; 부분++; ÉRTÉK = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ÉRTÉK = ÉRTÉK * 10 + 문자 - '0';
                if (++자릿수 > 3 || ÉRTÉK > 255) return 0;
            }
        }
        return 부분 == 4 ? KR : 0;
    }
    public static int Futtatás() {
        if (felhasználó.인수개수() != 3) { felhasználó.Írás("Usage: run udp IP PORT TEXT\n"); return 2; }
        int CÍM = CÍM(felhasználó.Argumentumok(0)), port_ÉRTÉK = számjegy_ÉRTÉK(felhasználó.Argumentumok(1));
        String Tartalom_ÉRTÉK = felhasználó.Argumentumok(2);
        if (CÍM == 0 || port_ÉRTÉK < 1 || Tartalom_ÉRTÉK.length() > 1024) { felhasználó.Írás("Bad destination\n"); return 2; }
        int leíró_ÉRTÉK = felhasználó.készít_hálózat(0);
        if (leíró_ÉRTÉK < 0) { felhasználó.Írás("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] adat = new int[1024];
        for (int INDEX = 0; INDEX < Tartalom_ÉRTÉK.length(); INDEX++) adat[INDEX] = Tartalom_ÉRTÉK.charAt(INDEX);
        if (felhasználó.küld_adat(leíró_ÉRTÉK, CÍM, port_ÉRTÉK, adat, Tartalom_ÉRTÉK.length()) < 0) {
            felhasználó.Írás("UDP SEND FAILED\n"); felhasználó.bezár_hálózat(leíró_ÉRTÉK); return 4;
        }
        felhasználó.Írás("UDP SENT\n");
        int KAPOTT_hossz = felhasználó.fogad_adat(leíró_ÉRTÉK, adat, 1500);
        boolean 같음 = KAPOTT_hossz == Tartalom_ÉRTÉK.length() && felhasználó.보낸주소(leíró_ÉRTÉK) == CÍM && felhasználó.보낸창구(leíró_ÉRTÉK) == port_ÉRTÉK;
        if (같음) for (int INDEX = 0; INDEX < KAPOTT_hossz; INDEX++) if (adat[INDEX] != Tartalom_ÉRTÉK.charAt(INDEX)) 같음 = false;
        felhasználó.bezár_hálózat(leíró_ÉRTÉK);
        if (KAPOTT_hossz < 0) { felhasználó.Írás("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        felhasználó.Írás(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
