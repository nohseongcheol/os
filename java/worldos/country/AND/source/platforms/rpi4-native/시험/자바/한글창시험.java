// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.Finestra;
import Català.propi.giny;
import Català.propi.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Finestra 화면;
    Etiqueta LLEGIU_ME_eb81d7d9;
    SMS_camp 입력;
    public void Executa() {
        검사.참인지(incidència_cua.사건처리중인가(), "Català 화면 작업 큐");
        화면 = new Finestra("Català biblioteca Finestra", 400, 280);
        LLEGIU_ME_eb81d7d9 = giny.marcar_VALOR("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = giny.SMS_camp("Nom", 20, 65, 340, 30);
        화면.afegir_element(LLEGIU_ME_eb81d7d9);
        화면.afegir_element(입력);
        화면.afegir_element(giny.Botó("인사하기", 20, 110, 180, 32, this));
        화면.mostrar_finestra();
        Sortida.escriure_línia("KOREAN SWING READY");
    }
    public void rebre_acció(동작알림 Esdeveniment) {
        검사.참인지(incidència_cua.사건처리중인가(), "Català Acció 되부름");
        검사.참인지(Esdeveniment.INDEX() == 1001 && Esdeveniment.incidència_font() instanceof Botó, "Català Esdeveniment 객체와 출처");
        검사.참인지(!((Object)Esdeveniment.incidència_font() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALOR");
        검사.참인지(!((Object)Esdeveniment instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALOR");
        LLEGIU_ME_eb81d7d9.escriure_SMS("안녕하세요 " + 입력.tancar_SMS());
        Sortida.escriure_línia("KOREAN SWING CLICK " + 입력.tancar_SMS());
    }
    public static void main(String[] 인수) {
        incidència_cua.나중에실행(new 한글창시험());
    }
}
