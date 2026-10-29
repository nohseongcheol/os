// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package русский.свой;
/** свой экран Событие 큐에 실행할 일을 맡긴다. */
public final class Событие_Очередь {
    private Событие_Очередь() {}
    public static native void 나중에실행(실행할일 дело_задача);
    public static native boolean 사건처리중인가();
}
