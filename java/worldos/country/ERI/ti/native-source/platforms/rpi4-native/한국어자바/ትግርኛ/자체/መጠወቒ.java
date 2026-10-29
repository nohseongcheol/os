// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
/** 자체 화면에서 ስጉምቲ 알림을 보내는 መጠወቒ. */
public final class መጠወቒ extends 화면구성요소 {
    public መጠወቒ(String ጽሑፍ, int 가로, int 세로, int 폭, int 높이, 동작받이 받이) {
        throw new 상태예외("자체 JVM의 ትግርኛ መጠወቒ 생성 기능이 필요합니다.");
    }
    public native void 동작맡기기(동작받이 받이);
}
