// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
/** 자체 JVM 스케줄러가 관리하는 ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ ਸਟ੍ਰੀਮ_ਕੀਮਤ. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ਕਾਰਜ_ਕਿਰਿਆ) {
        throw new 상태예외("자체 JVM의 ਪੰਜਾਬੀ 작업 ਥ੍ਰੈਡ_ਕੀਮਤ ਜਨਰੇਟ_ਕਰੋ 기능이 필요합니다.");
    }
    public native void ਸੁਰੂ_ਕਾਰਜ() throws 가닥상태예외;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void ਮੁਅੱਤਲ_ਕਾਰਜ();
}
