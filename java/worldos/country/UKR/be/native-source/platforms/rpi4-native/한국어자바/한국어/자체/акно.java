// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 자체 JVM과 커널의 акно 관리 기능에 직접 연결되는 акно. */
public final class акно extends 화면구성요소 {
    public акно(String акно_Загаловак, int 폭, int 높이) {
        throw new стан_выключэнне("자체 JVM의 한국어 акно 생성 기능이 필요합니다.");
    }
    public native void дадаць_элемент(화면구성요소 элемент_значэнне);
    public native void паказаць_акно();
    public native void Закрыць();
    public native boolean 보이는가();
}
