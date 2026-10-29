// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
/** 작업 urutan_VALUE: 하나의 laksanakan_perintah strim_VALUE. Asli JVM 안에서 Perintah 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 Jalan(실행할일 tugas_cadangan) { 작업가닥 urutan_VALUE = new 작업가닥(tugas_cadangan); urutan_VALUE.Mula_tugas(); return urutan_VALUE; }
    public static void 기다리기(작업가닥 urutan_VALUE) throws 대기중단예외 { urutan_VALUE.기다리기(); }
    public static boolean 살아있는가(작업가닥 urutan_VALUE) { return urutan_VALUE.살아있는가(); }
    public static void YIELD_tugas() { 작업가닥.YIELD_tugas(); }
}
