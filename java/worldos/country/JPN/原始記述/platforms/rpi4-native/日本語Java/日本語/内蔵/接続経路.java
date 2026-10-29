// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 相手へ接続された TCP バイト流の端点。 */
public final class 接続経路 {
    private final java.net.Socket 標準ライブラリ橋渡し;
    接続経路(java.net.Socket 標準ライブラリ橋渡し) { this.標準ライブラリ橋渡し = 標準ライブラリ橋渡し; }
    public static 接続経路 開放(String 番地, int ポート番号) throws 入力出力例外 {
        try {
            return new 接続経路(new java.net.Socket(番地, ポート番号));
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public 入力ストリーム 入力値() throws 入力出力例外 {
        try { return new 入力ストリーム(標準ライブラリ橋渡し.getInputStream());
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public 出力ストリーム 出力() throws 入力出力例外 {
        try { return new 出力ストリーム(標準ライブラリ橋渡し.getOutputStream());
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 待機期限(int ミリ秒) throws 入力出力例外 {
        try { 標準ライブラリ橋渡し.setSoTimeout(ミリ秒);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public int ポート番号() { return 標準ライブラリ橋渡し.getPort(); }
    public int 局所ポート番号() { return 標準ライブラリ橋渡し.getLocalPort(); }
    public boolean 判定閉鎖済み() { return 標準ライブラリ橋渡し.isClosed(); }
    public boolean 接続済み() { return 標準ライブラリ橋渡し.isConnected(); }
    public void 閉鎖() throws 入力出力例外 {
        try { 標準ライブラリ橋渡し.close();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
}
