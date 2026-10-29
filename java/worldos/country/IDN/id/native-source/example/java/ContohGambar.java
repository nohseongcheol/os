// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ContohGambar {
    public static void jalankan() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Indonesia.Asli.화면.persegi(600, 400, 28, 20, 0x0000ff);
        Indonesia.Asli.화면.persegi(600, 425, 28, 20, 0x00ff00);
        Indonesia.Asli.화면.persegi(600, 450, 28, 20, 0xff0000);
        Indonesia.Asli.keluaranTeks.tulis_baris("JAVA 그래픽: RGB");
        Indonesia.Asli.keluaranTeks.tulis_baris("Enter");
        Indonesia.Asli.화면.기다리기();
    }
}
