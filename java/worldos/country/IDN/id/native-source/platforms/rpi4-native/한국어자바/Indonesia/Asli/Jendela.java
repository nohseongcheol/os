// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** Asli JVM과 커널의 Jendela 관리 기능에 직접 연결되는 Jendela. */
public final class Jendela extends 화면구성요소 {
    public Jendela(String jendela_Judul, int 폭, int 높이) {
        throw new Status_pengecualian("Asli JVM의 Indonesia Jendela buat 기능이 필요합니다.");
    }
    public native void tambah_elemen(화면구성요소 elemen_VALUE);
    public native void show_jendela();
    public native void Tutup();
    public native boolean 보이는가();
}
