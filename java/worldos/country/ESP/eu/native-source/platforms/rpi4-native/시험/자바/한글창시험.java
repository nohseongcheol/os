// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자체.Leihoa;
import Euskara.자체.widget;
import Euskara.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Leihoa 화면;
    Etiketa IRAKHAU_eb81d7d9;
    SMS_eremu 입력;
    public void Exekutatu() {
        검사.참인지(gertaera_ilara.사건처리중인가(), "Euskara 화면 작업 큐");
        화면 = new Leihoa("Euskara liburutegi Leihoa", 400, 280);
        IRAKHAU_eb81d7d9 = widget.etiketa_balio("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.SMS_eremu("Izena", 20, 65, 340, 30);
        화면.gehitu_elementu(IRAKHAU_eb81d7d9);
        화면.gehitu_elementu(입력);
        화면.gehitu_elementu(widget.botoia("인사하기", 20, 110, 180, 32, this));
        화면.erakutsi_leiho();
        Irteera.idatzi_lerro("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Gertaera) {
        검사.참인지(gertaera_ilara.사건처리중인가(), "Euskara Ekintza 되부름");
        검사.참인지(Gertaera.INDIZE() == 1001 && Gertaera.gertaera_iturburu() instanceof botoia, "Euskara Gertaera 객체와 출처");
        검사.참인지(!((Object)Gertaera.gertaera_iturburu() instanceof javax.swing.JButton), "표준 단추와 독립된 formatu_balio");
        검사.참인지(!((Object)Gertaera instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formatu_balio");
        IRAKHAU_eb81d7d9.idatzi_SMS("안녕하세요 " + 입력.글읽기());
        Irteera.idatzi_lerro("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumentuak) {
        gertaera_ilara.나중에실행(new 한글창시험());
    }
}
