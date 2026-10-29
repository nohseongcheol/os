// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** 작업 saruna_VALUE: 하나의 Izpildīt_komanda Stream_VALUE. savs JVM 안에서 Komanda 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static nodarbinātais Palaist(실행할일 uzdevums_darbība) { nodarbinātais saruna_VALUE = new nodarbinātais(uzdevums_darbība); saruna_VALUE.Sākt_uzdevums(); return saruna_VALUE; }
    public static void 기다리기(nodarbinātais saruna_VALUE) throws 대기중단예외 { saruna_VALUE.기다리기(); }
    public static boolean 살아있는가(nodarbinātais saruna_VALUE) { return saruna_VALUE.살아있는가(); }
    public static void YIELD_uzdevums() { nodarbinātais.YIELD_uzdevums(); }
}
