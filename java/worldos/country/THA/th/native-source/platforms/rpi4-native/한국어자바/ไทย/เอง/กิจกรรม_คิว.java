// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
/** เอง 화면 เหตุการณ์ 큐에 실행할 일을 맡긴다. */
public final class กิจกรรม_คิว {
    private กิจกรรม_คิว() {}
    public static native void 나중에실행(실행할일 งาน_แอคชัน);
    public static native boolean 사건처리중인가();
}
