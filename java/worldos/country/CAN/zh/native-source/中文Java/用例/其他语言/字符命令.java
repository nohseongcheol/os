// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.Java.字符;

/** 供其他语言通过标准输出读取结果的小型 Java 入口。 */
public final class 字符命令 {
    public static void main(String[] 实参) {
        if (实参.length != 1) {
            System.err.println("사용법: 字符命令 字符串");
            System.exit(2);
        }
        System.out.println(字符.代码分个数(实参[0]));
    }
}
