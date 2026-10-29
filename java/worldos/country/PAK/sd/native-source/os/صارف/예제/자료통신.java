// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int ڊجٽ_قدر(String متن) {
        if (متن == null || متن.length() == 0) return -1;
        int 결과 = 0;
        for (int ابتدائي = 0; ابتدائي < متن.length(); ابتدائي++) {
            int قدر = متن.charAt(ابتدائي) - '0';
            if (قدر < 0 || قدر > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + قدر;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int پتو(String متن) {
        if (متن == null) return 0;
        int قدر = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int ابتدائي = 0; ابتدائي <= متن.length(); ابتدائي++) {
            int 문자 = ابتدائي == متن.length() ? '.' : متن.charAt(ابتدائي);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | قدر; 부분++; قدر = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                قدر = قدر * 10 + 문자 - '0';
                if (++자릿수 > 3 || قدر > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int هلائڻ() {
        if (صارف.인수개수() != 3) { صارف.لکو("Usage: run udp IP PORT TEXT\n"); return 2; }
        int پتو = پتو(صارف.인수(0)), پورٽ_قدر = ڊجٽ_قدر(صارف.인수(1));
        String مواد_قدر = صارف.인수(2);
        if (پتو == 0 || پورٽ_قدر < 1 || مواد_قدر.length() > 1024) { صارف.لکو("Bad destination\n"); return 2; }
        int منهن_ڏيڻ_قدر = صارف.ٺاھيو_نيٽ_ورڪ(0);
        if (منهن_ڏيڻ_قدر < 0) { صارف.لکو("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] ڪوائف = new int[1024];
        for (int ابتدائي = 0; ابتدائي < مواد_قدر.length(); ابتدائي++) ڪوائف[ابتدائي] = مواد_قدر.charAt(ابتدائي);
        if (صارف.اي_ميل_ڪوائف(منهن_ڏيڻ_قدر, پتو, پورٽ_قدر, ڪوائف, مواد_قدر.length()) < 0) {
            صارف.لکو("UDP SEND FAILED\n"); صارف.بند_ڪرڻ_نيٽ_ورڪ(منهن_ڏيڻ_قدر); return 4;
        }
        صارف.لکو("UDP SENT\n");
        int 받은길이 = صارف.자료받기(منهن_ڏيڻ_قدر, ڪوائف, 1500);
        boolean 같음 = 받은길이 == مواد_قدر.length() && صارف.보낸주소(منهن_ڏيڻ_قدر) == پتو && صارف.보낸창구(منهن_ڏيڻ_قدر) == پورٽ_قدر;
        if (같음) for (int ابتدائي = 0; ابتدائي < 받은길이; ابتدائي++) if (ڪوائف[ابتدائي] != مواد_قدر.charAt(ابتدائي)) 같음 = false;
        صارف.بند_ڪرڻ_نيٽ_ورڪ(منهن_ڏيڻ_قدر);
        if (받은길이 < 0) { صارف.لکو("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        صارف.لکو(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
