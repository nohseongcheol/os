// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class RajzPélda {
    public static void Futtatás() {
        // 640x480 화면 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        magyar.saját.화면.téglalap(600, 400, 28, 20, 0x0000ff);
        magyar.saját.화면.téglalap(600, 425, 28, 20, 0x00ff00);
        magyar.saját.화면.téglalap(600, 450, 28, 20, 0xff0000);
        magyar.saját.Kimenet.ír_sor("JAVA 그래픽: RGB");
        magyar.saját.Kimenet.ír_sor("Enter");
        magyar.saját.화면.기다리기();
    }
}
