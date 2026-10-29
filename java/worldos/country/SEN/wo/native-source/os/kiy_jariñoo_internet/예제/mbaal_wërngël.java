// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 tolluwaay/홀수 diir_xëyma 데이터그램으로 liteew_mbir RTL8139 수신 wërngël_xëyma 순환을 시험한다. */
public final class mbaal_wërngël {
    public static int daw() {
        if (kiy_jariñoo_internet.인수개수() != 1) { kiy_jariñoo_internet.biir("Usage: run stress PORT\n"); return 2; }
        String Tekst = kiy_jariñoo_internet.인수(0);
        int jël_xëyma = 0;
        for (int àlluwa_tur = 0; àlluwa_tur < Tekst.length(); àlluwa_tur++) {
            if (Tekst.charAt(àlluwa_tur) < '0' || Tekst.charAt(àlluwa_tur) > '9' || jël_xëyma > 6553) return 2;
            jël_xëyma = jël_xëyma * 10 + Tekst.charAt(àlluwa_tur) - '0';
        }
        if (jël_xëyma < 1 || jël_xëyma > 65535) return 2;
        int yombal_xëyma = kiy_jariñoo_internet.sos_mbaal(0);
        if (yombal_xëyma < 0) return 3;
        int[] mbir = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int diir_xëyma = 1024 - (회차 & 1);
            for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) mbir[àlluwa_tur] = (àlluwa_tur + 회차) & 255;
            if (kiy_jariñoo_internet.Yónnee_mbir(yombal_xëyma, 0x0a000202, jël_xëyma, mbir, diir_xëyma) != diir_xëyma) return 4;
            if (kiy_jariñoo_internet.자료받기(yombal_xëyma, mbir, 300) != diir_xëyma) return 5;
            for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) if (mbir[àlluwa_tur] != ((àlluwa_tur + 회차) & 255)) return 6;
        }
        kiy_jariñoo_internet.Tej_mbaal(yombal_xëyma);
        kiy_jariñoo_internet.biir("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
