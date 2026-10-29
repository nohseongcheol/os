// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String 글) {
        if (글 == null || 글.length() == 0) return -1;
        int 결과 = 0;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < 글.length(); ee_iyatialujuna++) {
            int ajutuu = 글.charAt(ee_iyatialujuna) - '0';
            if (ajutuu < 0 || ajutuu > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + ajutuu;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int ejepüsee(String 글) {
        if (글 == null) return 0;
        int ajutuu = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int ee_iyatialujuna = 0; ee_iyatialujuna <= 글.length(); ee_iyatialujuna++) {
            int 문자 = ee_iyatialujuna == 글.length() ? '.' : 글.charAt(ee_iyatialujuna);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | ajutuu; 부분++; ajutuu = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ajutuu = ajutuu * 10 + 문자 - '0';
                if (++자릿수 > 3 || ajutuu > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int 시작() {
        if (ka_yataayakalü.인수개수() != 3) { ka_yataayakalü.ashajaa("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ejepüsee = ejepüsee(ka_yataayakalü.인수(0)), outtülee_ajutuu = 숫자(ka_yataayakalü.인수(1));
        String alu_ujatüü_ajutuu = ka_yataayakalü.인수(2);
        if (ejepüsee == 0 || outtülee_ajutuu < 1 || alu_ujatüü_ajutuu.length() > 1024) { ka_yataayakalü.ashajaa("Bad destination\n"); return 2; }
        int aapaaya_ajutuu = ka_yataayakalü.통신열기(0);
        if (aapaaya_ajutuu < 0) { ka_yataayakalü.ashajaa("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] atijaaya = new int[1024];
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < alu_ujatüü_ajutuu.length(); ee_iyatialujuna++) atijaaya[ee_iyatialujuna] = alu_ujatüü_ajutuu.charAt(ee_iyatialujuna);
        if (ka_yataayakalü.ajütaa_atijaaya(aapaaya_ajutuu, ejepüsee, outtülee_ajutuu, atijaaya, alu_ujatüü_ajutuu.length()) < 0) {
            ka_yataayakalü.ashajaa("UDP SEND FAILED\n"); ka_yataayakalü.asürülaa_kusu(aapaaya_ajutuu); return 4;
        }
        ka_yataayakalü.ashajaa("UDP SENT\n");
        int 받은길이 = ka_yataayakalü.자료받기(aapaaya_ajutuu, atijaaya, 1500);
        boolean 같음 = 받은길이 == alu_ujatüü_ajutuu.length() && ka_yataayakalü.보낸주소(aapaaya_ajutuu) == ejepüsee && ka_yataayakalü.보낸창구(aapaaya_ajutuu) == outtülee_ajutuu;
        if (같음) for (int ee_iyatialujuna = 0; ee_iyatialujuna < 받은길이; ee_iyatialujuna++) if (atijaaya[ee_iyatialujuna] != alu_ujatüü_ajutuu.charAt(ee_iyatialujuna)) 같음 = false;
        ka_yataayakalü.asürülaa_kusu(aapaaya_ajutuu);
        if (받은길이 < 0) { ka_yataayakalü.ashajaa("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ka_yataayakalü.ashajaa(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
