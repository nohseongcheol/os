// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** 작업 alur_VALUE: 하나의 Jalankan_perintah Stream_VALUE. Asli JVM 안에서 perintah 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static tugasLatar jalankan(실행할일 tugas_Tugas) { tugasLatar alur_VALUE = new tugasLatar(tugas_Tugas); alur_VALUE.Mulai_tugas(); return alur_VALUE; }
    public static void 기다리기(tugasLatar alur_VALUE) throws 대기중단예외 { alur_VALUE.기다리기(); }
    public static boolean 살아있는가(tugasLatar alur_VALUE) { return alur_VALUE.살아있는가(); }
    public static void YIELD_tugas() { tugasLatar.YIELD_tugas(); }
}
