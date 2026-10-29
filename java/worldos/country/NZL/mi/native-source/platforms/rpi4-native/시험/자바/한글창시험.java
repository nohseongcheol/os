// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자체.matapihi;
import Reo_Māori.자체.taputapu;
import Reo_Māori.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    matapihi 화면;
    tapanga PĀNUIMAI_eb81d7d9;
    āpure_kuputuhi 입력;
    public void kawe_tūmahi() {
        검사.참인지(hui_tūtira.사건처리중인가(), "Reo_Māori 화면 작업 큐");
        화면 = new matapihi("Reo_Māori puna matapihi", 400, 280);
        PĀNUIMAI_eb81d7d9 = taputapu.tūtohu_uara("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = taputapu.āpure_kuputuhi("Ingoa", 20, 65, 340, 30);
        화면.tāpiri_huānga(PĀNUIMAI_eb81d7d9);
        화면.tāpiri_huānga(입력);
        화면.tāpiri_huānga(taputapu.pātene("인사하기", 20, 110, 180, 32, this));
        화면.whakaatu_matapihi();
        출력.tuhi_hononga("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 hui) {
        검사.참인지(hui_tūtira.사건처리중인가(), "Reo_Māori hohenga 되부름");
        검사.참인지(hui.INDEX() == 1001 && hui.hui_pūtake() instanceof pātene, "Reo_Māori hui 객체와 출처");
        검사.참인지(!((Object)hui.hui_pūtake() instanceof javax.swing.JButton), "표준 단추와 독립된 hōputu_uara");
        검사.참인지(!((Object)hui instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 hōputu_uara");
        PĀNUIMAI_eb81d7d9.tuhi_TEXT("안녕하세요 " + 입력.글읽기());
        출력.tuhi_hononga("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        hui_tūtira.나중에실행(new 한글창시험());
    }
}
