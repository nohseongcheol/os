// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ContohLukisan {
    public static void Jalan() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Melayu.Asli.화면.segi_empat_tepat(600, 400, 28, 20, 0x0000ff);
        Melayu.Asli.화면.segi_empat_tepat(600, 425, 28, 20, 0x00ff00);
        Melayu.Asli.화면.segi_empat_tepat(600, 450, 28, 20, 0xff0000);
        Melayu.Asli.출력.tulis_baris("JAVA 그래픽: RGB");
        Melayu.Asli.출력.tulis_baris("Enter");
        Melayu.Asli.화면.기다리기();
    }
}
