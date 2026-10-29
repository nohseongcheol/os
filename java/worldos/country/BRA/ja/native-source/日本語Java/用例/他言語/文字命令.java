// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 日本語.Java.文字;

/** 他言語が標準出力から結果を受け取れる小さな Java の入口。 */
public final class 文字命令 {
    public static void main(String[] 引数) {
        if (引数.length != 1) {
            System.err.println("사용법: 文字命令 文字列");
            System.exit(2);
        }
        System.out.println(文字.コード点個数(引数[0]));
    }
}
