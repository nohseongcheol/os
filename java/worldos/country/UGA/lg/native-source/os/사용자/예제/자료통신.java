// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int 숫자(String Bigambo) {
        if (Bigambo == null || Bigambo.length() == 0) return -1;
        int KIGENDERWA = 0;
        for (int 번호 = 0; 번호 < Bigambo.length(); 번호++) {
            int 값 = Bigambo.charAt(번호) - '0';
            if (값 < 0 || 값 > 9 || KIGENDERWA > 6553) return -1;
            KIGENDERWA = KIGENDERWA * 10 + 값;
            if (KIGENDERWA > 65535) return -1;
        }
        return KIGENDERWA;
    }
    static int 주소(String Bigambo) {
        if (Bigambo == null) return 0;
        int 값 = 0, KIGENDERWA = 0, 부분 = 0, 자릿수 = 0;
        for (int 번호 = 0; 번호 <= Bigambo.length(); 번호++) {
            int 문자 = 번호 == Bigambo.length() ? '.' : Bigambo.charAt(번호);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                KIGENDERWA = (KIGENDERWA << 8) | 값; 부분++; 값 = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                값 = 값 * 10 + 문자 - '0';
                if (++자릿수 > 3 || 값 > 255) return 0;
            }
        }
        return 부분 == 4 ? KIGENDERWA : 0;
    }
    public static int Tandika() {
        if (사용자.인수개수() != 3) { 사용자.쓰기("Usage: run udp IP PORT TEXT\n"); return 2; }
        int 주소 = 주소(사용자.인수(0)), 창구 = 숫자(사용자.인수(1));
        String 내용 = 사용자.인수(2);
        if (주소 == 0 || 창구 < 1 || 내용.length() > 1024) { 사용자.쓰기("Bad destination\n"); return 2; }
        int 손잡이 = 사용자.통신열기(0);
        if (손잡이 < 0) { 사용자.쓰기("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] 자료 = new int[1024];
        for (int 번호 = 0; 번호 < 내용.length(); 번호++) 자료[번호] = 내용.charAt(번호);
        if (사용자.자료보내기(손잡이, 주소, 창구, 자료, 내용.length()) < 0) {
            사용자.쓰기("UDP SEND FAILED\n"); 사용자.통신닫기(손잡이); return 4;
        }
        사용자.쓰기("UDP SENT\n");
        int 받은길이 = 사용자.자료받기(손잡이, 자료, 1500);
        boolean 같음 = 받은길이 == 내용.length() && 사용자.보낸주소(손잡이) == 주소 && 사용자.보낸창구(손잡이) == 창구;
        if (같음) for (int 번호 = 0; 번호 < 받은길이; 번호++) if (자료[번호] != 내용.charAt(번호)) 같음 = false;
        사용자.통신닫기(손잡이);
        if (받은길이 < 0) { 사용자.쓰기("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        사용자.쓰기(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
