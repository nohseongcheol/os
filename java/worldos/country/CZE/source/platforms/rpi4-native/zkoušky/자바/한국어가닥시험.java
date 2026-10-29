// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.*;
public class 한국어가닥시험 implements 실행할일 {
    private int celkem_HODNOTA;
    public void Spustit() {
        for (int SEQUENCE_HODNOTA = 0; SEQUENCE_HODNOTA < 100; SEQUENCE_HODNOTA++) { celkem_HODNOTA++; pracovník.YIELD_úkol(); }
    }
    public static void Spustit_2() throws 대기중단예외 {
        한국어가닥시험 úkol_Akce = new 한국어가닥시험();
        pracovník vlákno_HODNOTA = new pracovník(úkol_Akce);
        검사.참인지(!vlákno_HODNOTA.살아있는가(), "Spustit_2 전 Stav_HODNOTA");
        검사.참인지(!((Object)vlákno_HODNOTA instanceof Thread), "표준 가닥과 독립된 formát_HODNOTA");
        vlákno_HODNOTA.START_úkol(); vlákno_HODNOTA.기다리기();
        검사.참인지(úkol_Akce.celkem_HODNOTA == 100 && !vlákno_HODNOTA.살아있는가(), "한글 vlákno_HODNOTA 실행과 čekací_stav");
        try { vlákno_HODNOTA.START_úkol(); 검사.참인지(false, "중복 Spustit_2 odmítnout_HODNOTA"); }
        catch (vlákno_Stav_výjimka chyba) { výstupní_pozice.zápis_čára("čeština vlákno_HODNOTA 중복 Spustit_2 odmítnout_HODNOTA"); }
        pracovník Další_vlákno = 작업.Spustit_2(úkol_Akce); 작업.기다리기(Další_vlákno);
        검사.참인지(úkol_Akce.celkem_HODNOTA == 200 && !작업.살아있는가(Další_vlákno), "čeština 작업 편의 funkce_HODNOTA");
        검사.참인지(실행인수.zboží_POČET() == 0, "빈 Provést_příkaz argumenty");
        try { 실행인수.text(0); 검사.참인지(false, "argumenty oříznout 검사"); }
        catch (범위예외 chyba) { výstupní_pozice.zápis_čára("čeština argumenty oříznout odmítnout_HODNOTA"); }
        výstupní_pozice.zápis_čára("čeština 직접 vlákno_HODNOTA předat_HODNOTA");
    }
}
