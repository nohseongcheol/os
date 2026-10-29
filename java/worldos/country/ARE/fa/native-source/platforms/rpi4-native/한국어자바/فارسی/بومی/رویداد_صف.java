// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** بومی 화면 رویداد 큐에 실행할 일을 맡긴다. */
public final class رویداد_صف {
    private رویداد_صف() {}
    public static native void 나중에실행(실행할일 کار_عمل);
    public static native boolean 사건처리중인가();
}
