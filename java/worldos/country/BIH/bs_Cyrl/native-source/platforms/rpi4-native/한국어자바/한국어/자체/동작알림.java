// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM догађај 처리기가 생성하는 радња 알림. */
public final class 동작알림 {
    private 동작알림() {}
    public native String команда_текст();
    public native 화면구성요소 догађај_извор();
    public native int индекс();
}
