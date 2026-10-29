// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 크기/홀수 akaliaa_ajutuu 데이터그램으로 실제 RTL8139 수신 eitawaakualü_ajutuu 순환을 시험한다. */
public final class kusu_eitawaakualü {
    public static int 시작() {
        if (ka_yataayakalü.인수개수() != 1) { ka_yataayakalü.ashajaa("Usage: run stress PORT\n"); return 2; }
        String 글 = ka_yataayakalü.인수(0);
        int outtülee_ajutuu = 0;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 글.length(); ee_iyatialujuna++) {
            if (글.charAt(ee_iyatialujuna) < '0' || 글.charAt(ee_iyatialujuna) > '9' || outtülee_ajutuu > 6553) return 2;
            outtülee_ajutuu = outtülee_ajutuu * 10 + 글.charAt(ee_iyatialujuna) - '0';
        }
        if (outtülee_ajutuu < 1 || outtülee_ajutuu > 65535) return 2;
        int aapaaya_ajutuu = ka_yataayakalü.통신열기(0);
        if (aapaaya_ajutuu < 0) return 3;
        int[] atijaaya = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int akaliaa_ajutuu = 1024 - (회차 & 1);
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) atijaaya[ee_iyatialujuna] = (ee_iyatialujuna + 회차) & 255;
            if (ka_yataayakalü.ajütaa_atijaaya(aapaaya_ajutuu, 0x0a000202, outtülee_ajutuu, atijaaya, akaliaa_ajutuu) != akaliaa_ajutuu) return 4;
            if (ka_yataayakalü.자료받기(aapaaya_ajutuu, atijaaya, 300) != akaliaa_ajutuu) return 5;
            for (int ee_iyatialujuna = 0; ee_iyatialujuna < akaliaa_ajutuu; ee_iyatialujuna++) if (atijaaya[ee_iyatialujuna] != ((ee_iyatialujuna + 회차) & 255)) return 6;
        }
        ka_yataayakalü.asürülaa_kusu(aapaaya_ajutuu);
        ka_yataayakalü.ashajaa("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
