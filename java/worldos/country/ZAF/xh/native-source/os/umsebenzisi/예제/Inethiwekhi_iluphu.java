// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ubukhulu/홀수 ubude_ixabiso 데이터그램으로 eyona_yenzekileyo_iingcombolo RTL8139 수신 iluphu_ixabiso 순환을 시험한다. */
public final class Inethiwekhi_iluphu {
    public static int Phumeza() {
        if (umsebenzisi.인수개수() != 1) { umsebenzisi.Bhala("Usage: run stress PORT\n"); return 2; }
        String Umbhalo = umsebenzisi.인수(0);
        int iphothi_ixabiso = 0;
        for (int indeksa = 0; indeksa < Umbhalo.length(); indeksa++) {
            if (Umbhalo.charAt(indeksa) < '0' || Umbhalo.charAt(indeksa) > '9' || iphothi_ixabiso > 6553) return 2;
            iphothi_ixabiso = iphothi_ixabiso * 10 + Umbhalo.charAt(indeksa) - '0';
        }
        if (iphothi_ixabiso < 1 || iphothi_ixabiso > 65535) return 2;
        int isibambi_ixabiso = umsebenzisi.vula_Inethiwekhi(0);
        if (isibambi_ixabiso < 0) return 3;
        int[] iingcombolo = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int ubude_ixabiso = 1024 - (회차 & 1);
            for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) iingcombolo[indeksa] = (indeksa + 회차) & 255;
            if (umsebenzisi.thumela_iingcombolo(isibambi_ixabiso, 0x0a000202, iphothi_ixabiso, iingcombolo, ubude_ixabiso) != ubude_ixabiso) return 4;
            if (umsebenzisi.자료받기(isibambi_ixabiso, iingcombolo, 300) != ubude_ixabiso) return 5;
            for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) if (iingcombolo[indeksa] != ((indeksa + 회차) & 255)) return 6;
        }
        umsebenzisi.vala_Inethiwekhi(isibambi_ixabiso);
        umsebenzisi.Bhala("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
