// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** עצמי JVM 스케줄러가 관리하는 לבצע_פקודה זרם_ערך. 표준 Thread를 감싸지 않는다. */
public final class משימתרקע {
    public משימתרקע(실행할일 משימה_המלצה) {
        throw new מצב_חריגה("עצמי JVM의 עברית 작업 שרשור_ערך יצר 기능이 필요합니다.");
    }
    public native void התחל_משימה() throws שרשור_מצב_חריגה;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void רווח_משימה();
}
