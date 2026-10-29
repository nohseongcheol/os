// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** Asli JVM 스케줄러가 관리하는 Jalankan_perintah Stream_VALUE. 표준 Thread를 감싸지 않는다. */
public final class tugasLatar {
    public tugasLatar(실행할일 tugas_Tugas) {
        throw new Status_pengecualian("Asli JVM의 Indonesia 작업 alur_VALUE buat 기능이 필요합니다.");
    }
    public native void Mulai_tugas() throws alur_Status_pengecualian;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void YIELD_tugas();
}
