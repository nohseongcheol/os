// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int idijithi_inani(String Itekisi) {
        if (Itekisi == null || Itekisi.length() == 0) return -1;
        int 결과 = 0;
        for (int thola_inkomba = 0; thola_inkomba < Itekisi.length(); thola_inkomba++) {
            int inani = Itekisi.charAt(thola_inkomba) - '0';
            if (inani < 0 || inani > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + inani;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int ikheli(String Itekisi) {
        if (Itekisi == null) return 0;
        int inani = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int thola_inkomba = 0; thola_inkomba <= Itekisi.length(); thola_inkomba++) {
            int 문자 = thola_inkomba == Itekisi.length() ? '.' : Itekisi.charAt(thola_inkomba);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | inani; 부분++; inani = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                inani = inani * 10 + 문자 - '0';
                if (++자릿수 > 3 || inani > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int Sebenzisa() {
        if (umsebenzisi.인수개수() != 3) { umsebenzisi.Bhala("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ikheli = ikheli(umsebenzisi.인수(0)), intuba_inani = idijithi_inani(umsebenzisi.인수(1));
        String Okuqukethwe_inani = umsebenzisi.인수(2);
        if (ikheli == 0 || intuba_inani < 1 || Okuqukethwe_inani.length() > 1024) { umsebenzisi.Bhala("Bad destination\n"); return 2; }
        int isibambo_inani = umsebenzisi.vula_iNethiwekhi(0);
        if (isibambo_inani < 0) { umsebenzisi.Bhala("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] imininingwane = new int[1024];
        for (int thola_inkomba = 0; thola_inkomba < Okuqukethwe_inani.length(); thola_inkomba++) imininingwane[thola_inkomba] = Okuqukethwe_inani.charAt(thola_inkomba);
        if (umsebenzisi.Thumela_imininingwane(isibambo_inani, ikheli, intuba_inani, imininingwane, Okuqukethwe_inani.length()) < 0) {
            umsebenzisi.Bhala("UDP SEND FAILED\n"); umsebenzisi.vala_iNethiwekhi(isibambo_inani); return 4;
        }
        umsebenzisi.Bhala("UDP SENT\n");
        int 받은길이 = umsebenzisi.자료받기(isibambo_inani, imininingwane, 1500);
        boolean 같음 = 받은길이 == Okuqukethwe_inani.length() && umsebenzisi.보낸주소(isibambo_inani) == ikheli && umsebenzisi.보낸창구(isibambo_inani) == intuba_inani;
        if (같음) for (int thola_inkomba = 0; thola_inkomba < 받은길이; thola_inkomba++) if (imininingwane[thola_inkomba] != Okuqukethwe_inani.charAt(thola_inkomba)) 같음 = false;
        umsebenzisi.vala_iNethiwekhi(isibambo_inani);
        if (받은길이 < 0) { umsebenzisi.Bhala("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        umsebenzisi.Bhala(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
