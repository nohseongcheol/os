// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int عدد_قدر(String متن) {
        if (متن == null || متن.length() == 0) return -1;
        int پیمائش = 0;
        for (int اشاریہ = 0; اشاریہ < متن.length(); اشاریہ++) {
            int قدر = متن.charAt(اشاریہ) - '0';
            if (قدر < 0 || قدر > 9 || پیمائش > 6553) return -1;
            پیمائش = پیمائش * 10 + قدر;
            if (پیمائش > 65535) return -1;
        }
        return پیمائش;
    }
    static int پتہ(String متن) {
        if (متن == null) return 0;
        int قدر = 0, پیمائش = 0, 부분 = 0, 자릿수 = 0;
        for (int اشاریہ = 0; اشاریہ <= متن.length(); اشاریہ++) {
            int 문자 = اشاریہ == متن.length() ? '.' : متن.charAt(اشاریہ);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                پیمائش = (پیمائش << 8) | قدر; 부분++; قدر = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                قدر = قدر * 10 + 문자 - '0';
                if (++자릿수 > 3 || قدر > 255) return 0;
            }
        }
        return 부분 == 4 ? پیمائش : 0;
    }
    public static int چلائیں() {
        if (صارف.인수개수() != 3) { صارف.لکھیں("Usage: run udp IP PORT TEXT\n"); return 2; }
        int پتہ = پتہ(صارف.دلائل(0)), پورٹ_قدر = عدد_قدر(صارف.دلائل(1));
        String مشمول_قدر = صارف.دلائل(2);
        if (پتہ == 0 || پورٹ_قدر < 1 || مشمول_قدر.length() > 1024) { صارف.لکھیں("Bad destination\n"); return 2; }
        int ہینڈل_قدر = صارف.بنائیں_نیٹ_ورک(0);
        if (ہینڈل_قدر < 0) { صارف.لکھیں("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] کوائف = new int[1024];
        for (int اشاریہ = 0; اشاریہ < مشمول_قدر.length(); اشاریہ++) کوائف[اشاریہ] = مشمول_قدر.charAt(اشاریہ);
        if (صارف.بھیجیں_کوائف(ہینڈل_قدر, پتہ, پورٹ_قدر, کوائف, مشمول_قدر.length()) < 0) {
            صارف.لکھیں("UDP SEND FAILED\n"); صارف.بند_نیٹ_ورک(ہینڈل_قدر); return 4;
        }
        صارف.لکھیں("UDP SENT\n");
        int 받은길이 = صارف.자료받기(ہینڈل_قدر, کوائف, 1500);
        boolean 같음 = 받은길이 == مشمول_قدر.length() && صارف.보낸주소(ہینڈل_قدر) == پتہ && صارف.보낸창구(ہینڈل_قدر) == پورٹ_قدر;
        if (같음) for (int اشاریہ = 0; اشاریہ < 받은길이; اشاریہ++) if (کوائف[اشاریہ] != مشمول_قدر.charAt(اشاریہ)) 같음 = false;
        صارف.بند_نیٹ_ورک(ہینڈل_قدر);
        if (받은길이 < 0) { صارف.لکھیں("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        صارف.لکھیں(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
