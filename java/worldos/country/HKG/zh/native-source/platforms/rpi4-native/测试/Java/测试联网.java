// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 中文.内置.字符;
import 中文.内置.通信;
public class 测试联网 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 前端值 = 通信.打开(9431), 后端值 = 通信.打开(9432);
        try {
            通信.发送(前端值, 9432, "Java UDP 한글😀"); System.out.println(通信.接收(后端值));
            byte[] 源代码 = 字符.编码("회신"); 前端值.send(new DatagramPacket(源代码, 源代码.length, InetAddress.getByName("localhost"), 9432));
            byte[] 已接收值 = new byte[32]; DatagramPacket 数据报 = new DatagramPacket(已接收值, 已接收值.length); 后端值.receive(数据报);
            System.out.println(数据报.getLength()); System.out.println(数据报.getPort()); System.out.println(数据报.getAddress().getHostAddress());
            System.out.println(后端值.getLocalPort());
            后端值.setSoTimeout(10);
            try { 后端值.receive(数据报); } catch (SocketTimeoutException e) { System.out.println("接收值 时间值 초과"); }
            后端值.close();
            try { 后端值.receive(数据报); } catch (java.io.IOException e) { System.out.println("닫힌 通信"); }
        } finally { 前端值.close(); 后端值.close(); }
    }
}
