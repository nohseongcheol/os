// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.nativo.Janela;
import Português.nativo.Etiqueta;
import Português.nativo.campo_de_texto;
import Português.nativo.botão;
import Português.nativo.Evento_Fila;
import Português.nativo.saídaTexto;
import Português.nativo.실행할일;
import Português.nativo.동작받이;
import Português.nativo.Ação_aviso;

/** nativo 커널의 Swing Janela: Português entrada_VALOR → botão → LEIAME_eb81d7d9 texto renovar. */
public class ExemploJanela implements 실행할일, 동작받이 {
    private Janela saudação_janela;
    private campo_de_texto nome_Campo;
    private Etiqueta saudação;
    private int saudação_CONT_NÚM;

    public void abrir_janela() {
        saudação_janela = new Janela("Português Swing", 460, 300);
        saudação_janela.Adicionar_elemento(new Etiqueta("Olá", 20, 20, 420, 28));
        nome_Campo = new campo_de_texto("Português", 20, 64, 420, 30);
        saudação = new Etiqueta("Olá", 20, 152, 420, 28);
        saudação_janela.Adicionar_elemento(nome_Campo);
        saudação_janela.Adicionar_elemento(new botão("인사하기", 20, 108, 180, 32, this));
        saudação_janela.Adicionar_elemento(saudação);
        saudação_janela.Adicionar_elemento(new Etiqueta("F9 / Shift+Space | X", 20, 204, 420, 28));
        saudação_janela.mostrar_janela();
        saídaTexto.gravar_linha("GUI 예제 Preparar: ExemploJanela");
    }

    public void 인사하기() {
        saudação_CONT_NÚM++;
        saudação.gravar_SMS("Olá, " + nome_Campo.leitura_SMS() + "님! (" + saudação_CONT_NÚM + ")");
        saídaTexto.gravar_linha("GUI saudação_ae353e94: " + saudação.leitura_SMS());
    }

    public void Executar() { abrir_janela(); }
    public void receber_Ação(Ação_aviso aviso) {
        saídaTexto.gravar_linha("Acção aviso: " + aviso.comando_SMS());
        인사하기();
    }
    public static void iniciar() {
        Evento_Fila.나중에실행(new ExemploJanela());
    }
}
