// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 韩文字母源代码 {
    public static void main(String[] 实参) throws 中文.内置.输入输出异常 {
        中文.内置.输出.写入行("内置 컴파일러와 中文 库");
        int 字符个数 = 中文.内置.字符.代码分个数("한글😀");
        中文.内置.输出.写入编号(字符个数);
        中文.内置.文件.写入("한글자료.txt", "内置 内核值 안에서 저장한 한글😀");
        中文.内置.输出.写入行(中文.内置.文件.读取("한글자료.txt"));
    }
}
