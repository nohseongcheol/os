// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 順番に届くバイトを読み取る入力路。 */
public final class 入力ストリーム {
    private final java.io.InputStream 標準ストリーム;
    入力ストリーム(java.io.InputStream 標準ストリーム) { this.標準ストリーム = 標準ストリーム; }
    public int 読取() throws 入力出力例外 {
        try { return 標準ストリーム.read();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public int 読取(byte[] データ) throws 入力出力例外 {
        try { return 標準ストリーム.read(データ);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public int 読取(byte[] データ, int 起動処理, int 長さ) throws 入力出力例外 {
        try { return 標準ストリーム.read(データ, 起動処理, 長さ);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 閉鎖() throws 入力出力例外 {
        try { 標準ストリーム.close();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
}
