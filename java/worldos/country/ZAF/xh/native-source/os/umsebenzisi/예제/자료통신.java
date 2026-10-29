// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int inani_ixabiso(String Umbhalo) {
        if (Umbhalo == null || Umbhalo.length() == 0) return -1;
        int 결과 = 0;
        for (int indeksa = 0; indeksa < Umbhalo.length(); indeksa++) {
            int ixabiso = Umbhalo.charAt(indeksa) - '0';
            if (ixabiso < 0 || ixabiso > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + ixabiso;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int idilesi(String Umbhalo) {
        if (Umbhalo == null) return 0;
        int ixabiso = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int indeksa = 0; indeksa <= Umbhalo.length(); indeksa++) {
            int 문자 = indeksa == Umbhalo.length() ? '.' : Umbhalo.charAt(indeksa);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | ixabiso; 부분++; ixabiso = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ixabiso = ixabiso * 10 + 문자 - '0';
                if (++자릿수 > 3 || ixabiso > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Phumeza() {
        if (umsebenzisi.인수개수() != 3) { umsebenzisi.Bhala("Usage: run udp IP PORT TEXT\n"); return 2; }
        int idilesi = idilesi(umsebenzisi.인수(0)), iphothi_ixabiso = inani_ixabiso(umsebenzisi.인수(1));
        String Isiqulatho_ixabiso = umsebenzisi.인수(2);
        if (idilesi == 0 || iphothi_ixabiso < 1 || Isiqulatho_ixabiso.length() > 1024) { umsebenzisi.Bhala("Bad destination\n"); return 2; }
        int isibambi_ixabiso = umsebenzisi.vula_Inethiwekhi(0);
        if (isibambi_ixabiso < 0) { umsebenzisi.Bhala("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] iingcombolo = new int[1024];
        for (int indeksa = 0; indeksa < Isiqulatho_ixabiso.length(); indeksa++) iingcombolo[indeksa] = Isiqulatho_ixabiso.charAt(indeksa);
        if (umsebenzisi.thumela_iingcombolo(isibambi_ixabiso, idilesi, iphothi_ixabiso, iingcombolo, Isiqulatho_ixabiso.length()) < 0) {
            umsebenzisi.Bhala("UDP SEND FAILED\n"); umsebenzisi.vala_Inethiwekhi(isibambi_ixabiso); return 4;
        }
        umsebenzisi.Bhala("UDP SENT\n");
        int 받은길이 = umsebenzisi.자료받기(isibambi_ixabiso, iingcombolo, 1500);
        boolean 같음 = 받은길이 == Isiqulatho_ixabiso.length() && umsebenzisi.보낸주소(isibambi_ixabiso) == idilesi && umsebenzisi.보낸창구(isibambi_ixabiso) == iphothi_ixabiso;
        if (같음) for (int indeksa = 0; indeksa < 받은길이; indeksa++) if (iingcombolo[indeksa] != Isiqulatho_ixabiso.charAt(indeksa)) 같음 = false;
        umsebenzisi.vala_Inethiwekhi(isibambi_ixabiso);
        if (받은길이 < 0) { umsebenzisi.Bhala("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        umsebenzisi.Bhala(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
