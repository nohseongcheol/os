// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void phethagatša_mošomo() {
        for (int TATELANO_boleng = 0; TATELANO_boleng < 100; TATELANO_boleng++) { 합계++; 작업가닥.e_thibetšwe_mošomo(); }
    }
    public static void Diriša() throws 대기중단예외 {
        한국어가닥시험 mošomo_tiro = new 한국어가닥시험();
        작업가닥 threte_boleng = new 작업가닥(mošomo_tiro);
        검사.참인지(!threte_boleng.살아있는가(), "Diriša 전 boemo_boleng");
        검사.참인지(!((Object)threte_boleng instanceof Thread), "표준 가닥과 독립된 fomete_boleng");
        threte_boleng.Thomišo_mošomo(); threte_boleng.기다리기();
        검사.참인지(mošomo_tiro.합계 == 100 && !threte_boleng.살아있는가(), "한글 threte_boleng 실행과 기다림");
        try { threte_boleng.Thomišo_mošomo(); 검사.참인지(false, "중복 Diriša 거부"); }
        catch (가닥상태예외 Phošo) { 출력.ngwala_mothaladi("한국어 threte_boleng 중복 Diriša 거부"); }
        작업가닥 다음가닥 = 작업.Diriša(mošomo_tiro); 작업.기다리기(다음가닥);
        검사.참인지(mošomo_tiro.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 TIRO_boleng");
        검사.참인지(실행인수.개수() == 0, "빈 phethagatša_taelo 인수");
        try { 실행인수.Sengwalwa(0); 검사.참인지(false, "인수 setsopolwa 검사"); }
        catch (범위예외 Phošo) { 출력.ngwala_mothaladi("한국어 인수 setsopolwa 거부"); }
        출력.ngwala_mothaladi("한국어 직접 threte_boleng feta_boleng");
    }
}
