// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.oma.*;
public class 한국어가닥시험 implements 실행할일 {
    private int kokku_VALUE;
    public void Käivita() {
        for (int SEQUENCE_VALUE = 0; SEQUENCE_VALUE < 100; SEQUENCE_VALUE++) { kokku_VALUE++; töötaja.YIELD_tööüksus(); }
    }
    public static void Käivita_2() throws 대기중단예외 {
        한국어가닥시험 tööüksus_Toiming = new 한국어가닥시험();
        töötaja lõim_VALUE = new töötaja(tööüksus_Toiming);
        검사.참인지(!lõim_VALUE.살아있는가(), "Käivita_2 전 Olek_VALUE");
        검사.참인지(!((Object)lõim_VALUE instanceof Thread), "표준 가닥과 독립된 vorming_VALUE");
        lõim_VALUE.START_tööüksus(); lõim_VALUE.기다리기();
        검사.참인지(tööüksus_Toiming.kokku_VALUE == 100 && !lõim_VALUE.살아있는가(), "한글 lõim_VALUE 실행과 ooteolek");
        try { lõim_VALUE.START_tööüksus(); 검사.참인지(false, "중복 Käivita_2 keelduma_VALUE"); }
        catch (lõim_Olek_erand VIGA) { Väljund.kirjutamine_liin("Eesti lõim_VALUE 중복 Käivita_2 keelduma_VALUE"); }
        töötaja Edasi_lõim = 작업.Käivita_2(tööüksus_Toiming); 작업.기다리기(Edasi_lõim);
        검사.참인지(tööüksus_Toiming.kokku_VALUE == 200 && !작업.살아있는가(Edasi_lõim), "Eesti 작업 편의 FUNCTION_VALUE");
        검사.참인지(실행인수.kaup_COUNT() == 0, "빈 Täida_käsk Argumendid");
        try { 실행인수.Tekst(0); 검사.참인지(false, "Argumendid klipp 검사"); }
        catch (범위예외 VIGA) { Väljund.kirjutamine_liin("Eesti Argumendid klipp keelduma_VALUE"); }
        Väljund.kirjutamine_liin("Eesti 직접 lõim_VALUE edastama_VALUE");
    }
}
