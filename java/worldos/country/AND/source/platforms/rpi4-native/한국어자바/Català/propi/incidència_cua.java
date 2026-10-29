// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;
/** propi 화면 Esdeveniment 큐에 실행할 일을 맡긴다. */
public final class incidència_cua {
    private incidència_cua() {}
    public static native void 나중에실행(실행할일 tasca_acció);
    public static native boolean 사건처리중인가();
}
