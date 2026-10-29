// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 電文の境界を保った UDP データを送受信する端点。 */
public final class データグラムチャネル {
    private final java.net.DatagramSocket 標準通信端点;
    private データグラムチャネル(int ポート番号) throws 入力出力例外 {
        try { 標準通信端点 = 通信.開放(ポート番号);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static データグラムチャネル 開放(int ポート番号) throws 入力出力例外 {
        try { return new データグラムチャネル(ポート番号);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 送信(String 番地, int ポート番号, String データ) throws 入力出力例外 {
        try { 通信.送信(標準通信端点, 番地, ポート番号, データ);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public String 受取() throws 入力出力例外 {
        try { return 通信.受取(標準通信端点);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 待機期限(int ミリ秒) throws 入力出力例外 {
        try { 通信.待機期限(標準通信端点, ミリ秒);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public int ポート番号() { return 標準通信端点.getLocalPort(); }
    public boolean 判定閉鎖済み() { return 標準通信端点.isClosed(); }
    public void 閉鎖() { 通信.閉鎖(標準通信端点); }
}
