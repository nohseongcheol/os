// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** 작업 edefyn_VALUE: 하나의 Gweithredu_gorchymyn ffrwd_VALUE. 자체 JVM 안에서 Gorchymyn 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Gweithredu_2(실행할일 tasg_gweithred) { 작업가닥 edefyn_VALUE = new 작업가닥(tasg_gweithred); edefyn_VALUE.START_tasg(); return edefyn_VALUE; }
    public static void 기다리기(작업가닥 edefyn_VALUE) throws 대기중단예외 { edefyn_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 edefyn_VALUE) { return edefyn_VALUE.살아있는가(); }
    public static void atal_tasg() { 작업가닥.atal_tasg(); }
}
