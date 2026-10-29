// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** Öz JVM과 커널의 Pencere 관리 기능에 직접 연결되는 Pencere. */
public final class Pencere extends 화면구성요소 {
    public Pencere(String pencere_Başlık, int 폭, int 높이) {
        throw new Durum_özel_durum("Öz JVM의 Türkçe Pencere oluşturmak 기능이 필요합니다.");
    }
    public native void Ekle_öğe(화면구성요소 öğe_değer);
    public native void şov_pencere();
    public native void Kapat();
    public native boolean 보이는가();
}
