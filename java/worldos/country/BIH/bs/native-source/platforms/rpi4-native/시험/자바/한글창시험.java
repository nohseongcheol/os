// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.prozor;
import 한국어.자체.vidžet;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    prozor 화면;
    Oznaka Pročitaj_me_eb81d7d9;
    SMS_polje 입력;
    public void Izvrši() {
        검사.참인지(događaj_redoslijed.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new prozor("한국어 biblioteka prozor", 400, 280);
        Pročitaj_me_eb81d7d9 = vidžet.oznaka_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = vidžet.SMS_polje("Naziv", 20, 65, 340, 30);
        화면.dodati_element(Pročitaj_me_eb81d7d9);
        화면.dodati_element(입력);
        화면.dodati_element(vidžet.dugme("인사하기", 20, 110, 180, 32, this));
        화면.program_prozor();
        Ispis.pisati_redak("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 događaj) {
        검사.참인지(događaj_redoslijed.사건처리중인가(), "한국어 radnja 되부름");
        검사.참인지(događaj.INDEX() == 1001 && događaj.događaj_izvor() instanceof dugme, "한국어 događaj 객체와 출처");
        검사.참인지(!((Object)događaj.događaj_izvor() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)događaj instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        Pročitaj_me_eb81d7d9.pisati_SMS("안녕하세요 " + 입력.글읽기());
        Ispis.pisati_redak("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumenti) {
        događaj_redoslijed.나중에실행(new 한글창시험());
    }
}
