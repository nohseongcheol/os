// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.*;
public class 한국어가닥시험 implements 실행할일 {
    private int totale_VALORE;
    public void Esegui() {
        for (int SEQUENZA_VALORE = 0; SEQUENZA_VALORE < 100; SEQUENZA_VALORE++) { totale_VALORE++; esecutoreAsincrono.REND_task(); }
    }
    public static void avvia() throws 대기중단예외 {
        한국어가닥시험 task_Action = new 한국어가닥시험();
        esecutoreAsincrono thread_VALORE = new esecutoreAsincrono(task_Action);
        검사.참인지(!thread_VALORE.살아있는가(), "avvia 전 Stato_VALORE");
        검사.참인지(!((Object)thread_VALORE instanceof Thread), "표준 가닥과 독립된 formato_VALORE");
        thread_VALORE.START_task(); thread_VALORE.기다리기();
        검사.참인지(task_Action.totale_VALORE == 100 && !thread_VALORE.살아있는가(), "한글 thread_VALORE 실행과 stato_di_attesa");
        try { thread_VALORE.START_task(); 검사.참인지(false, "중복 avvia rifiutare_VALORE"); }
        catch (thread_Stato_eccezione errore) { uscitaTesto.scrivere_riga("Italiano thread_VALORE 중복 avvia rifiutare_VALORE"); }
        esecutoreAsincrono Avanti_thread = 작업.avvia(task_Action); 작업.기다리기(Avanti_thread);
        검사.참인지(task_Action.totale_VALORE == 200 && !작업.살아있는가(Avanti_thread), "Italiano 작업 편의 FUNZIONE_VALORE");
        검사.참인지(실행인수.articolo_CONTA_NUMERI() == 0, "빈 Esegui_comando argomenti");
        try { 실행인수.testo(0); 검사.참인지(false, "argomenti ritagliare 검사"); }
        catch (범위예외 errore) { uscitaTesto.scrivere_riga("Italiano argomenti ritagliare rifiutare_VALORE"); }
        uscitaTesto.scrivere_riga("Italiano 직접 thread_VALORE passare_VALORE");
    }
}
