// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, чыгыш_файлы = -1;
    static boolean 파이프입력, 파이프출력;
    static int эштән_туктау_VALUE;
    static boolean Рөхсәт_интерактив = true;
    public static int 대화가능() { return Рөхсәт_интерактив && 입력파일 < 3 && чыгыш_файлы < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int канал_VALUE, int VALUE) {
        if (канал_VALUE != 1) return 0;
        if (чыгыш_файлы >= 3) { int 처리값 = Хәтер_Файллар.язу(чыгыш_файлы, VALUE); if (처리값 < 0) эштән_туктау_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) эштән_туктау_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Хәтер_Файллар.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Алга_VALUE
    }
    static void эшләтү(boolean юлара_интервал_вертикаль_сызык, boolean 뒤파이프) {
        파이프입력 = юлара_интервал_вертикаль_сызык; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; чыгыш_файлы = -1; эштән_туктау_VALUE = 0;
    }
    static void 끝() {
        такта.입출력전환(0);
        if (입력파일 >= 3) Хәтер_Файллар.Yap(입력파일);
        if (чыгыш_файлы >= 3) Хәтер_Файллар.Yap(чыгыш_файлы);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; чыгыш_файлы = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
