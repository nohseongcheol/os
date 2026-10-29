// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void 실행하기() {
        for (int 차례 = 0; 차례 < 100; 차례++) { 합계++; 작업가닥.양보하기(); }
    }
    public static void 시작() throws 대기중단예외 {
        한국어가닥시험 sujassaq_sugiarut = new 한국어가닥시험();
        작업가닥 aqqusiqtarvik_atuutilik = new 작업가닥(sujassaq_sugiarut);
        검사.참인지(!aqqusiqtarvik_atuutilik.살아있는가(), "시작 전 qanuilinganiq_atuutilik");
        검사.참인지(!((Object)aqqusiqtarvik_atuutilik instanceof Thread), "표준 가닥과 독립된 aaqqisurli_atuutilik");
        aqqusiqtarvik_atuutilik.pigiarli_sujassaq(); aqqusiqtarvik_atuutilik.기다리기();
        검사.참인지(sujassaq_sugiarut.합계 == 100 && !aqqusiqtarvik_atuutilik.살아있는가(), "한글 aqqusiqtarvik_atuutilik 실행과 기다림");
        try { aqqusiqtarvik_atuutilik.pigiarli_sujassaq(); 검사.참인지(false, "중복 시작 거부"); }
        catch (가닥상태예외 tammarniq) { 출력.titiraq_titikutaak("한국어 aqqusiqtarvik_atuutilik 중복 시작 거부"); }
        작업가닥 다음가닥 = 작업.시작(sujassaq_sugiarut); 작업.기다리기(다음가닥);
        검사.참인지(sujassaq_sugiarut.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 sugiakkannirut_atuutilik");
        검사.참인지(실행인수.개수() == 0, "빈 실행 인수");
        try { 실행인수.titiqqaq(0); 검사.참인지(false, "인수 Nakatigat 검사"); }
        catch (범위예외 tammarniq) { 출력.titiraq_titikutaak("한국어 인수 Nakatigat 거부"); }
        출력.titiraq_titikutaak("한국어 직접 aqqusiqtarvik_atuutilik 통과");
    }
}
