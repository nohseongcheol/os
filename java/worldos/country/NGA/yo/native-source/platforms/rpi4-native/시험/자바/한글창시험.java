// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.wínńdò;
import 한국어.자체.wíjẹ́ẹ̀tì;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    wínńdò 화면;
    àkọlé KÀ_MÍ_eb81d7d9;
    SMS_àayè_wúnrẹ̀n 입력;
    public void ṣiṣẹ́_iṣẹ́() {
        검사.참인지(ìgbéṣẹ̀_ìtòléra.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new wínńdò("한국어 ibi_ìpamọ́ wínńdò", 400, 280);
        KÀ_MÍ_eb81d7d9 = wíjẹ́ẹ̀tì.sàmì_iye("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = wíjẹ́ẹ̀tì.SMS_àayè_wúnrẹ̀n("Orúkọ", 20, 65, 340, 30);
        화면.ròmọ́_ìdá_ìpìlẹ̀(KÀ_MÍ_eb81d7d9);
        화면.ròmọ́_ìdá_ìpìlẹ̀(입력);
        화면.ròmọ́_ìdá_ìpìlẹ̀(wíjẹ́ẹ̀tì.bọ́tìnnì("인사하기", 20, 110, 180, 32, this));
        화면.ṣàfihàn_wínńdò();
        출력.kọ_ìlà("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 ìgbéṣẹ̀) {
        검사.참인지(ìgbéṣẹ̀_ìtòléra.사건처리중인가(), "한국어 ìṣe 되부름");
        검사.참인지(ìgbéṣẹ̀.wá_atọ̀ka_àkóónú() == 1001 && ìgbéṣẹ̀.ìgbéṣẹ̀_orísun() instanceof bọ́tìnnì, "한국어 ìgbéṣẹ̀ 객체와 출처");
        검사.참인지(!((Object)ìgbéṣẹ̀.ìgbéṣẹ̀_orísun() instanceof javax.swing.JButton), "표준 단추와 독립된 ìgúnrégé_iye");
        검사.참인지(!((Object)ìgbéṣẹ̀ instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 ìgúnrégé_iye");
        KÀ_MÍ_eb81d7d9.kọ_SMS("안녕하세요 " + 입력.글읽기());
        출력.kọ_ìlà("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        ìgbéṣẹ̀_ìtòléra.나중에실행(new 한글창시험());
    }
}
