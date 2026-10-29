// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.pəncərə;
import 한국어.자체.vidget;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    pəncərə 화면;
    Etiket OXUMƏNİ_eb81d7d9;
    SMS_sahə 입력;
    public void icra_etmək_tapşırıq() {
        검사.참인지(hadisə_növbə.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new pəncərə("한국어 kitabxana pəncərə", 400, 280);
        OXUMƏNİ_eb81d7d9 = vidget.teq_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = vidget.SMS_sahə("Ad", 20, 65, 340, 30);
        화면.əlavə_etmək_element(OXUMƏNİ_eb81d7d9);
        화면.əlavə_etmək_element(입력);
        화면.əlavə_etmək_element(vidget.düymə("인사하기", 20, 110, 180, 32, this));
        화면.göstərmək_pəncərə();
        출력.yazmaq_xətt("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 hadisə) {
        검사.참인지(hadisə_növbə.사건처리중인가(), "한국어 Gedişat 되부름");
        검사.참인지(hadisə.INDEX() == 1001 && hadisə.hadisə_mənbə() instanceof düymə, "한국어 hadisə 객체와 출처");
        검사.참인지(!((Object)hadisə.hadisə_mənbə() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)hadisə instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        OXUMƏNİ_eb81d7d9.yazmaq_SMS("안녕하세요 " + 입력.글읽기());
        출력.yazmaq_xətt("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        hadisə_növbə.나중에실행(new 한글창시험());
    }
}
