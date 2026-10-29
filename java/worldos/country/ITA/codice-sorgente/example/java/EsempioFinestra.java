// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.Finestra;
import Italiano.nativo.Etichetta;
import Italiano.nativo.campo_di_testo;
import Italiano.nativo.pulsante;
import Italiano.nativo.evento_coda;
import Italiano.nativo.uscitaTesto;
import Italiano.nativo.실행할일;
import Italiano.nativo.동작받이;
import Italiano.nativo.Action_informativa;

/** nativo 커널의 Swing Finestra: Italiano input_VALORE → pulsante → README_eb81d7d9 testo aggiornare. */
public class EsempioFinestra implements 실행할일, 동작받이 {
    private Finestra messaggio_di_saluto_finestra;
    private campo_di_testo nome_campo;
    private Etichetta messaggio_di_saluto;
    private int messaggio_di_saluto_CONTA_NUMERI;

    public void aperto_finestra() {
        messaggio_di_saluto_finestra = new Finestra("Italiano Swing", 460, 300);
        messaggio_di_saluto_finestra.Aggiungi_elemento(new Etichetta("Ciao", 20, 20, 420, 28));
        nome_campo = new campo_di_testo("Italiano", 20, 64, 420, 30);
        messaggio_di_saluto = new Etichetta("Ciao", 20, 152, 420, 28);
        messaggio_di_saluto_finestra.Aggiungi_elemento(nome_campo);
        messaggio_di_saluto_finestra.Aggiungi_elemento(new pulsante("인사하기", 20, 108, 180, 32, this));
        messaggio_di_saluto_finestra.Aggiungi_elemento(messaggio_di_saluto);
        messaggio_di_saluto_finestra.Aggiungi_elemento(new Etichetta("F9 / Shift+Space | X", 20, 204, 420, 28));
        messaggio_di_saluto_finestra.mostrare_finestra();
        uscitaTesto.scrivere_riga("GUI 예제 Prepara: EsempioFinestra");
    }

    public void 인사하기() {
        messaggio_di_saluto_CONTA_NUMERI++;
        messaggio_di_saluto.scrivere_SMS("Ciao, " + nome_campo.글읽기() + "님! (" + messaggio_di_saluto_CONTA_NUMERI + ")");
        uscitaTesto.scrivere_riga("GUI messaggio_di_saluto_ae353e94: " + messaggio_di_saluto.글읽기());
    }

    public void Esegui() { aperto_finestra(); }
    public void ricevere_Action(Action_informativa informativa) {
        uscitaTesto.scrivere_riga("Azione informativa: " + informativa.comando_SMS());
        인사하기();
    }
    public static void avvia() {
        evento_coda.나중에실행(new EsempioFinestra());
    }
}
