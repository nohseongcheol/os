// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자체.Xanela;
import Galego.자체.Etiqueta;
import Galego.자체.SMS_campo;
import Galego.자체.botón;
import Galego.자체.evento_cola;
import Galego.자체.Saída;
import Galego.자체.실행할일;
import Galego.자체.동작받이;
import Galego.자체.동작알림;

/** 자체 커널의 Swing Xanela: gl 입력 → botón → Léame_eb81d7d9 Texto actualizar. */
public class 창예제 implements 실행할일, 동작받이 {
    private Xanela 인사창;
    private SMS_campo nome_campo;
    private Etiqueta 인사말;
    private int 인사횟수;

    public void abrir_ventá() {
        인사창 = new Xanela("gl Swing", 460, 300);
        인사창.engadir_elemento(new Etiqueta("gl", 20, 20, 420, 28));
        nome_campo = new SMS_campo("gl", 20, 64, 420, 30);
        인사말 = new Etiqueta("gl", 20, 152, 420, 28);
        인사창.engadir_elemento(nome_campo);
        인사창.engadir_elemento(new botón("인사하기", 20, 108, 180, 32, this));
        인사창.engadir_elemento(인사말);
        인사창.engadir_elemento(new Etiqueta("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.mostrar_ventá();
        Saída.escribir_liña("GUI 예제 준비: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.escribir_SMS("gl, " + nome_campo.글읽기() + "님! (" + 인사횟수 + ")");
        Saída.escribir_liña("GUI 인사: " + 인사말.글읽기());
    }

    public void Executar() { abrir_ventá(); }
    public void 동작받기(동작알림 알림) {
        Saída.escribir_liña("Acción 알림: " + 알림.comando_SMS());
        인사하기();
    }
    public static void Executar_2() {
        evento_cola.나중에실행(new 창예제());
    }
}
