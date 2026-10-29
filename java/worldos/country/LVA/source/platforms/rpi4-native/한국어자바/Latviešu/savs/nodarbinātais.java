// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** savs JVM 스케줄러가 관리하는 Izpildīt_komanda Stream_VALUE. 표준 Thread를 감싸지 않는다. */
public final class nodarbinātais {
    public nodarbinātais(실행할일 uzdevums_darbība) {
        throw new Statuss_izņēmums("savs JVM의 Latviešu 작업 saruna_VALUE ģenerēt 기능이 필요합니다.");
    }
    public native void Sākt_uzdevums() throws saruna_Statuss_izņēmums;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_uzdevums();
}
