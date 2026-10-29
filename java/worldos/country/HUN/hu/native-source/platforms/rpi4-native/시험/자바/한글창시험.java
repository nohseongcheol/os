// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.saját.Ablak;
import magyar.saját.widget;
import magyar.saját.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Ablak 화면;
    Címke fontos_fájl_eb81d7d9;
    szövegmező bevitel_ÉRTÉK;
    public void Végrehajtás() {
        검사.참인지(esemény_várólista.사건처리중인가(), "magyar 화면 작업 큐");
        화면 = new Ablak("magyar kódtár Ablak", 400, 280);
        fontos_fájl_eb81d7d9 = widget.címke_ÉRTÉK("한글로 Java 코딩", 20, 20, 340, 30);
        bevitel_ÉRTÉK = widget.szövegmező("Név", 20, 65, 340, 30);
        화면.hozzáad_elem(fontos_fájl_eb81d7d9);
        화면.hozzáad_elem(bevitel_ÉRTÉK);
        화면.hozzáad_elem(widget.gomb("인사하기", 20, 110, 180, 32, this));
        화면.bemutató_ablak();
        Kimenet.ír_sor("KOREAN SWING READY");
    }
    public void fogad_Action(Action_alapelv Esemény) {
        검사.참인지(esemény_várólista.사건처리중인가(), "magyar Művelet 되부름");
        검사.참인지(Esemény.INDEX() == 1001 && Esemény.eseményforrás() instanceof gomb, "magyar Esemény 객체와 eredet_ÉRTÉK");
        검사.참인지(!((Object)Esemény.eseményforrás() instanceof javax.swing.JButton), "표준 단추와 독립된 formáz_ÉRTÉK");
        검사.참인지(!((Object)Esemény instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formáz_ÉRTÉK");
        fontos_fájl_eb81d7d9.ír_SMS("안녕하세요 " + bevitel_ÉRTÉK.글읽기());
        Kimenet.ír_sor("KOREAN SWING CLICK " + bevitel_ÉRTÉK.글읽기());
    }
    public static void main(String[] Argumentumok) {
        esemény_várólista.나중에실행(new 한글창시험());
    }
}
