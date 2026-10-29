// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ગુજરાતી.자체;
/** 자체 JVM과 커널의 વિંડો 관리 기능에 직접 연결되는 વિંડો. */
public final class વિંડો extends 화면구성요소 {
    public વિંડો(String વિંડો_શીર્ષક, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 ગુજરાતી વિંડો જનરેટ_કરો 기능이 필요합니다.");
    }
    public native void ઍડ_કરો_તત્વ(화면구성요소 તત્વ_મૂલ્ય);
    public native void શૉ_વિંડો();
    public native void બંધ_કરો();
    public native boolean 보이는가();
}
