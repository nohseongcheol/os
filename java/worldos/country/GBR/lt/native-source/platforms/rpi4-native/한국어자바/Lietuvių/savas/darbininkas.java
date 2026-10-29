// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** savas JVM 스케줄러가 관리하는 Vykdyti_komanda Stream_VALUE. 표준 Thread를 감싸지 않는다. */
public final class darbininkas {
    public darbininkas(실행할일 užduotis_gavinys) {
        throw new Būsena_išimtis("savas JVM의 Lietuvių 작업 gija_VALUE generuoti 기능이 필요합니다.");
    }
    public native void Start_užduotis() throws gija_Būsena_išimtis;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_užduotis();
}
