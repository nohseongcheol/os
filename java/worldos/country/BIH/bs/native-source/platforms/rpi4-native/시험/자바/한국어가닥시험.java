// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;
public class 한국어가닥시험 implements 실행할일 {
    private int 합계;
    public void Izvrši() {
        for (int SEQUENCE_VALUE = 0; SEQUENCE_VALUE < 100; SEQUENCE_VALUE++) { 합계++; 작업가닥.YIELD_zadatak(); }
    }
    public static void Pokreni() throws 대기중단예외 {
        한국어가닥시험 zadatak_radnja = new 한국어가닥시험();
        작업가닥 nit_VALUE = new 작업가닥(zadatak_radnja);
        검사.참인지(!nit_VALUE.살아있는가(), "Pokreni 전 stanje_VALUE");
        검사.참인지(!((Object)nit_VALUE instanceof Thread), "표준 가닥과 독립된 format_VALUE");
        nit_VALUE.START_zadatak(); nit_VALUE.기다리기();
        검사.참인지(zadatak_radnja.합계 == 100 && !nit_VALUE.살아있는가(), "한글 nit_VALUE 실행과 čekaj_stanje");
        try { nit_VALUE.START_zadatak(); 검사.참인지(false, "중복 Pokreni odbiti_VALUE"); }
        catch (nit_stanje_izuzetak GRESKA) { Ispis.pisati_redak("한국어 nit_VALUE 중복 Pokreni odbiti_VALUE"); }
        작업가닥 Dalje_nit = 작업.Pokreni(zadatak_radnja); 작업.기다리기(Dalje_nit);
        검사.참인지(zadatak_radnja.합계 == 200 && !작업.살아있는가(Dalje_nit), "한국어 작업 편의 FUNCTION_VALUE");
        검사.참인지(실행인수.stavka_COUNT() == 0, "빈 Izvrši_komanda Argumenti");
        try { 실행인수.Tekst(0); 검사.참인지(false, "Argumenti isječak 검사"); }
        catch (범위예외 GRESKA) { Ispis.pisati_redak("한국어 Argumenti isječak odbiti_VALUE"); }
        Ispis.pisati_redak("한국어 직접 nit_VALUE proslijediti_VALUE");
    }
}
