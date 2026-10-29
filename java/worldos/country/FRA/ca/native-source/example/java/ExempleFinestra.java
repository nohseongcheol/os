// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.Finestra;
import Català.propi.Etiqueta;
import Català.propi.SMS_camp;
import Català.propi.Botó;
import Català.propi.incidència_cua;
import Català.propi.Sortida;
import Català.propi.실행할일;
import Català.propi.동작받이;
import Català.propi.동작알림;

/** propi 커널의 Swing Finestra: ca 입력 → Botó → LLEGIU_ME_eb81d7d9 SMS actualitzar. */
public class ExempleFinestra implements 실행할일, 동작받이 {
    private Finestra 인사창;
    private SMS_camp nom_camp;
    private Etiqueta 인사말;
    private int 인사횟수;

    public void crear_finestra() {
        인사창 = new Finestra("ca Swing", 460, 300);
        인사창.afegir_element(new Etiqueta("ca", 20, 20, 420, 28));
        nom_camp = new SMS_camp("ca", 20, 64, 420, 30);
        인사말 = new Etiqueta("ca", 20, 152, 420, 28);
        인사창.afegir_element(nom_camp);
        인사창.afegir_element(new Botó("인사하기", 20, 108, 180, 32, this));
        인사창.afegir_element(인사말);
        인사창.afegir_element(new Etiqueta("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.mostrar_finestra();
        Sortida.escriure_línia("GUI 예제 Prepara: ExempleFinestra");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.escriure_SMS("ca, " + nom_camp.tancar_SMS() + "님! (" + 인사횟수 + ")");
        Sortida.escriure_línia("GUI 인사: " + 인사말.tancar_SMS());
    }

    public void Executa() { crear_finestra(); }
    public void rebre_acció(동작알림 알림) {
        Sortida.escriure_línia("Acció 알림: " + 알림.ordre_SMS());
        인사하기();
    }
    public static void Executa_2() {
        incidència_cua.나중에실행(new ExempleFinestra());
    }
}
