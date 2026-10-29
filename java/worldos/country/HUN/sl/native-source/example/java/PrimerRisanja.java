// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class PrimerRisanja {
    public static void Zaženi() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        slovenščina.lastno.화면.pravokotnik(600, 400, 28, 20, 0x0000ff);
        slovenščina.lastno.화면.pravokotnik(600, 425, 28, 20, 0x00ff00);
        slovenščina.lastno.화면.pravokotnik(600, 450, 28, 20, 0xff0000);
        slovenščina.lastno.Izpis.pisati_linija("JAVA 그래픽: RGB");
        slovenščina.lastno.Izpis.pisati_linija("Enter");
        slovenščina.lastno.화면.기다리기();
    }
}
