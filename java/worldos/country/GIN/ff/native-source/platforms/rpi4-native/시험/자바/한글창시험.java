// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.falanteere;
import 한국어.자체.화면요소;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    falanteere 화면;
    tinndinoore TARƊOO_eb81d7d9;
    binndi_suudu 입력;
    public void 실행하기() {
        검사.참인지(saɗteende_lappol.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new falanteere("한국어 defterdu falanteere", 400, 280);
        TARƊOO_eb81d7d9 = 화면요소.hebtinirde_njaru("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = 화면요소.binndi_suudu("innde", 20, 65, 340, 30);
        화면.ɓeydude_geɗel(TARƊOO_eb81d7d9);
        화면.ɓeydude_geɗel(입력);
        화면.ɓeydude_geɗel(화면요소.feɗoode("인사하기", 20, 110, 180, 32, this));
        화면.hollirde_falanteere();
        출력.winndude_diidol("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 saɗteende) {
        검사.참인지(saɗteende_lappol.사건처리중인가(), "한국어 gollal 되부름");
        검사.참인지(saɗteende.joopirdu() == 1001 && saɗteende.saɗteende_sewnde() instanceof feɗoode, "한국어 saɗteende 객체와 출처");
        검사.참인지(!((Object)saɗteende.saɗteende_sewnde() instanceof javax.swing.JButton), "표준 단추와 독립된 formaa_njaru");
        검사.참인지(!((Object)saɗteende instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formaa_njaru");
        TARƊOO_eb81d7d9.winndude_binndi("안녕하세요 " + 입력.글읽기());
        출력.winndude_diidol("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        saɗteende_lappol.나중에실행(new 한글창시험());
    }
}
