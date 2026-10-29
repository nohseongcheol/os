// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.analaaya;
import 한국어.자체.화면요소;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    analaaya 화면;
    akanüliajaa PAASHAJE_ERAN_eb81d7d9;
    입력칸 입력;
    public void 실행하기() {
        검사.참인지(kasachiki_a_atapajüsüirua.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new analaaya("한국어 anaajaalee analaaya", 400, 280);
        PAASHAJE_ERAN_eb81d7d9 = 화면요소.akanüliajia_ajutuu("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = 화면요소.입력칸("이름", 20, 65, 340, 30);
        화면.담기(PAASHAJE_ERAN_eb81d7d9);
        화면.담기(입력);
        화면.담기(화면요소.ajüttülee("인사하기", 20, 110, 180, 32, this));
        화면.보이기();
        출력.ashajaa_liinia("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 kasachiki) {
        검사.참인지(kasachiki_a_atapajüsüirua.사건처리중인가(), "한국어 aa_inra_awai 되부름");
        검사.참인지(kasachiki.ee_iyatialujuna() == 1001 && kasachiki.kasachiki_eejeejetülein() instanceof ajüttülee, "한국어 kasachiki 객체와 출처");
        검사.참인지(!((Object)kasachiki.kasachiki_eejeejetülein() instanceof javax.swing.JButton), "표준 단추와 독립된 akua_ipaa_ajutuu");
        검사.참인지(!((Object)kasachiki instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 akua_ipaa_ajutuu");
        PAASHAJE_ERAN_eb81d7d9.글쓰기("안녕하세요 " + 입력.글읽기());
        출력.ashajaa_liinia("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        kasachiki_a_atapajüsüirua.나중에실행(new 한글창시험());
    }
}
