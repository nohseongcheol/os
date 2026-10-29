// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** IPv4 UDP 電文による通信。外部の相手には数値アドレスを使う。 */
public final class 通信 {
    private 通信() {}
    public static DatagramSocket 開放(int ポート値) throws 入力出力例外 {
        try { return new DatagramSocket(ポート値);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static void 送信(DatagramSocket 通信端点, int ポート値, String 内容物値) throws 入力出力例外 {
        try {
        送信(通信端点, "127.0.0.1", ポート値, 内容物値);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static void 送信(DatagramSocket 通信端点, String 番地, int ポート値, String 内容物値) throws 入力出力例外 {
        try {
        byte[] バイト値 = 文字.符号化(内容物値);
        通信端点.send(new DatagramPacket(バイト値, バイト値.length, InetAddress.getByName(番地), ポート値));
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static String 受取(DatagramSocket 通信端点) throws 入力出力例外 {
        try {
        byte[] バイト値 = new byte[512]; DatagramPacket データグラム = new DatagramPacket(バイト値, バイト値.length); 通信端点.receive(データグラム);
        byte[] 結果 = new byte[データグラム.getLength()]; System.arraycopy(バイト値, 0, 結果, 0, 結果.length); return 文字.データ復号化(結果);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static void 待機期限(DatagramSocket 通信端点, int ミリ秒) throws 入力出力例外 {
        try { 通信端点.setSoTimeout(ミリ秒);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static void 閉鎖(DatagramSocket 通信端点) { 通信端点.close(); }
}
