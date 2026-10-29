// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Tekenvoorbeeld {
    public static void starten() {
        // 640x480 scherm 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Nederlands.Eigen.scherm.rechthoek(600, 400, 28, 20, 0x0000ff);
        Nederlands.Eigen.scherm.rechthoek(600, 425, 28, 20, 0x00ff00);
        Nederlands.Eigen.scherm.rechthoek(600, 450, 28, 20, 0xff0000);
        Nederlands.Eigen.tekstuitvoer.schrijven_lijn("JAVA 그래픽: RGB");
        Nederlands.Eigen.tekstuitvoer.schrijven_lijn("Enter");
        Nederlands.Eigen.scherm.기다리기();
    }
}
