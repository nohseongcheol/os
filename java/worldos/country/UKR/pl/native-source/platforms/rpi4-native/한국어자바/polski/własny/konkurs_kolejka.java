// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** własny 화면 Wydarzenie 큐에 실행할 일을 맡긴다. */
public final class konkurs_kolejka {
    private konkurs_kolejka() {}
    public static native void 나중에실행(실행할일 zadanie_akcja);
    public static native boolean 사건처리중인가();
}
