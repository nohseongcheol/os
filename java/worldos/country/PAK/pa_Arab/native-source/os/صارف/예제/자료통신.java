// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int عدد_قدر(String متن) {
        if (متن == null || متن.length() == 0) return -1;
        int 결과 = 0;
        for (int اشاریہ = 0; اشاریہ < متن.length(); اشاریہ++) {
            int قدر = متن.charAt(اشاریہ) - '0';
            if (قدر < 0 || قدر > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + قدر;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int پتا(String متن) {
        if (متن == null) return 0;
        int قدر = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int اشاریہ = 0; اشاریہ <= متن.length(); اشاریہ++) {
            int 문자 = اشاریہ == متن.length() ? '.' : متن.charAt(اشاریہ);
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
    public static int چلاؤ() {
        if (صارف.인수개수() != 3) { صارف.لکھو("Usage: run udp IP PORT TEXT\n"); return 2; }
        int پتا = پتا(صارف.인수(0)), دہانہ_قدر = عدد_قدر(صارف.인수(1));
        String اجزاء_قدر = صارف.인수(2);
        if (پتا == 0 || دہانہ_قدر < 1 || اجزاء_قدر.length() > 1024) { صارف.لکھو("Bad destination\n"); return 2; }
        int نبٹنا_قدر = صارف.بنڑاؤ_نیٹ_ورک(0);
        if (نبٹنا_قدر < 0) { صارف.لکھو("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] کوائف = new int[1024];
        for (int اشاریہ = 0; اشاریہ < اجزاء_قدر.length(); اشاریہ++) کوائف[اشاریہ] = اجزاء_قدر.charAt(اشاریہ);
        if (صارف.بھیجو_کوائف(نبٹنا_قدر, پتا, دہانہ_قدر, کوائف, اجزاء_قدر.length()) < 0) {
            صارف.لکھو("UDP SEND FAILED\n"); صارف.بند_کرو_نیٹ_ورک(نبٹنا_قدر); return 4;
        }
        صارف.لکھو("UDP SENT\n");
        int 받은길이 = صارف.자료받기(نبٹنا_قدر, کوائف, 1500);
        boolean 같음 = 받은길이 == اجزاء_قدر.length() && صارف.보낸주소(نبٹنا_قدر) == پتا && صارف.보낸창구(نبٹنا_قدر) == دہانہ_قدر;
        if (같음) for (int اشاریہ = 0; اشاریہ < 받은길이; اشاریہ++) if (کوائف[اشاریہ] != اجزاء_قدر.charAt(اشاریہ)) 같음 = false;
        صارف.بند_کرو_نیٹ_ورک(نبٹنا_قدر);
        if (받은길이 < 0) { صارف.لکھو("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        صارف.لکھو(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
