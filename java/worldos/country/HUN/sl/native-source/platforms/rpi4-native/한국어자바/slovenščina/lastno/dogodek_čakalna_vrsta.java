// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** lastno 화면 dogodek 큐에 실행할 일을 맡긴다. */
public final class dogodek_čakalna_vrsta {
    private dogodek_čakalna_vrsta() {}
    public static native void 나중에실행(실행할일 opravek_akcija);
    public static native boolean 사건처리중인가();
}
