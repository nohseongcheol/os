// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
/** Asli JVM과 커널의 Tetingkap 관리 기능에 직접 연결되는 Tetingkap. */
public final class Tetingkap extends 화면구성요소 {
    public Tetingkap(String tetingkap_Tajuk, int 폭, int 높이) {
        throw new status_pengecualian("Asli JVM의 Melayu Tetingkap jana 기능이 필요합니다.");
    }
    public native void tambah_unsur(화면구성요소 unsur_VALUE);
    public native void tayang_tetingkap();
    public native void Tutup();
    public native boolean 보이는가();
}
