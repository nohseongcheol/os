// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Melayu.Asli.Tetingkap;
import Melayu.Asli.unsur_skrin;
import Melayu.Asli.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Tetingkap 화면;
    label README_eb81d7d9;
    medan_teks 입력;
    public void Lakukan() {
        검사.참인지(acara_baris.사건처리중인가(), "Melayu 화면 작업 큐");
        화면 = new Tetingkap("Melayu pustaka Tetingkap", 400, 280);
        README_eb81d7d9 = unsur_skrin.tag_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = unsur_skrin.medan_teks("Nama", 20, 65, 340, 30);
        화면.tambah_unsur(README_eb81d7d9);
        화면.tambah_unsur(입력);
        화면.tambah_unsur(unsur_skrin.Butang("인사하기", 20, 110, 180, 32, this));
        화면.tayang_tetingkap();
        출력.tulis_baris("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Peristiwa) {
        검사.참인지(acara_baris.사건처리중인가(), "Melayu Aksi 되부름");
        검사.참인지(Peristiwa.INDEX() == 1001 && Peristiwa.sumber_peristiwa() instanceof Butang, "Melayu Peristiwa 객체와 출처");
        검사.참인지(!((Object)Peristiwa.sumber_peristiwa() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)Peristiwa instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        README_eb81d7d9.tulis_SMS("안녕하세요 " + 입력.글읽기());
        출력.tulis_baris("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        acara_baris.나중에실행(new 한글창시험());
    }
}
