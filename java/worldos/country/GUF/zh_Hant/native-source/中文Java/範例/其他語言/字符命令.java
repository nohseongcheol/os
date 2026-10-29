// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.Java.字元;

/** 供其他語言透過標準輸出讀取結果的小型 Java 進入點。 */
public final class 字符命令 {
    public static void main(String[] 實參) {
        if (實參.length != 1) {
            System.err.println("사용법: 字符命令 字符串");
            System.exit(2);
        }
        System.out.println(字元.程式碼分個數(實參[0]));
    }
}
