// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ubungako/홀수 ubude_inani 데이터그램으로 ulwazi_ngokwenzekile_imininingwane RTL8139 수신 iluphu_inani 순환을 시험한다. */
public final class iNethiwekhi_iluphu {
    public static int Sebenzisa() {
        if (umsebenzisi.인수개수() != 1) { umsebenzisi.Bhala("Usage: run stress PORT\n"); return 2; }
        String Itekisi = umsebenzisi.인수(0);
        int intuba_inani = 0;
        for (int thola_inkomba = 0; thola_inkomba < Itekisi.length(); thola_inkomba++) {
            if (Itekisi.charAt(thola_inkomba) < '0' || Itekisi.charAt(thola_inkomba) > '9' || intuba_inani > 6553) return 2;
            intuba_inani = intuba_inani * 10 + Itekisi.charAt(thola_inkomba) - '0';
        }
        if (intuba_inani < 1 || intuba_inani > 65535) return 2;
        int isibambo_inani = umsebenzisi.vula_iNethiwekhi(0);
        if (isibambo_inani < 0) return 3;
        int[] imininingwane = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int ubude_inani = 1024 - (회차 & 1);
            for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) imininingwane[thola_inkomba] = (thola_inkomba + 회차) & 255;
            if (umsebenzisi.Thumela_imininingwane(isibambo_inani, 0x0a000202, intuba_inani, imininingwane, ubude_inani) != ubude_inani) return 4;
            if (umsebenzisi.자료받기(isibambo_inani, imininingwane, 300) != ubude_inani) return 5;
            for (int thola_inkomba = 0; thola_inkomba < ubude_inani; thola_inkomba++) if (imininingwane[thola_inkomba] != ((thola_inkomba + 회차) & 255)) return 6;
        }
        umsebenzisi.vala_iNethiwekhi(isibambo_inani);
        umsebenzisi.Bhala("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
