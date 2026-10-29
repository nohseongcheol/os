// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package slovenščina.lastno;
/** lastno JVM 스케줄러가 관리하는 Izvedi_ukaz tok_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 opravek_akcija) {
        throw new stanje_izjema("lastno JVM의 slovenščina 작업 nit_VALUE ustvariti 기능이 필요합니다.");
    }
    public native void Start_opravek() throws nit_stanje_izjema;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_opravek();
}
