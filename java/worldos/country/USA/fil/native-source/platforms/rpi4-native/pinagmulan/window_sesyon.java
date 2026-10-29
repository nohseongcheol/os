// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell katayuan_VALUE. file 저장소는 공유하고 path/변수/LOG_hanay/입력은 분리한다. */
public final class window_sesyon {
    static int[] 보관 = new int[4 * 30000], Ihanda = new int[4];
    static int 현재, posisyon;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] data, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_VALUE) 보관[posisyon++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[posisyon++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[posisyon++] = data_VALUE; return data_VALUE; } return 보관[posisyon++]; }
    static void i_seek_posisyon(int 보관칸, boolean 저장여부) {
        posisyon = 보관칸 * 30000;
        ARRAY_VALUE(Memory_Mga_File.현재, 저장여부); Memory_Mga_File.현재길이 = VALUE(Memory_Mga_File.현재길이, 저장여부);
        ARRAY_VALUE(shell_syntax.변수이름, 저장여부); ARRAY_VALUE(shell_syntax.변수값, 저장여부); ARRAY_VALUE(shell_syntax.이름길이, 저장여부); ARRAY_VALUE(shell_syntax.VALUE_haba, 저장여부);
        shell_syntax.katayuan_VALUE = VALUE(shell_syntax.katayuan_VALUE, 저장여부);
        ARRAY_VALUE(linya_Editor.LOG_hanay, 저장여부); ARRAY_VALUE(linya_Editor.LOG_haba, 저장여부); ARRAY_VALUE(linya_Editor.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.linya, 저장여부);
        linya_Editor.LOG_COUNT = VALUE(linya_Editor.LOG_COUNT, 저장여부); linya_Editor.LOG_hanay_tapusin = VALUE(linya_Editor.LOG_hanay_tapusin, 저장여부);
        linya_Editor.SEARCH_VALUE = VALUE(linya_Editor.SEARCH_VALUE, 저장여부); linya_Editor.저장길이 = VALUE(linya_Editor.저장길이, 저장여부);
        linya_Editor.sukat_82232621 = VALUE(linya_Editor.sukat_82232621, 저장여부); linya_Editor.kursor_VALUE = VALUE(linya_Editor.kursor_VALUE, 저장여부); linya_Editor.Start_window = VALUE(linya_Editor.Start_window, 저장여부);
        Ihanda[보관칸] = 1;
    }
    static void Proseso_VALUE_pagpasok() {
        int 사건번호 = board.Terminal(12); if (사건번호 == 0) return;
        i_seek_posisyon(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { board.control_gumagamit_app(32 + Loop_INDEX); Ihanda[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Ihanda[Loop_INDEX] = 0;
        }
        int Susunod_posisyon = (사건번호 & 15) - 1; if (Susunod_posisyon < 0) Susunod_posisyon = 0;
        if (Ihanda[Susunod_posisyon] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Susunod_posisyon * 30000 + Loop_INDEX] = 0;
        현재 = Susunod_posisyon; i_seek_posisyon(현재, false); board.Terminal(100 + 현재); 이어읽기 = true;
        단말.sumulat("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (board.control_gumagamit_app(16 + 현재) == 0) return false;
        셸입출력.payagan_tumutugon_interactive = true; 셸입출력.run(false, false); board.입출력전환(1);
        int 처리값 = board.control_gumagamit_app(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_syntax.katayuan_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.sumulat("exit "); 단말.수(처리값); 단말.문자(10); board.Terminal(3); }
        return true;
    }
}
