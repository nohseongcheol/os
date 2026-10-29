// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class VíDụVẽ {
    public static void chạy() {
        // Vẽ hình chữ nhật đỏ, xanh lá và xanh dương bên phải màn hình 640x480.
        tiếngViệt.tựThân.MànHình.hìnhChữNhật(600, 400, 28, 20, 0x0000ff);
        tiếngViệt.tựThân.MànHình.hìnhChữNhật(600, 425, 28, 20, 0x00ff00);
        tiếngViệt.tựThân.MànHình.hìnhChữNhật(600, 450, 28, 20, 0xff0000);
        tiếngViệt.tựThân.ĐầuRa.ghiDòng("JAVA 그래픽: RGB");
        tiếngViệt.tựThân.ĐầuRa.ghiDòng("Enter");
        tiếngViệt.tựThân.MànHình.đợi();
    }
}
