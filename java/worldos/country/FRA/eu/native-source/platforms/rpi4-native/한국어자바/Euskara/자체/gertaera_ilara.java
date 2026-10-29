// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** 자체 화면 Gertaera 큐에 실행할 일을 맡긴다. */
public final class gertaera_ilara {
    private gertaera_ilara() {}
    public static native void 나중에실행(실행할일 ataza_ekintza);
    public static native boolean 사건처리중인가();
}
