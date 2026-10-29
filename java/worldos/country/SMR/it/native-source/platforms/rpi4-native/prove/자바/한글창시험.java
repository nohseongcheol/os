// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.Finestra;
import Italiano.nativo.elemento_grafico;
import Italiano.nativo.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Finestra schermata;
    Etichetta README_eb81d7d9;
    campo_di_testo input_VALORE;
    public void Esegui() {
        검사.참인지(evento_coda.사건처리중인가(), "Italiano schermata 작업 큐");
        schermata = new Finestra("Italiano Catalogo Finestra", 400, 280);
        README_eb81d7d9 = elemento_grafico.tag_VALORE("한글로 Java 코딩", 20, 20, 340, 30);
        input_VALORE = elemento_grafico.campo_di_testo("Nome", 20, 65, 340, 30);
        schermata.Aggiungi_elemento(README_eb81d7d9);
        schermata.Aggiungi_elemento(input_VALORE);
        schermata.Aggiungi_elemento(elemento_grafico.pulsante("인사하기", 20, 110, 180, 32, this));
        schermata.mostrare_finestra();
        uscitaTesto.scrivere_riga("KOREAN SWING READY");
    }
    public void ricevere_Action(Action_informativa Evento) {
        검사.참인지(evento_coda.사건처리중인가(), "Italiano Azione 되부름");
        검사.참인지(Evento.INDICE() == 1001 && Evento.origine_evento() instanceof pulsante, "Italiano Evento 객체와 origine_VALORE");
        검사.참인지(!((Object)Evento.origine_evento() instanceof javax.swing.JButton), "표준 단추와 독립된 formato_VALORE");
        검사.참인지(!((Object)Evento instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formato_VALORE");
        README_eb81d7d9.scrivere_SMS("안녕하세요 " + input_VALORE.글읽기());
        uscitaTesto.scrivere_riga("KOREAN SWING CLICK " + input_VALORE.글읽기());
    }
    public static void main(String[] argomenti) {
        evento_coda.나중에실행(new 한글창시험());
    }
}
