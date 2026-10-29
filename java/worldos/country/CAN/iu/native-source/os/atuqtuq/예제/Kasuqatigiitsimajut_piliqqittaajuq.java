// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 anininga/홀수 takininga_atuutilik 데이터그램으로 taannallarik_titiqqat RTL8139 수신 piliqqittaajuq_atuutilik 순환을 시험한다. */
public final class Kasuqatigiitsimajut_piliqqittaajuq {
    public static int 시작() {
        if (atuqtuq.인수개수() != 1) { atuqtuq.titiraq("Usage: run stress PORT\n"); return 2; }
        String titiqqaq = atuqtuq.인수(0);
        int kapputigaq_atuutilik = 0;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < titiqqaq.length(); nalunaiqsimavik++) {
            if (titiqqaq.charAt(nalunaiqsimavik) < '0' || titiqqaq.charAt(nalunaiqsimavik) > '9' || kapputigaq_atuutilik > 6553) return 2;
            kapputigaq_atuutilik = kapputigaq_atuutilik * 10 + titiqqaq.charAt(nalunaiqsimavik) - '0';
        }
        if (kapputigaq_atuutilik < 1 || kapputigaq_atuutilik > 65535) return 2;
        int nuuttarut_atuutilik = atuqtuq.matuirli_Kasuqatigiitsimajut(0);
        if (nuuttarut_atuutilik < 0) return 3;
        int[] titiqqat = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int takininga_atuutilik = 1024 - (회차 & 1);
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) titiqqat[nalunaiqsimavik] = (nalunaiqsimavik + 회차) & 255;
            if (atuqtuq.nassiutili_titiqqat(nuuttarut_atuutilik, 0x0a000202, kapputigaq_atuutilik, titiqqat, takininga_atuutilik) != takininga_atuutilik) return 4;
            if (atuqtuq.자료받기(nuuttarut_atuutilik, titiqqat, 300) != takininga_atuutilik) return 5;
            for (int nalunaiqsimavik = 0; nalunaiqsimavik < takininga_atuutilik; nalunaiqsimavik++) if (titiqqat[nalunaiqsimavik] != ((nalunaiqsimavik + 회차) & 255)) return 6;
        }
        atuqtuq.matuli_Kasuqatigiitsimajut(nuuttarut_atuutilik);
        atuqtuq.titiraq("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
