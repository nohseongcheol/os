// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** निज 화면 घटना 큐에 실행할 일을 맡긴다. */
public final class घटना_कतार {
    private घटना_कतार() {}
    public static native void 나중에실행(실행할일 कार्य_एक्शन);
    public static native boolean 사건처리중인가();
}
