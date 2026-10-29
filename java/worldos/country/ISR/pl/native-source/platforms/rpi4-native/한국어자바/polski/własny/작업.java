// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;
/** 작업 wątek_WARTOŚĆ: 하나의 Wykonaj_polecenie Stream_WARTOŚĆ. własny JVM 안에서 polecenie 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static pracownik Uruchom_2(실행할일 zadanie_akcja) { pracownik wątek_WARTOŚĆ = new pracownik(zadanie_akcja); wątek_WARTOŚĆ.START_zadanie(); return wątek_WARTOŚĆ; }
    public static void 기다리기(pracownik wątek_WARTOŚĆ) throws 대기중단예외 { wątek_WARTOŚĆ.기다리기(); }
    public static boolean 살아있는가(pracownik wątek_WARTOŚĆ) { return wątek_WARTOŚĆ.살아있는가(); }
    public static void Dochód_zadanie() { pracownik.Dochód_zadanie(); }
}
