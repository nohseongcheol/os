// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;
/** 자체 화면 настан 큐에 실행할 일을 맡긴다. */
public final class настан_ред_на_чекање {
    private настан_ред_на_чекање() {}
    public static native void 나중에실행(실행할일 задача_Дејство);
    public static native boolean 사건처리중인가();
}
