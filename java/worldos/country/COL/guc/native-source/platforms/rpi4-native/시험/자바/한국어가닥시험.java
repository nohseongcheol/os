// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void 실행하기() {
        for (int 차례 = 0; 차례 < 100; 차례++) { 합계++; 작업가닥.양보하기(); }
    }
    public static void 시작() throws 대기중단예외 {
        한국어가닥시험 aa_innajatü_aa_inra_awai = new 한국어가닥시험();
        작업가닥 akumajia_ipa_ajutuu = new 작업가닥(aa_innajatü_aa_inra_awai);
        검사.참인지(!akumajia_ipa_ajutuu.살아있는가(), "시작 전 jamakua_iparülein_ajutuu");
        검사.참인지(!((Object)akumajia_ipa_ajutuu instanceof Thread), "표준 가닥과 독립된 akua_ipaa_ajutuu");
        akumajia_ipa_ajutuu.achuwalaa_aa_innajatü(); akumajia_ipa_ajutuu.기다리기();
        검사.참인지(aa_innajatü_aa_inra_awai.합계 == 100 && !akumajia_ipa_ajutuu.살아있는가(), "한글 akumajia_ipa_ajutuu 실행과 기다림");
        try { akumajia_ipa_ajutuu.achuwalaa_aa_innajatü(); 검사.참인지(false, "중복 시작 거부"); }
        catch (가닥상태예외 ajachitia) { 출력.ashajaa_liinia("한국어 akumajia_ipa_ajutuu 중복 시작 거부"); }
        작업가닥 다음가닥 = 작업.시작(aa_innajatü_aa_inra_awai); 작업.기다리기(다음가닥);
        검사.참인지(aa_innajatü_aa_inra_awai.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 함수");
        검사.참인지(실행인수.개수() == 0, "빈 실행 인수");
        try { 실행인수.글(0); 검사.참인지(false, "인수 külipü_ayaakuaapijana 검사"); }
        catch (범위예외 ajachitia) { 출력.ashajaa_liinia("한국어 인수 külipü_ayaakuaapijana 거부"); }
        출력.ashajaa_liinia("한국어 직접 akumajia_ipa_ajutuu 통과");
    }
}
