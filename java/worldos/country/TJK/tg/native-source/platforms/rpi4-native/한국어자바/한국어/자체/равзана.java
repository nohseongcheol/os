// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 равзана 관리 기능에 직접 연결되는 равзана. */
public final class равзана extends 화면구성요소 {
    public равзана(String равзана_Унвон, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 한국어 равзана 생성 기능이 필요합니다.");
    }
    public native void илова_кардан_унсур(화면구성요소 унсур_қимат);
    public native void намоиш_додан_равзана();
    public native void Пӯшидан();
    public native boolean 보이는가();
}
