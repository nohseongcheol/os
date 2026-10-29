// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 測試流 {
    public static void main(String[] args) throws Exception {
        ServerSocket 服務器值 = new ServerSocket(9250);
        Socket 客戶機值 = new Socket("localhost", 9250);
        Socket 連接 = 服務器值.accept();
        if (連接.getPort() != 客戶機值.getLocalPort() || 客戶機值.getPort() != 連接.getLocalPort()) throw new RuntimeException("埠值 불일치");
        byte[] 數據報 = "한글 流值".getBytes("UTF-8");
        客戶機值.getOutputStream().write(數據報);
        byte[] 已接收項目 = new byte[100];
        int 長度 = 連接.getInputStream().read(已接收項目, 0, 已接收項目.length);
        System.out.println(長度 == 數據報.length);
        for (int i = 0; i < 長度; i++) if (已接收項目[i] != 數據報[i]) throw new RuntimeException("內容值 불일치");
        連接.getOutputStream().write(42);
        System.out.println(客戶機值.getInputStream().read());
        客戶機值.close();
        System.out.println(連接.getInputStream().read());
        連接.close(); 服務器值.close();
        ServerSocket 空服務器 = new ServerSocket(9250);
        空服務器.setSoTimeout(10);
        try { 空服務器.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("時間值 限制值"); }
        空服務器.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 是否不支持"); }
        System.out.println("STREAM PASS");
    }
}
