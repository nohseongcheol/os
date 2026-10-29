// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ÇizimÖrneği {
    public static void çalıştır() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Türkçe.Öz.화면.dikdörtgen(600, 400, 28, 20, 0x0000ff);
        Türkçe.Öz.화면.dikdörtgen(600, 425, 28, 20, 0x00ff00);
        Türkçe.Öz.화면.dikdörtgen(600, 450, 28, 20, 0xff0000);
        Türkçe.Öz.metinÇıktısı.yazma_hat("JAVA 그래픽: RGB");
        Türkçe.Öz.metinÇıktısı.yazma_hat("Enter");
        Türkçe.Öz.화면.기다리기();
    }
}
