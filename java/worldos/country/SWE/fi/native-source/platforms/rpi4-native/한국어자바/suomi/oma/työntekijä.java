// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package suomi.oma;
/** oma JVM 스케줄러가 관리하는 Suorita_komento virta_ARVO. 표준 Thread를 감싸지 않는다. */
public final class työntekijä {
    public työntekijä(실행할일 tehtävä_toimi) {
        throw new Tila_poikkeus("oma JVM의 suomi 작업 säie_ARVO generoida 기능이 필요합니다.");
    }
    public native void alku_tehtävä() throws säie_Tila_poikkeus;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void TUOTTO_tehtävä();
}
