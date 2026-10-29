// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;
/** 작업 þráður_VALUE: 하나의 keyra_skipun Stream_VALUE. eigin JVM 안에서 Skipun 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static starfskraftur Keyra_2(실행할일 verk_aðgerð) { starfskraftur þráður_VALUE = new starfskraftur(verk_aðgerð); þráður_VALUE.Opna_verk(); return þráður_VALUE; }
    public static void 기다리기(starfskraftur þráður_VALUE) throws 대기중단예외 { þráður_VALUE.기다리기(); }
    public static boolean 살아있는가(starfskraftur þráður_VALUE) { return þráður_VALUE.살아있는가(); }
    public static void YIELD_verk() { starfskraftur.YIELD_verk(); }
}
