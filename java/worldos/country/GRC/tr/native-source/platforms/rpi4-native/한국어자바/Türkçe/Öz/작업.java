// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** 작업 yazışma_değer: 하나의 yürütmek_komut akış_değer. Öz JVM 안에서 komut 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static arkaPlanGörevi çalıştır(실행할일 Görev_Eylem) { arkaPlanGörevi yazışma_değer = new arkaPlanGörevi(Görev_Eylem); yazışma_değer.Start_Görev(); return yazışma_değer; }
    public static void 기다리기(arkaPlanGörevi yazışma_değer) throws 대기중단예외 { yazışma_değer.기다리기(); }
    public static boolean 살아있는가(arkaPlanGörevi yazışma_değer) { return yazışma_değer.살아있는가(); }
    public static void ÖDEME_Görev() { arkaPlanGörevi.ÖDEME_Görev(); }
}
