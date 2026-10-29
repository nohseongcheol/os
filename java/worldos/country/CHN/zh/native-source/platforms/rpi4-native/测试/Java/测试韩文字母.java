// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.内置.字符;
import 中文.内置.文件;
import 中文.内置.条目列表;
import 中文.内置.字典;
import 中文.内置.输出;
public class 测试韩文字母 {
    public static void main(String[] a) throws Exception {
        String 问候例 = "안녕하세요 · 日本語 · العربية · 😀";
        输出.写入行(字符.解密数据(字符.编码(问候例))); 输出.写入编号(字符.代码分个数("한글😀"));
        文件.写入("한글자료.txt", 问候例); 输出.写入行(文件.读取("한글자료.txt"));
        条目列表 名称列列表 = new 条目列表(); 名称列列表.添加值列("가람"); 名称列列表.添加值列("누리"); 输出.写入行(名称列列表.读取(1));
        字典 含义值 = new 字典(); 含义值.放入值("가람", "강"); System.gc(); 输出.写入行(含义值.查找条目("가람"));
        try { 字符.解密数据(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { 输出.写入行("UTF-8 错误 拒绝值"); }
        输出.写入行("中文 库 是否完成");
    }
}
