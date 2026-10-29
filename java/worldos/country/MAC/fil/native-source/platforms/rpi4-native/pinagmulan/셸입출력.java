// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, file_ng_output = -1;
    static boolean 파이프입력, 파이프출력;
    static int pagpalya_VALUE;
    static boolean payagan_tumutugon_interactive = true;
    public static int information_technology_tumutugon_interactive() { return payagan_tumutugon_interactive && 입력파일 < 3 && file_ng_output < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int channel_VALUE, int VALUE) {
        if (channel_VALUE != 1) return 0;
        if (file_ng_output >= 3) { int 처리값 = Memory_Mga_File.sumulat(file_ng_output, VALUE); if (처리값 < 0) pagpalya_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) pagpalya_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Memory_Mga_File.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 ipasa_VALUE_24592b8a
    }
    static void run(boolean pagitan_ng_linya_patayong_bar, boolean 뒤파이프) {
        파이프입력 = pagitan_ng_linya_patayong_bar; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; file_ng_output = -1; pagpalya_VALUE = 0;
    }
    static void 끝() {
        board.입출력전환(0);
        if (입력파일 >= 3) Memory_Mga_File.isara(입력파일);
        if (file_ng_output >= 3) Memory_Mga_File.isara(file_ng_output);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; file_ng_output = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
