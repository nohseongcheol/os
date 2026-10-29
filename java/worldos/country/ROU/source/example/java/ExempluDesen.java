// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ExempluDesen {
    public static void Pornește() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Română.propriu.화면.dreptunghi(600, 400, 28, 20, 0x0000ff);
        Română.propriu.화면.dreptunghi(600, 425, 28, 20, 0x00ff00);
        Română.propriu.화면.dreptunghi(600, 450, 28, 20, 0xff0000);
        Română.propriu.Rezultat.scriere_linie("JAVA 그래픽: RGB");
        Română.propriu.Rezultat.scriere_linie("Enter");
        Română.propriu.화면.기다리기();
    }
}
