// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;

/** 日本語 API の境界で標準 Java のエラーを変換する。標準 catch 節の意味は変えない。 */
final class 例外変換 {
    private 例外変換() {}
    public static 入力出力例外 入力出力(java.io.IOException エラー) {
        if (エラー instanceof 入力出力例外) return (入力出力例外)エラー;
        if (エラー instanceof java.net.SocketTimeoutException) return new 待合待機期限例外("通信の待ち時間を超えました。");
        if (エラー instanceof java.net.UnknownHostException) return new 番地検索例外("アドレスを解決できません。現在は数値の IPv4 アドレスを使用してください。");
        if (エラー instanceof java.io.FileNotFoundException) return new 未存在ファイル例外("ファイルを開けません。");
        if (エラー instanceof java.net.SocketException) return new 通信例外("通信の接続処理に失敗しました: " + エラー.getMessage());
        return new 入力出力例外("入出力処理に失敗しました: " + エラー.getMessage());
    }
    public static RuntimeException 命令実行(RuntimeException エラー) {
        if (エラー instanceof java.lang.NumberFormatException) return new 番号書式失敗("数値の形式と範囲を確認してください。");
        if (エラー instanceof java.lang.IllegalArgumentException) return new 無効引数例外("引数の値と範囲を確認してください。");
        if (エラー instanceof java.lang.ArrayIndexOutOfBoundsException) return new 配列境界例外("配列の範囲を超えました。");
        if (エラー instanceof java.lang.StringIndexOutOfBoundsException) return new 文字列境界例外("文字列の範囲を超えました。");
        if (エラー instanceof java.lang.IndexOutOfBoundsException) return new 境界例外("許可された範囲を超えました。");
        if (エラー instanceof java.lang.NullPointerException) return new 空参照参照例外("参照が空です。");
        return new 実行状態例外(エラー.getMessage());
    }
}
