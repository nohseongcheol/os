// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.nativo.Janela;
import Português.nativo.elemento_de_ecrã;
import Português.nativo.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Janela tela;
    Etiqueta LEIAME_eb81d7d9;
    campo_de_texto entrada_VALOR;
    public void Executar() {
        검사.참인지(Evento_Fila.사건처리중인가(), "Português tela 작업 큐");
        tela = new Janela("Português biblioteca Janela", 400, 280);
        LEIAME_eb81d7d9 = elemento_de_ecrã.tag_VALOR("한글로 Java 코딩", 20, 20, 340, 30);
        entrada_VALOR = elemento_de_ecrã.campo_de_texto("Nome", 20, 65, 340, 30);
        tela.Adicionar_elemento(LEIAME_eb81d7d9);
        tela.Adicionar_elemento(entrada_VALOR);
        tela.Adicionar_elemento(elemento_de_ecrã.botão("인사하기", 20, 110, 180, 32, this));
        tela.mostrar_janela();
        saídaTexto.gravar_linha("KOREAN SWING READY");
    }
    public void receber_Ação(Ação_aviso Evento) {
        검사.참인지(Evento_Fila.사건처리중인가(), "Português Acção 되부름");
        검사.참인지(Evento.ÍNDICE() == 1001 && Evento.origem_do_evento() instanceof botão, "Português Evento 객체와 origem_VALOR");
        검사.참인지(!((Object)Evento.origem_do_evento() instanceof javax.swing.JButton), "표준 단추와 독립된 formato_VALOR");
        검사.참인지(!((Object)Evento instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formato_VALOR");
        LEIAME_eb81d7d9.gravar_SMS("안녕하세요 " + entrada_VALOR.leitura_SMS());
        saídaTexto.gravar_linha("KOREAN SWING CLICK " + entrada_VALOR.leitura_SMS());
    }
    public static void main(String[] argumentos) {
        Evento_Fila.나중에실행(new 한글창시험());
    }
}
