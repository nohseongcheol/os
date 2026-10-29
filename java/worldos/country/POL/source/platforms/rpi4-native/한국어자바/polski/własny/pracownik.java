// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** własny JVM 스케줄러가 관리하는 Wykonaj_polecenie Stream_WARTOŚĆ. 표준 Thread를 감싸지 않는다. */
public final class pracownik {
    public pracownik(실행할일 zadanie_akcja) {
        throw new Stan_wyjątek("własny JVM의 polski 작업 wątek_WARTOŚĆ generować 기능이 필요합니다.");
    }
    public native void START_zadanie() throws wątek_Stan_wyjątek;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void Dochód_zadanie();
}
