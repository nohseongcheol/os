// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.निज;
/** निज JVM과 커널의 सन्झ्याल 관리 기능에 직접 연결되는 सन्झ्याल. */
public final class सन्झ्याल extends 화면구성요소 {
    public सन्झ्याल(String सन्झ्याल_शिर्षक, int 폭, int 높이) {
        throw new 상태예외("निज JVM의 नेपाली सन्झ्याल सिर्जना_गर्नुहोस् 기능이 필요합니다.");
    }
    public native void थप्नुहोस्_तत्त्व(화면구성요소 तत्त्व_मान);
    public native void शो_सन्झ्याल();
    public native void बन्दगर्नुहोस्();
    public native boolean 보이는가();
}
