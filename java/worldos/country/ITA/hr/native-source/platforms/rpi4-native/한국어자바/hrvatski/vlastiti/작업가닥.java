// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** vlastiti JVM 스케줄러가 관리하는 Izvrši_naredba tok_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 obaveza_akcija) {
        throw new Stanje_iznimka("vlastiti JVM의 hrvatski 작업 nit_VALUE generirati 기능이 필요합니다.");
    }
    public native void START_obaveza() throws nit_Stanje_iznimka;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_obaveza();
}
