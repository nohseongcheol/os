// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void ṣiṣẹ́_iṣẹ́() {
        for (int ÀTẸ̀LÉRA_iye = 0; ÀTẸ̀LÉRA_iye < 100; ÀTẸ̀LÉRA_iye++) { 합계++; 작업가닥.ti_dádúró_díẹ̀_iṣẹ́(); }
    }
    public static void Rọ́ọ̀nù() throws 대기중단예외 {
        한국어가닥시험 iṣẹ́_ìṣe = new 한국어가닥시험();
        작업가닥 èròjà_atẹ̀lélànà_iye = new 작업가닥(iṣẹ́_ìṣe);
        검사.참인지(!èròjà_atẹ̀lélànà_iye.살아있는가(), "Rọ́ọ̀nù 전 ipò_iye");
        검사.참인지(!((Object)èròjà_atẹ̀lélànà_iye instanceof Thread), "표준 가닥과 독립된 ìgúnrégé_iye");
        èròjà_atẹ̀lélànà_iye.bẹ̀rẹ̀_iṣẹ́(); èròjà_atẹ̀lélànà_iye.기다리기();
        검사.참인지(iṣẹ́_ìṣe.합계 == 100 && !èròjà_atẹ̀lélànà_iye.살아있는가(), "한글 èròjà_atẹ̀lélànà_iye 실행과 기다림");
        try { èròjà_atẹ̀lélànà_iye.bẹ̀rẹ̀_iṣẹ́(); 검사.참인지(false, "중복 Rọ́ọ̀nù 거부"); }
        catch (가닥상태예외 àṣìṣe) { 출력.kọ_ìlà("한국어 èròjà_atẹ̀lélànà_iye 중복 Rọ́ọ̀nù 거부"); }
        작업가닥 다음가닥 = 작업.Rọ́ọ̀nù(iṣẹ́_ìṣe); 작업.기다리기(다음가닥);
        검사.참인지(iṣẹ́_ìṣe.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 ÀKÀNṢEFỌMÚLÀ_iye");
        검사.참인지(실행인수.개수() == 0, "빈 ṣiṣẹ́_àṣẹ 인수");
        try { 실행인수.SMS(0); 검사.참인지(false, "인수 ní_ṣókí 검사"); }
        catch (범위예외 àṣìṣe) { 출력.kọ_ìlà("한국어 인수 ní_ṣókí 거부"); }
        출력.kọ_ìlà("한국어 직접 èròjà_atẹ̀lélànà_iye fí_dátà_ránṣẹ́_iye");
    }
}
