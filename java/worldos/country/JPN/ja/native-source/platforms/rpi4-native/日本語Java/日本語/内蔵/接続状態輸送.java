// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
import java.net.*;
public final class 接続状態輸送 {
    private 接続状態輸送() {}
    public static 接続経路 開放(String 番地, int ポート番号) throws 入力出力例外 {
        try { return 接続経路.開放(番地, ポート番号);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static ポート受取 受信先開放(int ポート番号) throws 入力出力例外 {
        try { return ポート受取.開放(ポート番号);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static Socket 接続(String 番地, int ポート値) throws 入力出力例外 {
        try { return new Socket(番地, ポート値);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static ServerSocket 通信端点接続待機(int ポート値) throws 入力出力例外 {
        try { return new ServerSocket(ポート値);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static Socket 受取(ServerSocket サーバー値) throws 入力出力例外 {
        try { return サーバー値.accept();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
}
