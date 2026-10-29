// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.اپنا;
/** اپنا 화면 واقعہ 큐에 실행할 일을 맡긴다. */
public final class ایونٹ_قطار {
    private ایونٹ_قطار() {}
    public static native void 나중에실행(실행할일 ٹاسک_عمل);
    public static native boolean 사건처리중인가();
}
