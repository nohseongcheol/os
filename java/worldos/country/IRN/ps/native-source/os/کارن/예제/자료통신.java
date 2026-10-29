// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String ليکنه) {
        if (ليکنه == null || ليکنه.length() == 0) return -1;
        int 결과 = 0;
        for (int لړیال = 0; لړیال < ليکنه.length(); لړیال++) {
            int ارزښت = ليکنه.charAt(لړیال) - '0';
            if (ارزښت < 0 || ارزښت > 9 || 결과 > 6553) return -1;
            결과 = 결과 * 10 + ارزښت;
            if (결과 > 65535) return -1;
        }
        return 결과;
    }
    static int پته(String ليکنه) {
        if (ليکنه == null) return 0;
        int ارزښت = 0, 결과 = 0, 부분 = 0, 자릿수 = 0;
        for (int لړیال = 0; لړیال <= ليکنه.length(); لړیال++) {
            int 문자 = لړیال == ليکنه.length() ? '.' : ليکنه.charAt(لړیال);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                결과 = (결과 << 8) | ارزښت; 부분++; ارزښت = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                ارزښت = ارزښت * 10 + 문자 - '0';
                if (++자릿수 > 3 || ارزښت > 255) return 0;
            }
        }
        return 부분 == 4 ? 결과 : 0;
    }
    public static int ځغلول() {
        if (کارن.인수개수() != 3) { کارن.لوستل_2("Usage: run udp IP PORT TEXT\n"); return 2; }
        int پته = پته(کارن.인수(0)), درشل_ارزښت = 숫자(کارن.인수(1));
        String منځپانګه_ارزښت = کارن.인수(2);
        if (پته == 0 || درشل_ارزښت < 1 || منځپانګه_ارزښت.length() > 1024) { کارن.لوستل_2("Bad destination\n"); return 2; }
        int لاستى_ارزښت = کارن.통신열기(0);
        if (لاستى_ارزښت < 0) { کارن.لوستل_2("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] اومتوک = new int[1024];
        for (int لړیال = 0; لړیال < منځپانګه_ارزښت.length(); لړیال++) اومتوک[لړیال] = منځپانګه_ارزښت.charAt(لړیال);
        if (کارن.استول_اومتوک(لاستى_ارزښت, پته, درشل_ارزښت, اومتوک, منځپانګه_ارزښت.length()) < 0) {
            کارن.لوستل_2("UDP SEND FAILED\n"); کارن.بندول_جال(لاستى_ارزښت); return 4;
        }
        کارن.لوستل_2("UDP SENT\n");
        int 받은길이 = کارن.자료받기(لاستى_ارزښت, اومتوک, 1500);
        boolean 같음 = 받은길이 == منځپانګه_ارزښت.length() && کارن.보낸주소(لاستى_ارزښت) == پته && کارن.보낸창구(لاستى_ارزښت) == درشل_ارزښت;
        if (같음) for (int لړیال = 0; لړیال < 받은길이; لړیال++) if (اومتوک[لړیال] != منځپانګه_ارزښت.charAt(لړیال)) 같음 = false;
        کارن.بندول_جال(لاستى_ارزښت);
        if (받은길이 < 0) { کارن.لوستل_2("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        کارن.لوستل_2(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
