// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 中文.内置.连接通道;
import 中文.内置.运行参数;
import 中文.内置.数据报信道;
import 中文.内置.字符;
import 中文.内置.输出;
import 中文.内置.检查项;
import 中文.内置.输入流;
import 中文.内置.输入输出异常;

public class 网络例 {
    public static void 运行() throws 输入输出异常 {
        // 宿主机: python3 工具集/示例回显.py --tcp-port 9000 --udp-port 9001
        连接通道 连接 = 连接通道.打开("10.0.2.2", 字符.解析整数(运行参数.文本(0)));
        try {
            连接.超时(700);
            byte[] 消息 = 字符.编码("JAVA TCP Chinese\n");
            连接.输出().写入(消息);
            输入流 输入值 = 连接.输入值();
            for (int 数 = 0; 数 < 字符.字节个数(消息); 数++) {
                检查项.确认真值(输入值.读取() == (消息[数] & 255), "TCP 回复 불일치");
            }
        } finally { 连接.关闭(); }
        数据报信道 端点 = 数据报信道.打开(0);
        try {
            端点.超时(700);
            端点.发送("10.0.2.2", 字符.解析整数(运行参数.文本(1)), "JAVA UDP Chinese");
            检查项.确认真值(字符.相等文本(端点.接收(), "JAVA UDP Chinese"), "UDP 回复 불일치");
        } finally { 端点.关闭(); }
        输出.写入行("JAVA 네트워크 验证: TCP UDP Chinese");
    }
}
