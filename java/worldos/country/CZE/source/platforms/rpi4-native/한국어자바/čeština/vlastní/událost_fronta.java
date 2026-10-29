// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package čeština.vlastní;
/** vlastní 화면 Události 큐에 실행할 일을 맡긴다. */
public final class událost_fronta {
    private událost_fronta() {}
    public static native void 나중에실행(실행할일 úkol_Akce);
    public static native boolean 사건처리중인가();
}
