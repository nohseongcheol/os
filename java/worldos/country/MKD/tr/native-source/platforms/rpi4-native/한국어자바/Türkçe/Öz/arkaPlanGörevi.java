// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** Öz JVM 스케줄러가 관리하는 yürütmek_komut akış_değer. 표준 Thread를 감싸지 않는다. */
public final class arkaPlanGörevi {
    public arkaPlanGörevi(실행할일 Görev_Eylem) {
        throw new Durum_özel_durum("Öz JVM의 Türkçe 작업 yazışma_değer oluşturmak 기능이 필요합니다.");
    }
    public native void Start_Görev() throws yazışma_Durum_özel_durum;
    public native void 기다리기() throws 대기중단예외;
    public native boolean 살아있는가();
    public static native void ÖDEME_Görev();
}
