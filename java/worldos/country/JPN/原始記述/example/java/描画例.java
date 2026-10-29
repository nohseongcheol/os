// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 描画例 {
    public static void 起動処理() {
        // 640×480画面の右側に赤・緑・青の長方形を描く。
        日本語.内蔵.画面.矩形(600, 400, 28, 20, 0x0000ff);
        日本語.内蔵.画面.矩形(600, 425, 28, 20, 0x00ff00);
        日本語.内蔵.画面.矩形(600, 450, 28, 20, 0xff0000);
        日本語.内蔵.出力.行書込("JAVA 그래픽: RGB");
        日本語.内蔵.出力.行書込("Enter");
        日本語.内蔵.画面.待機();
    }
}
