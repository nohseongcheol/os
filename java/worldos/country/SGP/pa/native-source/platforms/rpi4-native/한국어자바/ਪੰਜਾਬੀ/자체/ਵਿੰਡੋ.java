// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
/** 자체 JVM과 커널의 ਵਿੰਡੋ 관리 기능에 직접 연결되는 ਵਿੰਡੋ. */
public final class ਵਿੰਡੋ extends 화면구성요소 {
    public ਵਿੰਡੋ(String ਵਿੰਡੋ_ਸਿਰਲੇਖ, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 ਪੰਜਾਬੀ ਵਿੰਡੋ ਜਨਰੇਟ_ਕਰੋ 기능이 필요합니다.");
    }
    public native void ਜੋੜਨਾ_ਤੱਤ(화면구성요소 ਤੱਤ_ਕੀਮਤ);
    public native void ਸ਼ੋਅ_ਵਿੰਡੋ();
    public native void ਬੰਦ_ਕਰੋ();
    public native boolean 보이는가();
}
