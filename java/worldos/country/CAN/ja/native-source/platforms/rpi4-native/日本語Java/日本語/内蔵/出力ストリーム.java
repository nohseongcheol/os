// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 順序を保ってバイトを書き出す出力路。 */
public final class 出力ストリーム {
    private final java.io.OutputStream 標準ストリーム;
    出力ストリーム(java.io.OutputStream 標準ストリーム) { this.標準ストリーム = 標準ストリーム; }
    public void 書込(int 値) throws 入力出力例外 {
        try { 標準ストリーム.write(値);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 書込(byte[] データ) throws 入力出力例外 {
        try { 標準ストリーム.write(データ);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 書込(byte[] データ, int 起動処理, int 長さ) throws 入力出力例外 {
        try { 標準ストリーム.write(データ, 起動処理, 長さ);
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 値出力() throws 入力出力例外 {
        try { 標準ストリーム.flush();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public void 閉鎖() throws 入力出力例外 {
        try { 標準ストリーム.close();
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
}
