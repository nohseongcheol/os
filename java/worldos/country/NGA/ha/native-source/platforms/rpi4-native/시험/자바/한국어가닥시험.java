// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void gudanar_aiki() {
        for (int JERI_Daraja = 0; JERI_Daraja < 100; JERI_Daraja++) { 합계++; 작업가닥.ɗan_tsai_da_aiki(); }
    }
    public static void Tafiyar_da() throws 대기중단예외 {
        한국어가닥시험 aiki_Aiki = new 한국어가닥시험();
        작업가닥 hira_Daraja = new 작업가닥(aiki_Aiki);
        검사.참인지(!hira_Daraja.살아있는가(), "Tafiyar_da 전 Matsayi_Daraja");
        검사.참인지(!((Object)hira_Daraja instanceof Thread), "표준 가닥과 독립된 zubi_Daraja");
        hira_Daraja.Fara_aiki(); hira_Daraja.기다리기();
        검사.참인지(aiki_Aiki.합계 == 100 && !hira_Daraja.살아있는가(), "한글 hira_Daraja 실행과 jira_Matsayi");
        try { hira_Daraja.Fara_aiki(); 검사.참인지(false, "중복 Tafiyar_da kore_Daraja"); }
        catch (hira_Matsayi_banbanchi Kuskure) { 출력.Rubuta_Layi("한국어 hira_Daraja 중복 Tafiyar_da kore_Daraja"); }
        작업가닥 다음가닥 = 작업.Tafiyar_da(aiki_Aiki); 작업.기다리기(다음가닥);
        검사.참인지(aiki_Aiki.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 AIKI_Daraja");
        검사.참인지(실행인수.개수() == 0, "빈 gudanar_Umarni 인수");
        try { 실행인수.SMS(0); 검사.참인지(false, "인수 darfi 검사"); }
        catch (범위예외 Kuskure) { 출력.Rubuta_Layi("한국어 인수 darfi kore_Daraja"); }
        출력.Rubuta_Layi("한국어 직접 hira_Daraja 통과");
    }
}
