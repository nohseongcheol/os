// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Ritexempel {
    public static void Kör() {
        // 640x480 skärmbild 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Svenska.eget.skärmbild.rektangel(600, 400, 28, 20, 0x0000ff);
        Svenska.eget.skärmbild.rektangel(600, 425, 28, 20, 0x00ff00);
        Svenska.eget.skärmbild.rektangel(600, 450, 28, 20, 0xff0000);
        Svenska.eget.utmatningsposition.skriva_rad("JAVA 그래픽: RGB");
        Svenska.eget.utmatningsposition.skriva_rad("Enter");
        Svenska.eget.skärmbild.기다리기();
    }
}
