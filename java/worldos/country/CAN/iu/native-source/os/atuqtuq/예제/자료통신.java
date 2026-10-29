// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String titiqqaq) {
        if (titiqqaq == null || titiqqaq.length() == 0) return -1;
        int 결과 = 0;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < titiqqaq.length(); nalunaiqsimavik++) {
            int atuutilik = titiqqaq.charAt(nalunaiqsimavik) - '0';
            if (atuutilik < 0 || atuutilik > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + atuutilik;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int turaarut(String titiqqaq) {
        if (titiqqaq == null) return 0;
        int atuutilik = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int nalunaiqsimavik = 0; nalunaiqsimavik <= titiqqaq.length(); nalunaiqsimavik++) {
            int 문자 = nalunaiqsimavik == titiqqaq.length() ? '.' : titiqqaq.charAt(nalunaiqsimavik);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | atuutilik; 부분++; atuutilik = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                atuutilik = atuutilik * 10 + 문자 - '0';
                if (++자릿수 > 3 || atuutilik > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int 시작() {
        if (atuqtuq.인수개수() != 3) { atuqtuq.titiraq("Usage: run udp IP PORT TEXT\n"); return 2; }
        int turaarut = turaarut(atuqtuq.인수(0)), kapputigaq_atuutilik = 숫자(atuqtuq.인수(1));
        String Ilulingit_atuutilik = atuqtuq.인수(2);
        if (turaarut == 0 || kapputigaq_atuutilik < 1 || Ilulingit_atuutilik.length() > 1024) { atuqtuq.titiraq("Bad destination\n"); return 2; }
        int nuuttarut_atuutilik = atuqtuq.matuirli_Kasuqatigiitsimajut(0);
        if (nuuttarut_atuutilik < 0) { atuqtuq.titiraq("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] titiqqat = new int[1024];
        for (int nalunaiqsimavik = 0; nalunaiqsimavik < Ilulingit_atuutilik.length(); nalunaiqsimavik++) titiqqat[nalunaiqsimavik] = Ilulingit_atuutilik.charAt(nalunaiqsimavik);
        if (atuqtuq.nassiutili_titiqqat(nuuttarut_atuutilik, turaarut, kapputigaq_atuutilik, titiqqat, Ilulingit_atuutilik.length()) < 0) {
            atuqtuq.titiraq("UDP SEND FAILED\n"); atuqtuq.matuli_Kasuqatigiitsimajut(nuuttarut_atuutilik); return 4;
        }
        atuqtuq.titiraq("UDP SENT\n");
        int 받은길이 = atuqtuq.자료받기(nuuttarut_atuutilik, titiqqat, 1500);
        boolean 같음 = 받은길이 == Ilulingit_atuutilik.length() && atuqtuq.보낸주소(nuuttarut_atuutilik) == turaarut && atuqtuq.보낸창구(nuuttarut_atuutilik) == kapputigaq_atuutilik;
        if (같음) for (int nalunaiqsimavik = 0; nalunaiqsimavik < 받은길이; nalunaiqsimavik++) if (titiqqat[nalunaiqsimavik] != Ilulingit_atuutilik.charAt(nalunaiqsimavik)) 같음 = false;
        atuqtuq.matuli_Kasuqatigiitsimajut(nuuttarut_atuutilik);
        if (받은길이 < 0) { atuqtuq.titiraq("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        atuqtuq.titiraq(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
