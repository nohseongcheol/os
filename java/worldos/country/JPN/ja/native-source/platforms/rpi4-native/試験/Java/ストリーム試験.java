// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class ストリーム試験 {
    public static void main(String[] args) throws Exception {
        ServerSocket サーバー値 = new ServerSocket(9250);
        Socket ゲスト値 = new Socket("localhost", 9250);
        Socket 接続 = サーバー値.accept();
        if (接続.getPort() != ゲスト値.getLocalPort() || ゲスト値.getPort() != 接続.getLocalPort()) throw new RuntimeException("ポート値 불일치");
        byte[] データグラム = "한글 ストリーム値".getBytes("UTF-8");
        ゲスト値.getOutputStream().write(データグラム);
        byte[] 受信済み項目 = new byte[100];
        int 長さ = 接続.getInputStream().read(受信済み項目, 0, 受信済み項目.length);
        System.out.println(長さ == データグラム.length);
        for (int i = 0; i < 長さ; i++) if (受信済み項目[i] != データグラム[i]) throw new RuntimeException("内容物値 불일치");
        接続.getOutputStream().write(42);
        System.out.println(ゲスト値.getInputStream().read());
        ゲスト値.close();
        System.out.println(接続.getInputStream().read());
        接続.close(); サーバー値.close();
        ServerSocket 空サーバー = new ServerSocket(9250);
        空サーバー.setSoTimeout(10);
        try { 空サーバー.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("時間値 上限値"); }
        空サーバー.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 判定未対応"); }
        System.out.println("STREAM PASS");
    }
}
