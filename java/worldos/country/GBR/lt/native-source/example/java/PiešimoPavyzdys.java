// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class PiešimoPavyzdys {
    public static void Paleisti() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Lietuvių.savas.화면.stačiakampis(600, 400, 28, 20, 0x0000ff);
        Lietuvių.savas.화면.stačiakampis(600, 425, 28, 20, 0x00ff00);
        Lietuvių.savas.화면.stačiakampis(600, 450, 28, 20, 0xff0000);
        Lietuvių.savas.Išvestis.rašymas_eilutė("JAVA 그래픽: RGB");
        Lietuvių.savas.Išvestis.rašymas_eilutė("Enter");
        Lietuvių.savas.화면.기다리기();
    }
}
