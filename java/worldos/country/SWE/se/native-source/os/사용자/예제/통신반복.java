// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 크기/홀수 길이 데이터그램으로 실제 RTL8139 수신 고리 순환을 시험한다. */
public final class 통신반복 {
    public static int 시작() {
        if (사용자.인수개수() != 1) { 사용자.Čále("Usage: run stress PORT\n"); return 2; }
        String teaksta = 사용자.Argumeanttat(0);
        int 창구 = 0;
        for (int 번호 = 0; 번호 < teaksta.length(); 번호++) {
            if (teaksta.charAt(번호) < '0' || teaksta.charAt(번호) > '9' || 창구 > 6553) return 2;
            창구 = 창구 * 10 + teaksta.charAt(번호) - '0';
        }
        if (창구 < 1 || 창구 > 65535) return 2;
        int 손잡이 = 사용자.통신열기(0);
        if (손잡이 < 0) return 3;
        int[] 자료 = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int 번호 = 0; 번호 < 길이; 번호++) 자료[번호] = (번호 + 회차) & 255;
            if (사용자.자료보내기(손잡이, 0x0a000202, 창구, 자료, 길이) != 길이) return 4;
            if (사용자.자료받기(손잡이, 자료, 300) != 길이) return 5;
            for (int 번호 = 0; 번호 < 길이; 번호++) if (자료[번호] != ((번호 + 회차) & 255)) return 6;
        }
        사용자.통신닫기(손잡이);
        사용자.Čále("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
