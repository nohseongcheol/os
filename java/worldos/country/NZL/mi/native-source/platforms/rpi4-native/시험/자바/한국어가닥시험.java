// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void kawe_tūmahi() {
        for (int SEQUENCE_uara = 0; SEQUENCE_uara < 100; SEQUENCE_uara++) { 합계++; 작업가닥.YIELD_tūmahi(); }
    }
    public static void whakahaere() throws 대기중단예외 {
        한국어가닥시험 tūmahi_hohenga = new 한국어가닥시험();
        작업가닥 miro_uara = new 작업가닥(tūmahi_hohenga);
        검사.참인지(!miro_uara.살아있는가(), "whakahaere 전 tūnga_uara");
        검사.참인지(!((Object)miro_uara instanceof Thread), "표준 가닥과 독립된 hōputu_uara");
        miro_uara.Start_tūmahi(); miro_uara.기다리기();
        검사.참인지(tūmahi_hohenga.합계 == 100 && !miro_uara.살아있는가(), "한글 miro_uara 실행과 기다림");
        try { miro_uara.Start_tūmahi(); 검사.참인지(false, "중복 whakahaere 거부"); }
        catch (가닥상태예외 Pōhēhē) { 출력.tuhi_hononga("Reo_Māori miro_uara 중복 whakahaere 거부"); }
        작업가닥 Panuku_miro = 작업.whakahaere(tūmahi_hohenga); 작업.기다리기(Panuku_miro);
        검사.참인지(tūmahi_hohenga.합계 == 200 && !작업.살아있는가(Panuku_miro), "Reo_Māori 작업 편의 TAUMAHI_uara");
        검사.참인지(실행인수.tuemi_COUNT() == 0, "빈 kawe_tono 인수");
        try { 실행인수.Ngā_kupu(0); 검사.참인지(false, "인수 topenga 검사"); }
        catch (범위예외 Pōhēhē) { 출력.tuhi_hononga("Reo_Māori 인수 topenga 거부"); }
        출력.tuhi_hononga("Reo_Māori 직접 miro_uara whakawhiti_uara");
    }
}
