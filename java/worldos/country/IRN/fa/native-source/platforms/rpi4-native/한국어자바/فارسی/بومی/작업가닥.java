// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package فارسی.بومی;
/** بومی JVM 스케줄러가 관리하는 اجرا_فرمان جریان_مقدار. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 کار_عمل) {
        throw new وضعیت_استثنا("بومی JVM의 فارسی 작업 رشته_مقدار ایجاد 기능이 필요합니다.");
    }
    public native void شروع_کار() throws رشته_وضعیت_استثنا;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void تعلیق_کار();
}
