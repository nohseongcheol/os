// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class PrimjerCrtanja {
    public static void Pokreni() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        hrvatski.vlastiti.화면.pravokutnik(600, 400, 28, 20, 0x0000ff);
        hrvatski.vlastiti.화면.pravokutnik(600, 425, 28, 20, 0x00ff00);
        hrvatski.vlastiti.화면.pravokutnik(600, 450, 28, 20, 0xff0000);
        hrvatski.vlastiti.Izlaz.zapisivanje_red("JAVA 그래픽: RGB");
        hrvatski.vlastiti.Izlaz.zapisivanje_red("Enter");
        hrvatski.vlastiti.화면.기다리기();
    }
}
