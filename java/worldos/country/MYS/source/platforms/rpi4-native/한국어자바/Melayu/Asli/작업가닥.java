// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
/** Asli JVM 스케줄러가 관리하는 laksanakan_perintah strim_VALUE. 표준 Thread를 감싸지 않는다. */
public final class 작업가닥 {
    public 작업가닥(실행할일 tugas_cadangan) {
        throw new status_pengecualian("Asli JVM의 Melayu 작업 urutan_VALUE jana 기능이 필요합니다.");
    }
    public native void Mula_tugas() throws urutan_status_pengecualian;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_tugas();
}
