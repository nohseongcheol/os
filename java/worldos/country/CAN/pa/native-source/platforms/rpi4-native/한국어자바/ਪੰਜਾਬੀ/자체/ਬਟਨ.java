// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
/** 자체 화면에서 ਐਕਸ਼ਨ 알림을 보내는 ਬਟਨ. */
public final class ਬਟਨ extends 화면구성요소 {
    public ਬਟਨ(String ਟੈਕਸਟ, int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 폭, int 높이, 동작받이 받이) {
        throw new 상태예외("자체 JVM의 ਪੰਜਾਬੀ ਬਟਨ ਜਨਰੇਟ_ਕਰੋ 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
