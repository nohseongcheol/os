// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;
/** निज JVM 스케줄러가 관리하는 निष्पादित_करें_आदेश स्ट्रीम_मान. 표준 Thread를 감싸지 않는다. */
public final class कार्यसूत्र {
    public कार्यसूत्र(실행할일 कार्य_एक्शन) {
        throw new अवस्था_अपवाद("निज JVM의 हिंदी 작업 थ्रेड_मान जनरेट_करें 기능이 필요합니다.");
    }
    public native void प्रारंभ_कार्य() throws थ्रेड_अवस्था_अपवाद;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void स्थगित_करें_कार्य();
}
