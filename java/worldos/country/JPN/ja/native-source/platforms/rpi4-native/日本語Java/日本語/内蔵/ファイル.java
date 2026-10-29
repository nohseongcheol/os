// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 従来のファイルという概念を保つ。現在の格納域は再起動で消える RAM ファイル。 */
public final class ファイル {
    private ファイル() {}
    public static byte[] バイト値読取(String 名前) throws 入力出力例外 {
        try {
        FileInputStream ストリーム値 = new FileInputStream(名前);
        try {
            byte[] 一時値 = new byte[16384]; int 数 = 0, 値;
            while ((値 = ストリーム値.read()) != -1) { if (数 == 一時値.length) throw new 入力出力例外("ファイルの大きさの上限"); 一時値[数++] = (byte)値; }
            byte[] 結果 = new byte[数]; System.arraycopy(一時値, 0, 結果, 0, 数); return 結果;
        } finally { ストリーム値.close(); }
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static void バイト値書込(String 名前, byte[] 内容物値) throws 入力出力例外 {
        try {
        FileOutputStream ストリーム値 = new FileOutputStream(名前);
        try { for (int ループ添字 = 0; ループ添字 < 内容物値.length; ループ添字++) ストリーム値.write(内容物値[ループ添字] & 255); } finally { ストリーム値.close(); }
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static String 読取(String 名前) throws 入力出力例外 {
        try { return 文字.データ復号化(バイト値読取(名前));
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
    public static void 書込(String 名前, String 内容物値) throws 入力出力例外 {
        try { バイト値書込(名前, 文字.符号化(内容物値));
        } catch (java.io.IOException エラー) { throw 例外変換.入力出力(エラー); }
        catch (RuntimeException エラー) { throw 例外変換.命令実行(エラー); }
    }
}
