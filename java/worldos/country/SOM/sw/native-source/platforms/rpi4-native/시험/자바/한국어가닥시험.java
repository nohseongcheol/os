// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void tekeleza_kazi() {
        for (int MFUATANO_thamani = 0; MFUATANO_thamani < 100; MFUATANO_thamani++) { 합계++; 작업가닥.ahirisha_kazi(); }
    }
    public static void endesha() throws 대기중단예외 {
        한국어가닥시험 kazi_Kitendo = new 한국어가닥시험();
        작업가닥 mtungo_thamani = new 작업가닥(kazi_Kitendo);
        검사.참인지(!mtungo_thamani.살아있는가(), "endesha 전 hali_thamani");
        검사.참인지(!((Object)mtungo_thamani instanceof Thread), "표준 가닥과 독립된 umbiza_thamani");
        mtungo_thamani.Anza_kazi(); mtungo_thamani.기다리기();
        검사.참인지(kazi_Kitendo.합계 == 100 && !mtungo_thamani.살아있는가(), "한글 mtungo_thamani 실행과 subiri_hali");
        try { mtungo_thamani.Anza_kazi(); 검사.참인지(false, "중복 endesha kataa_thamani"); }
        catch (mtungo_hali_vighairi kosa) { 출력.andika_laini("한국어 mtungo_thamani 중복 endesha kataa_thamani"); }
        작업가닥 다음가닥 = 작업.endesha(kazi_Kitendo); 작업.기다리기(다음가닥);
        검사.참인지(kazi_Kitendo.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 KITENDAKAZI_thamani");
        검사.참인지(실행인수.개수() == 0, "빈 tekeleza_amri 인수");
        try { 실행인수.SMS(0); 검사.참인지(false, "인수 dondoo 검사"); }
        catch (범위예외 kosa) { 출력.andika_laini("한국어 인수 dondoo kataa_thamani"); }
        출력.andika_laini("한국어 직접 mtungo_thamani pitisha_thamani");
    }
}
