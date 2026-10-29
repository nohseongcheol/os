// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM 스케줄러가 관리하는 అమలు_చేయి_ఆదేశం ధార_మూల్యం. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 విధి_చర్య) {
        throw new స్థితి_మినహాయింపు("자체 JVM의 한국어 작업 థ్రెడ్_మూల్యం రూపొందించు 기능이 필요합니다.");
    }
    public native void ప్రారంభం_విధి() throws థ్రెడ్_స్థితి_మినహాయింపు;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void తాత్కాలికంగా_నిలిపివేయి_విధి();
}
