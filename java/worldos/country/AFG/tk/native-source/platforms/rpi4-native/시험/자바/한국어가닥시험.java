// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void ýerine_ýetir_tabşyryk() {
        for (int SEQUENCE_baha = 0; SEQUENCE_baha < 100; SEQUENCE_baha++) { 합계++; 작업가닥.togtatmak_tabşyryk(); }
    }
    public static void Bitir() throws 대기중단예외 {
        한국어가닥시험 tabşyryk_iş = new 한국어가닥시험();
        작업가닥 akym_baha = new 작업가닥(tabşyryk_iş);
        검사.참인지(!akym_baha.살아있는가(), "Bitir 전 ýagdaý_baha");
        검사.참인지(!((Object)akym_baha instanceof Thread), "표준 가닥과 독립된 format_baha");
        akym_baha.başlat_tabşyryk(); akym_baha.기다리기();
        검사.참인지(tabşyryk_iş.합계 == 100 && !akym_baha.살아있는가(), "한글 akym_baha 실행과 기다림");
        try { akym_baha.başlat_tabşyryk(); 검사.참인지(false, "중복 Bitir 거부"); }
        catch (가닥상태예외 Hata) { 출력.ýaz_setir("한국어 akym_baha 중복 Bitir 거부"); }
        작업가닥 다음가닥 = 작업.Bitir(tabşyryk_iş); 작업.기다리기(다음가닥);
        검사.참인지(tabşyryk_iş.합계 == 200 && !작업.살아있는가(다음가닥), "한국어 작업 편의 FUNCTION_baha");
        검사.참인지(실행인수.개수() == 0, "빈 ýerine_ýetir_buýruk 인수");
        try { 실행인수.Metin(0); 검사.참인지(false, "인수 klip 검사"); }
        catch (범위예외 Hata) { 출력.ýaz_setir("한국어 인수 klip 거부"); }
        출력.ýaz_setir("한국어 직접 akym_baha 통과");
    }
}
