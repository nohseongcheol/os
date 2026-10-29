// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void yenza_umsebenzi() {
        for (int UKULANDELANA_inani = 0; UKULANDELANA_inani < 100; UKULANDELANA_inani++) { 합계++; 작업가닥.misa_okwesikhashana_umsebenzi(); }
    }
    public static void Sebenzisa() throws 대기중단예외 {
        한국어가닥시험 umsebenzi_isenzo = new 한국어가닥시험();
        작업가닥 uhlu_lwemilayezo_inani = new 작업가닥(umsebenzi_isenzo);
        검사.참인지(!uhlu_lwemilayezo_inani.살아있는가(), "Sebenzisa 전 isimo_inani");
        검사.참인지(!((Object)uhlu_lwemilayezo_inani instanceof Thread), "표준 가닥과 독립된 misa_inani");
        uhlu_lwemilayezo_inani.qala_umsebenzi(); uhlu_lwemilayezo_inani.기다리기();
        검사.참인지(umsebenzi_isenzo.합계 == 100 && !uhlu_lwemilayezo_inani.살아있는가(), "한글 uhlu_lwemilayezo_inani 실행과 기다림");
        try { uhlu_lwemilayezo_inani.qala_umsebenzi(); 검사.참인지(false, "중복 Sebenzisa 거부"); }
        catch (가닥상태예외 Iphutha) { 출력.bhala_umugqa("Isi_Zulu uhlu_lwemilayezo_inani 중복 Sebenzisa 거부"); }
        작업가닥 다음가닥 = 작업.Sebenzisa(umsebenzi_isenzo); 작업.기다리기(다음가닥);
        검사.참인지(umsebenzi_isenzo.합계 == 200 && !작업.살아있는가(다음가닥), "Isi_Zulu 작업 편의 umsebenzi_inani");
        검사.참인지(실행인수.개수() == 0, "빈 yenza_umyalo 인수");
        try { 실행인수.Itekisi(0); 검사.참인지(false, "인수 isiqeshana 검사"); }
        catch (범위예외 Iphutha) { 출력.bhala_umugqa("Isi_Zulu 인수 isiqeshana 거부"); }
        출력.bhala_umugqa("Isi_Zulu 직접 uhlu_lwemilayezo_inani dlulisa_inani");
    }
}
