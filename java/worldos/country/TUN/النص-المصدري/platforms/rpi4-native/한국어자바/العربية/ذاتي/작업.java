// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package العربية.ذاتي;
/** 작업 محادثة_قيمة: 하나의 ينفذ_أمر بث_قيمة. ذاتي JVM 안에서 أمر 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static خيطالعمل تشغيل(실행할일 مهمة_إجراء) { خيطالعمل محادثة_قيمة = new خيطالعمل(مهمة_إجراء); محادثة_قيمة.بدء_مهمة(); return محادثة_قيمة; }
    public static void 기다리기(خيطالعمل محادثة_قيمة) throws 대기중단예외 { محادثة_قيمة.기다리기(); }
    public static boolean 살아있는가(خيطالعمل محادثة_قيمة) { return محادثة_قيمة.살아있는가(); }
    public static void العائد_مهمة() { خيطالعمل.العائد_مهمة(); }
}
