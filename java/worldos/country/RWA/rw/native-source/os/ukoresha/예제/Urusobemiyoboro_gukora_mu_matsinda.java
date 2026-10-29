// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ingano/홀수 uburebure_agaciro 데이터그램으로 nyakuri_amakurushingiro RTL8139 수신 gukora_mu_matsinda_agaciro 순환을 시험한다. */
public final class Urusobemiyoboro_gukora_mu_matsinda {
    public static int ihuriro() {
        if (ukoresha.인수개수() != 1) { ukoresha.kwandika("Usage: run stress PORT\n"); return 2; }
        String Umwandiko = ukoresha.인수(0);
        int poti_agaciro = 0;
        for (int umugerekashakiro = 0; umugerekashakiro < Umwandiko.length(); umugerekashakiro++) {
            if (Umwandiko.charAt(umugerekashakiro) < '0' || Umwandiko.charAt(umugerekashakiro) > '9' || poti_agaciro > 6553) return 2;
            poti_agaciro = poti_agaciro * 10 + Umwandiko.charAt(umugerekashakiro) - '0';
        }
        if (poti_agaciro < 1 || poti_agaciro > 65535) return 2;
        int umukondo_agaciro = ukoresha.kurema_Urusobemiyoboro(0);
        if (umukondo_agaciro < 0) return 3;
        int[] amakurushingiro = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int uburebure_agaciro = 1024 - (회차 & 1);
            for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) amakurushingiro[umugerekashakiro] = (umugerekashakiro + 회차) & 255;
            if (ukoresha.kohereza_amakurushingiro(umukondo_agaciro, 0x0a000202, poti_agaciro, amakurushingiro, uburebure_agaciro) != uburebure_agaciro) return 4;
            if (ukoresha.자료받기(umukondo_agaciro, amakurushingiro, 300) != uburebure_agaciro) return 5;
            for (int umugerekashakiro = 0; umugerekashakiro < uburebure_agaciro; umugerekashakiro++) if (amakurushingiro[umugerekashakiro] != ((umugerekashakiro + 회차) & 255)) return 6;
        }
        ukoresha.gufunga_Urusobemiyoboro(umukondo_agaciro);
        ukoresha.kwandika("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
