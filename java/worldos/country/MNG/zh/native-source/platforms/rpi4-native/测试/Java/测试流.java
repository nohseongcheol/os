// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 测试流 {
    public static void main(String[] args) throws Exception {
        ServerSocket 服务器值 = new ServerSocket(9250);
        Socket 客户机值 = new Socket("localhost", 9250);
        Socket 连接 = 服务器值.accept();
        if (连接.getPort() != 客户机值.getLocalPort() || 客户机值.getPort() != 连接.getLocalPort()) throw new RuntimeException("端口值 불일치");
        byte[] 数据报 = "한글 流值".getBytes("UTF-8");
        客户机值.getOutputStream().write(数据报);
        byte[] 已接收项目 = new byte[100];
        int 长度 = 连接.getInputStream().read(已接收项目, 0, 已接收项目.length);
        System.out.println(长度 == 数据报.length);
        for (int i = 0; i < 长度; i++) if (已接收项目[i] != 数据报[i]) throw new RuntimeException("内容值 불일치");
        连接.getOutputStream().write(42);
        System.out.println(客户机值.getInputStream().read());
        客户机值.close();
        System.out.println(连接.getInputStream().read());
        连接.close(); 服务器值.close();
        ServerSocket 空服务器 = new ServerSocket(9250);
        空服务器.setSoTimeout(10);
        try { 空服务器.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("时间值 限制值"); }
        空服务器.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 是否不支持"); }
        System.out.println("STREAM PASS");
    }
}
