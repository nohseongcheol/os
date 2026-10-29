// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 中文.內建.字元;
import 中文.內建.通信;
public class 測試聯網 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 前端值 = 通信.打開(9431), 後端值 = 通信.打開(9432);
        try {
            通信.發送(前端值, 9432, "Java UDP 한글😀"); System.out.println(通信.接收(後端值));
            byte[] 原始碼 = 字元.編碼("회신"); 前端值.send(new DatagramPacket(原始碼, 原始碼.length, InetAddress.getByName("localhost"), 9432));
            byte[] 已接收值 = new byte[32]; DatagramPacket 數據報 = new DatagramPacket(已接收值, 已接收值.length); 後端值.receive(數據報);
            System.out.println(數據報.getLength()); System.out.println(數據報.getPort()); System.out.println(數據報.getAddress().getHostAddress());
            System.out.println(後端值.getLocalPort());
            後端值.setSoTimeout(10);
            try { 後端值.receive(數據報); } catch (SocketTimeoutException e) { System.out.println("接收值 時間值 초과"); }
            後端值.close();
            try { 後端值.receive(數據報); } catch (java.io.IOException e) { System.out.println("닫힌 通信"); }
        } finally { 前端值.close(); 後端值.close(); }
    }
}
