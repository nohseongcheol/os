// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, 출력파일 = -1;
    static boolean 파이프입력, 파이프출력;
    static int 실패;
    static boolean 대화허용 = true;
    public static int 대화가능() { return 대화허용 && 입력파일 < 3 && 출력파일 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int 채널, int 값) {
        if (채널 != 1) return 0;
        if (출력파일 >= 3) { int 처리값 = 기억파일.쓰기(출력파일, 값); if (처리값 < 0) 실패 = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) 실패 = -28;
        else 출력자료[출력길이++] = 값;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = 기억파일.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 전달
    }
    static void Koyr(boolean 앞파이프, boolean 뒤파이프) {
        파이프입력 = 앞파이프; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; 출력파일 = -1; 실패 = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) 기억파일.닫기(입력파일);
        if (출력파일 >= 3) 기억파일.닫기(출력파일);
        if (파이프출력) { 입력길이 = 출력길이; for (int 반복자리 = 0; 반복자리 < 출력길이; 반복자리++) 입력자료[반복자리] = 출력자료[반복자리]; }
        입력파일 = -1; 출력파일 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
