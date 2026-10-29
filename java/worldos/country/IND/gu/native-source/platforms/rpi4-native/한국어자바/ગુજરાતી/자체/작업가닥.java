// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** 자체 JVM 스케줄러가 관리하는 અમલ_કરો_આદેશ સ્ટ્રીમ_મૂલ્ય. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 કાર્ય_સંદેશ) {
        throw new 상태예외("자체 JVM의 ગુજરાતી 작업 થ્રેડ_મૂલ્ય જનરેટ_કરો 기능이 필요합니다.");
    }
    public native void પ્રારંભ_કાર્ય() throws 가닥상태예외;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void સ્થગિત_કરો_કાર્ય();
}
