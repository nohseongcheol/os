// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, излезна_датотека = -1;
    static boolean 파이프입력, 파이프출력;
    static int неуспех_VALUE;
    static boolean Дозволи_интерактивен = true;
    public static int информатичка_технологија_интерактивен() { return Дозволи_интерактивен && 입력파일 < 3 && излезна_датотека < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int канал_VALUE, int VALUE) {
        if (канал_VALUE != 1) return 0;
        if (излезна_датотека >= 3) { int 처리값 = Меморија_Датотеки.Запиши(излезна_датотека, VALUE); if (처리값 < 0) неуспех_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) неуспех_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Меморија_Датотеки.Читај(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Напред_VALUE
    }
    static void Изврши_2(boolean проред_вертикална_црта, boolean 뒤파이프) {
        파이프입력 = проред_вертикална_црта; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; излезна_датотека = -1; неуспех_VALUE = 0;
    }
    static void 끝() {
        табла.입출력전환(0);
        if (입력파일 >= 3) Меморија_Датотеки.Затвори(입력파일);
        if (излезна_датотека >= 3) Меморија_Датотеки.Затвори(излезна_датотека);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; излезна_датотека = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
