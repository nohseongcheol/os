// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
/** 자체 JVM 스케줄러가 관리하는 ፈጽም_ትእዛዝ ልቀቅ_እሴት. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 ተግባር_ምክር) {
        throw new ዞን_ልዩነት("자체 JVM의 አማርኛ 작업 ክር_እሴት አዘጋጅ 기능이 필요합니다.");
    }
    public native void ጀምር_ተግባር() throws ክር_ዞን_ልዩነት;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void አግድ_ተግባር();
}
