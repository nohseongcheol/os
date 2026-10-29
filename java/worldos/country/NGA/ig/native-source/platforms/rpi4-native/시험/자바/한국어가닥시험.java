// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void mee_ọrụ() {
        for (int NSOTANSO_valuu = 0; NSOTANSO_valuu < 100; NSOTANSO_valuu++) { 합계++; 작업가닥.kwụsịtụ_ọrụ(); }
    }
    public static void Bido() throws 대기중단예외 {
        한국어가닥시험 ọrụ_mmèm = new 한국어가닥시험();
        작업가닥 treèd_valuu = new 작업가닥(ọrụ_mmèm);
        검사.참인지(!treèd_valuu.살아있는가(), "Bido 전 ọnọdụ_valuu");
        검사.참인지(!((Object)treèd_valuu instanceof Thread), "표준 가닥과 독립된 hàzie_valuu");
        treèd_valuu.Mbido_ọrụ(); treèd_valuu.기다리기();
        검사.참인지(ọrụ_mmèm.합계 == 100 && !treèd_valuu.살아있는가(), "한글 treèd_valuu 실행과 기다림");
        try { treèd_valuu.Mbido_ọrụ(); 검사.참인지(false, "중복 Bido 거부"); }
        catch (가닥상태예외 mmejọ) { 출력.dee_ahịrī("한국어 treèd_valuu 중복 Bido 거부"); }
        작업가닥 다음가닥 = 작업.Bido(ọrụ_mmèm); 작업.기다리기(다음가닥);
        검사.참인지(ọrụ_mmèm.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 ọrụ_valuu");
        검사.참인지(실행인수.개수() == 0, "빈 mee_nnyemiwu 인수");
        try { 실행인수.SMS(0); 검사.참인지(false, "인수 ntipanye 검사"); }
        catch (범위예외 mmejọ) { 출력.dee_ahịrī("한국어 인수 ntipanye 거부"); }
        출력.dee_ahịrī("한국어 직접 treèd_valuu 통과");
    }
}
