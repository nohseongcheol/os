// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int umubare_agaciro(String Umwandiko) {
        if (Umwandiko == null || Umwandiko.length() == 0) return -1;
        int 결과 = 0;
        for (int umugerekashakiro = 0; umugerekashakiro < Umwandiko.length(); umugerekashakiro++) {
            int agaciro = Umwandiko.charAt(umugerekashakiro) - '0';
            if (agaciro < 0 || agaciro > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + agaciro;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int aderesi(String Umwandiko) {
        if (Umwandiko == null) return 0;
        int agaciro = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int umugerekashakiro = 0; umugerekashakiro <= Umwandiko.length(); umugerekashakiro++) {
            int 문자 = umugerekashakiro == Umwandiko.length() ? '.' : Umwandiko.charAt(umugerekashakiro);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | agaciro; 부분++; agaciro = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                agaciro = agaciro * 10 + 문자 - '0';
                if (++자릿수 > 3 || agaciro > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int ihuriro() {
        if (ukoresha.인수개수() != 3) { ukoresha.kwandika("Usage: run udp IP PORT TEXT\n"); return 2; }
        int aderesi = aderesi(ukoresha.인수(0)), poti_agaciro = umubare_agaciro(ukoresha.인수(1));
        String Ibirimo_agaciro = ukoresha.인수(2);
        if (aderesi == 0 || poti_agaciro < 1 || Ibirimo_agaciro.length() > 1024) { ukoresha.kwandika("Bad destination\n"); return 2; }
        int umukondo_agaciro = ukoresha.kurema_Urusobemiyoboro(0);
        if (umukondo_agaciro < 0) { ukoresha.kwandika("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] amakurushingiro = new int[1024];
        for (int umugerekashakiro = 0; umugerekashakiro < Ibirimo_agaciro.length(); umugerekashakiro++) amakurushingiro[umugerekashakiro] = Ibirimo_agaciro.charAt(umugerekashakiro);
        if (ukoresha.kohereza_amakurushingiro(umukondo_agaciro, aderesi, poti_agaciro, amakurushingiro, Ibirimo_agaciro.length()) < 0) {
            ukoresha.kwandika("UDP SEND FAILED\n"); ukoresha.gufunga_Urusobemiyoboro(umukondo_agaciro); return 4;
        }
        ukoresha.kwandika("UDP SENT\n");
        int 받은길이 = ukoresha.자료받기(umukondo_agaciro, amakurushingiro, 1500);
        boolean 같음 = 받은길이 == Ibirimo_agaciro.length() && ukoresha.보낸주소(umukondo_agaciro) == aderesi && ukoresha.보낸창구(umukondo_agaciro) == poti_agaciro;
        if (같음) for (int umugerekashakiro = 0; umugerekashakiro < 받은길이; umugerekashakiro++) if (amakurushingiro[umugerekashakiro] != Ibirimo_agaciro.charAt(umugerekashakiro)) 같음 = false;
        ukoresha.gufunga_Urusobemiyoboro(umukondo_agaciro);
        if (받은길이 < 0) { ukoresha.kwandika("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ukoresha.kwandika(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
