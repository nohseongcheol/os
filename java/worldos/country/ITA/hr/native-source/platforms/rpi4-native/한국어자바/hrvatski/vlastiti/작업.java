// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;
/** 작업 nit_VALUE: 하나의 Izvrši_naredba tok_VALUE. vlastiti JVM 안에서 Naredba 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Pokreni(실행할일 obaveza_akcija) { 작업가닥 nit_VALUE = new 작업가닥(obaveza_akcija); nit_VALUE.START_obaveza(); return nit_VALUE; }
    public static void 기다리기(작업가닥 nit_VALUE) throws 대기중단예외 { nit_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 nit_VALUE) { return nit_VALUE.살아있는가(); }
    public static void YIELD_obaveza() { 작업가닥.YIELD_obaveza(); }
}
