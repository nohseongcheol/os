// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 入ってくる TCP 接続を受け付ける窓口。 */
public final class ポート受取 {
    private final java.net.ServerSocket 標準ポート;
    private ポート受取(int ポート番号) throws 入力出力例外 {
        try { 標準ポート = new java.net.ServerSocket(ポート番号);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static ポート受取 開放(int ポート番号) throws 入力出力例外 {
        try { return new ポート受取(ポート番号);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public 接続経路 受取() throws 入力出力例外 {
        try { return new 接続経路(標準ポート.accept());
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public int ポート番号() { return 標準ポート.getLocalPort(); }
    public void 待機期限(int ミリ秒) throws 入力出力例外 {
        try { 標準ポート.setSoTimeout(ミリ秒);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public boolean 判定閉鎖済み() { return 標準ポート.isClosed(); }
    public void 閉鎖() throws 入力出力例外 {
        try { 標準ポート.close();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
}
