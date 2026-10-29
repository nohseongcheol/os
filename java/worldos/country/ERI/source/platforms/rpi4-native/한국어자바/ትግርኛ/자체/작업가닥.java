// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
/** 자체 JVM 스케줄러가 관리하는 ተግብር_ትእዛዝ ወሓዚ_ዋጋ. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ዕማም_ስጉምቲ) {
        throw new 상태예외("자체 JVM의 ትግርኛ 작업 ፈትሊ_ዋጋ 생성 기능이 필요합니다.");
    }
    public native void ጀምር_ዕማም() throws 가닥상태예외;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void አግድ_ዕማም();
}
