// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 颜色 {
    public static void main(String[] 实参) throws Exception {
        int 总和值 = 0;
        int 数 = 1;
        while (数 <= 10) {
            总和值 = 总和值 + 数;
            数 = 数 + 1;
        }
        中文.内置.输出.写入编号(总和值);
        中文.内置.文件.写入("aot.txt", "한글 AOT 文件 😀");
        中文.内置.输出.写入行(中文.内置.文件.读取("aot.txt"));
    }
}
