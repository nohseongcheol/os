// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 文件例 {
    public static void 运行() throws 中文.内置.输入输出异常 {
        中文.内置.文件.写入("java.txt", "JAVA 文件: Chinese 😀\n");
        中文.内置.输出.写入(中文.内置.文件.读取("java.txt"));
    }
}
