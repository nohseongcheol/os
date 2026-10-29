// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int siifar_xëyma(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int 결과 = 0;
        for (int àlluwa_tur = 0; àlluwa_tur < Tekst.length(); àlluwa_tur++) {
            int xëyma = Tekst.charAt(àlluwa_tur) - '0';
            if (xëyma < 0 || xëyma > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + xëyma;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int dëkkuwaay(String Tekst) {
        if (Tekst == null) return 0;
        int xëyma = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int àlluwa_tur = 0; àlluwa_tur <= Tekst.length(); àlluwa_tur++) {
            int 문자 = àlluwa_tur == Tekst.length() ? '.' : Tekst.charAt(àlluwa_tur);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | xëyma; 부분++; xëyma = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                xëyma = xëyma * 10 + 문자 - '0';
                if (++자릿수 > 3 || xëyma > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int daw() {
        if (kiy_jariñoo_internet.인수개수() != 3) { kiy_jariñoo_internet.biir("Usage: run udp IP PORT TEXT\n"); return 2; }
        int dëkkuwaay = dëkkuwaay(kiy_jariñoo_internet.인수(0)), jël_xëyma = siifar_xëyma(kiy_jariñoo_internet.인수(1));
        String Këmb_xëyma = kiy_jariñoo_internet.인수(2);
        if (dëkkuwaay == 0 || jël_xëyma < 1 || Këmb_xëyma.length() > 1024) { kiy_jariñoo_internet.biir("Bad destination\n"); return 2; }
        int yombal_xëyma = kiy_jariñoo_internet.sos_mbaal(0);
        if (yombal_xëyma < 0) { kiy_jariñoo_internet.biir("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] mbir = new int[1024];
        for (int àlluwa_tur = 0; àlluwa_tur < Këmb_xëyma.length(); àlluwa_tur++) mbir[àlluwa_tur] = Këmb_xëyma.charAt(àlluwa_tur);
        if (kiy_jariñoo_internet.Yónnee_mbir(yombal_xëyma, dëkkuwaay, jël_xëyma, mbir, Këmb_xëyma.length()) < 0) {
            kiy_jariñoo_internet.biir("UDP SEND FAILED\n"); kiy_jariñoo_internet.Tej_mbaal(yombal_xëyma); return 4;
        }
        kiy_jariñoo_internet.biir("UDP SENT\n");
        int 받은길이 = kiy_jariñoo_internet.자료받기(yombal_xëyma, mbir, 1500);
        boolean 같음 = 받은길이 == Këmb_xëyma.length() && kiy_jariñoo_internet.보낸주소(yombal_xëyma) == dëkkuwaay && kiy_jariñoo_internet.보낸창구(yombal_xëyma) == jël_xëyma;
        if (같음) for (int àlluwa_tur = 0; àlluwa_tur < 받은길이; àlluwa_tur++) if (mbir[àlluwa_tur] != Këmb_xëyma.charAt(àlluwa_tur)) 같음 = false;
        kiy_jariñoo_internet.Tej_mbaal(yombal_xëyma);
        if (받은길이 < 0) { kiy_jariñoo_internet.biir("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        kiy_jariñoo_internet.biir(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
