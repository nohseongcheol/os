// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.*;
public class 한국어가닥시험 implements 실행할일 {
    private int total_VERDI;
    public void Kjør() {
        for (int SEKVENS_VERDI = 0; SEKVENS_VERDI < 100; SEKVENS_VERDI++) { total_VERDI++; arbeider.AVKAST_oppgave(); }
    }
    public static void Kjør_2() throws 대기중단예외 {
        한국어가닥시험 oppgave_Gjøremål = new 한국어가닥시험();
        arbeider tråd_VERDI = new arbeider(oppgave_Gjøremål);
        검사.참인지(!tråd_VERDI.살아있는가(), "Kjør_2 전 status_VERDI");
        검사.참인지(!((Object)tråd_VERDI instanceof Thread), "표준 가닥과 독립된 format_VERDI");
        tråd_VERDI.START_oppgave(); tråd_VERDI.기다리기();
        검사.참인지(oppgave_Gjøremål.total_VERDI == 100 && !tråd_VERDI.살아있는가(), "한글 tråd_VERDI 실행과 ventende_tilstand");
        try { tråd_VERDI.START_oppgave(); 검사.참인지(false, "중복 Kjør_2 avvise_VERDI"); }
        catch (tråd_status_unntak feil) { Utgang.skrive_linje("norsk tråd_VERDI 중복 Kjør_2 avvise_VERDI"); }
        arbeider Neste_tråd = 작업.Kjør_2(oppgave_Gjøremål); 작업.기다리기(Neste_tråd);
        검사.참인지(oppgave_Gjøremål.total_VERDI == 200 && !작업.살아있는가(Neste_tråd), "norsk 작업 편의 FUNKSJON_VERDI");
        검사.참인지(실행인수.vare_ANTALL() == 0, "빈 Utfør_kommando Argumenter");
        try { 실행인수.Tekst(0); 검사.참인지(false, "Argumenter klippe 검사"); }
        catch (범위예외 feil) { Utgang.skrive_linje("norsk Argumenter klippe avvise_VERDI"); }
        Utgang.skrive_linje("norsk 직접 tråd_VERDI sende_VERDI");
    }
}
