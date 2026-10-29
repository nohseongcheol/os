// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 日本語.内蔵.文字;
import 日本語.内蔵.通信;
public class 通信機構試験 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 前面値 = 通信.開放(9431), 後端値 = 通信.開放(9432);
        try {
            通信.送信(前面値, 9432, "Java UDP 한글😀"); System.out.println(通信.受取(後端値));
            byte[] ソース = 文字.符号化("회신"); 前面値.send(new DatagramPacket(ソース, ソース.length, InetAddress.getByName("localhost"), 9432));
            byte[] 受信済み値 = new byte[32]; DatagramPacket データグラム = new DatagramPacket(受信済み値, 受信済み値.length); 後端値.receive(データグラム);
            System.out.println(データグラム.getLength()); System.out.println(データグラム.getPort()); System.out.println(データグラム.getAddress().getHostAddress());
            System.out.println(後端値.getLocalPort());
            後端値.setSoTimeout(10);
            try { 後端値.receive(データグラム); } catch (SocketTimeoutException e) { System.out.println("値受取 時間値 초과"); }
            後端値.close();
            try { 後端値.receive(データグラム); } catch (java.io.IOException e) { System.out.println("닫힌 通信"); }
        } finally { 前面値.close(); 後端値.close(); }
    }
}
