// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void 실행하기() {
        for (int 차례 = 0; 차례 < 100; 차례++) { 합계++; 작업가닥.양보하기(); }
    }
    public static void huutoraade() throws 대기중단예외 {
        한국어가닥시험 golle_gollal = new 한국어가닥시험();
        작업가닥 piilol_njaru = new 작업가닥(golle_gollal);
        검사.참인지(!piilol_njaru.살아있는가(), "huutoraade 전 ngonka_njaru");
        검사.참인지(!((Object)piilol_njaru instanceof Thread), "표준 가닥과 독립된 formaa_njaru");
        piilol_njaru.huɓɓude_golle(); piilol_njaru.기다리기();
        검사.참인지(golle_gollal.합계 == 100 && !piilol_njaru.살아있는가(), "한글 piilol_njaru 실행과 기다림");
        try { piilol_njaru.huɓɓude_golle(); 검사.참인지(false, "중복 huutoraade 거부"); }
        catch (가닥상태예외 juumre) { 출력.winndude_diidol("한국어 piilol_njaru 중복 huutoraade 거부"); }
        작업가닥 다음가닥 = 작업.huutoraade(golle_gollal); 작업.기다리기(다음가닥);
        검사.참인지(golle_gollal.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 juɓɓol_njaru");
        검사.참인지(실행인수.개수() == 0, "빈 실행 인수");
        try { 실행인수.binndi(0); 검사.참인지(false, "인수 kilip 검사"); }
        catch (범위예외 juumre) { 출력.winndude_diidol("한국어 인수 kilip 거부"); }
        출력.winndude_diidol("한국어 직접 piilol_njaru 통과");
    }
}
