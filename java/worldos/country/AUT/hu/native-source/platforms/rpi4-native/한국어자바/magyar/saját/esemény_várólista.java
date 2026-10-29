// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package magyar.saját;
/** saját 화면 Esemény 큐에 실행할 일을 맡긴다. */
public final class esemény_várólista {
    private esemény_várólista() {}
    public static native void 나중에실행(실행할일 teendő_Action);
    public static native boolean 사건처리중인가();
}
