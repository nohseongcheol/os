// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** 작업 رشته_مقدار: 하나의 اجرا_فرمان جریان_مقدار. بومی JVM 안에서 فرمان 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 اجرا_2(실행할일 کار_عمل) { 작업가닥 رشته_مقدار = new 작업가닥(کار_عمل); رشته_مقدار.شروع_کار(); return رشته_مقدار; }
    public static void 기다리기(작업가닥 رشته_مقدار) throws 대기중단예외 { رشته_مقدار.기다리기(); }
    public static boolean 살아있는가(작업가닥 رشته_مقدار) { return رشته_مقدار.살아있는가(); }
    public static void تعلیق_کار() { 작업가닥.تعلیق_کار(); }
}
