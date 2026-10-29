// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package עברית.עצמי;
/** 작업 שרשור_ערך: 하나의 לבצע_פקודה זרם_ערך. עצמי JVM 안에서 פקודה 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static משימתרקע הפעלה(실행할일 משימה_המלצה) { משימתרקע שרשור_ערך = new משימתרקע(משימה_המלצה); שרשור_ערך.התחל_משימה(); return שרשור_ערך; }
    public static void 기다리기(משימתרקע שרשור_ערך) throws 대기중단예외 { שרשור_ערך.기다리기(); }
    public static boolean 살아있는가(משימתרקע שרשור_ערך) { return שרשור_ערך.살아있는가(); }
    public static void רווח_משימה() { משימתרקע.רווח_משימה(); }
}
