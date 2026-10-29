// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Dansk.eget;
/** eget skærmbillede hændelse 큐에 실행할 일을 맡긴다. */
public final class hændelse_kø {
    private hændelse_kø() {}
    public static native void 나중에실행(실행할일 job_To_do);
    public static native boolean 사건처리중인가();
}
