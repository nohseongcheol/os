// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자체.Xanela;
import Galego.자체.widget;
import Galego.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Xanela 화면;
    Etiqueta Léame_eb81d7d9;
    SMS_campo 입력;
    public void Executar() {
        검사.참인지(evento_cola.사건처리중인가(), "Galego 화면 작업 큐");
        화면 = new Xanela("Galego biblioteca Xanela", 400, 280);
        Léame_eb81d7d9 = widget.etiqueta_VALOR("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.SMS_campo("Nome", 20, 65, 340, 30);
        화면.engadir_elemento(Léame_eb81d7d9);
        화면.engadir_elemento(입력);
        화면.engadir_elemento(widget.botón("인사하기", 20, 110, 180, 32, this));
        화면.mostrar_ventá();
        Saída.escribir_liña("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Evento) {
        검사.참인지(evento_cola.사건처리중인가(), "Galego Acción 되부름");
        검사.참인지(Evento.ÍNDICE() == 1001 && Evento.evento_fonte() instanceof botón, "Galego Evento 객체와 출처");
        검사.참인지(!((Object)Evento.evento_fonte() instanceof javax.swing.JButton), "표준 단추와 독립된 formato_VALOR");
        검사.참인지(!((Object)Evento instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formato_VALOR");
        Léame_eb81d7d9.escribir_SMS("안녕하세요 " + 입력.글읽기());
        Saída.escribir_liña("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumentos) {
        evento_cola.나중에실행(new 한글창시험());
    }
}
