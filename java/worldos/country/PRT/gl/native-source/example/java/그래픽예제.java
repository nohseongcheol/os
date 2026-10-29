// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 그래픽예제 {
    public static void Executar_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Galego.자체.화면.사각형(600, 400, 28, 20, 0x0000ff);
        Galego.자체.화면.사각형(600, 425, 28, 20, 0x00ff00);
        Galego.자체.화면.사각형(600, 450, 28, 20, 0xff0000);
        Galego.자체.Saída.escribir_liña("JAVA 그래픽: RGB");
        Galego.자체.Saída.escribir_liña("Enter");
        Galego.자체.화면.기다리기();
    }
}
