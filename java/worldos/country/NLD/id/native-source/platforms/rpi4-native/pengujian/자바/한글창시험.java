// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Indonesia.Asli.Jendela;
import Indonesia.Asli.unsur_layar;
import Indonesia.Asli.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Jendela 화면;
    Nama baca_saya_eb81d7d9;
    bidang_teks 입력;
    public void Eksekusi() {
        검사.참인지(acara_antrean.사건처리중인가(), "Indonesia 화면 작업 큐");
        화면 = new Jendela("Indonesia pustaka Jendela", 400, 280);
        baca_saya_eb81d7d9 = unsur_layar.tag_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = unsur_layar.bidang_teks("Nama_2", 20, 65, 340, 30);
        화면.tambah_elemen(baca_saya_eb81d7d9);
        화면.tambah_elemen(입력);
        화면.tambah_elemen(unsur_layar.tombol("인사하기", 20, 110, 180, 32, this));
        화면.show_jendela();
        keluaranTeks.tulis_baris("KOREAN SWING READY");
    }
    public void terima_Tugas(동작알림 Even) {
        검사.참인지(acara_antrean.사건처리중인가(), "Indonesia Aksi 되부름");
        검사.참인지(Even.INDEX() == 1001 && Even.sumber_kejadian() instanceof tombol, "Indonesia Even 객체와 출처");
        검사.참인지(!((Object)Even.sumber_kejadian() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)Even instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        baca_saya_eb81d7d9.tulis_SMS("안녕하세요 " + 입력.글읽기());
        keluaranTeks.tulis_baris("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] argumen) {
        acara_antrean.나중에실행(new 한글창시험());
    }
}
