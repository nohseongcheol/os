// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** eigin 화면 atvik 큐에 실행할 일을 맡긴다. */
public final class atvik_biðröð {
    private atvik_biðröð() {}
    public static native void 나중에실행(실행할일 verk_aðgerð);
    public static native boolean 사건처리중인가();
}
