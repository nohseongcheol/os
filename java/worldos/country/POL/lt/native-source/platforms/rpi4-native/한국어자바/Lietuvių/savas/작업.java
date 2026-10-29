// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;
/** 작업 gija_VALUE: 하나의 Vykdyti_komanda Stream_VALUE. savas JVM 안에서 Komanda 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static darbininkas Paleisti(실행할일 užduotis_gavinys) { darbininkas gija_VALUE = new darbininkas(užduotis_gavinys); gija_VALUE.Start_užduotis(); return gija_VALUE; }
    public static void 기다리기(darbininkas gija_VALUE) throws 대기중단예외 { gija_VALUE.기다리기(); }
    public static boolean 살아있는가(darbininkas gija_VALUE) { return gija_VALUE.살아있는가(); }
    public static void YIELD_užduotis() { darbininkas.YIELD_užduotis(); }
}
