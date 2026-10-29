// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Татарча.자체;
/** 자체 JVM과 커널의 тәрәз 관리 기능에 직접 연결되는 тәрәз. */
public final class тәрәз extends 화면구성요소 {
    public тәрәз(String тәрәз_Башлам, int 폭, int 높이) {
        throw new 상태예외("자체 JVM의 Татарча тәрәз булдыру 기능이 필요합니다.");
    }
    public native void өстәү_элемент(화면구성요소 элемент_VALUE);
    public native void күрсәтү_тәрәз();
    public native void Yap();
    public native boolean 보이는가();
}
