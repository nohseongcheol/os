// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class UkázkaKreslení {
    public static void Spustit_2() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        čeština.vlastní.화면.obdélník(600, 400, 28, 20, 0x0000ff);
        čeština.vlastní.화면.obdélník(600, 425, 28, 20, 0x00ff00);
        čeština.vlastní.화면.obdélník(600, 450, 28, 20, 0xff0000);
        čeština.vlastní.výstupní_pozice.zápis_čára("JAVA 그래픽: RGB");
        čeština.vlastní.výstupní_pozice.zápis_čára("Enter");
        čeština.vlastní.화면.기다리기();
    }
}
