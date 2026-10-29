// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.vlastiti.*;
public class 한국어가닥시험 implements 실행할일 {
    private int ukupni_zbroj_VALUE;
    public void Izvrši() {
        for (int SEQUENCE_VALUE = 0; SEQUENCE_VALUE < 100; SEQUENCE_VALUE++) { ukupni_zbroj_VALUE++; 작업가닥.YIELD_obaveza(); }
    }
    public static void Pokreni() throws 대기중단예외 {
        한국어가닥시험 obaveza_akcija = new 한국어가닥시험();
        작업가닥 nit_VALUE = new 작업가닥(obaveza_akcija);
        검사.참인지(!nit_VALUE.살아있는가(), "Pokreni 전 Stanje_VALUE");
        검사.참인지(!((Object)nit_VALUE instanceof Thread), "표준 가닥과 독립된 oblik_VALUE");
        nit_VALUE.START_obaveza(); nit_VALUE.기다리기();
        검사.참인지(obaveza_akcija.ukupni_zbroj_VALUE == 100 && !nit_VALUE.살아있는가(), "한글 nit_VALUE 실행과 stanje_čekanja");
        try { nit_VALUE.START_obaveza(); 검사.참인지(false, "중복 Pokreni odbiti_VALUE"); }
        catch (nit_Stanje_iznimka GREŠKA) { Izlaz.zapisivanje_red("hrvatski nit_VALUE 중복 Pokreni odbiti_VALUE"); }
        작업가닥 Dalje_nit = 작업.Pokreni(obaveza_akcija); 작업.기다리기(Dalje_nit);
        검사.참인지(obaveza_akcija.ukupni_zbroj_VALUE == 200 && !작업.살아있는가(Dalje_nit), "hrvatski 작업 편의 FUNCTION_VALUE");
        검사.참인지(실행인수.artikl_COUNT() == 0, "빈 Izvrši_naredba Argumenti");
        try { 실행인수.Tekst(0); 검사.참인지(false, "Argumenti isječak 검사"); }
        catch (범위예외 GREŠKA) { Izlaz.zapisivanje_red("hrvatski Argumenti isječak odbiti_VALUE"); }
        Izlaz.zapisivanje_red("hrvatski 직접 nit_VALUE proslijediti_VALUE");
    }
}
