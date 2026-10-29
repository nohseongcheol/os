// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.作業;

import ブラジル.JBraOS.記憶領域.ページ管理器;
import ブラジル.JBraOS.ファイルシステム.ファイル記述子表;

public final class プロセス値 {
    private final int 識別子値;
    private final int 親識別子;
    private final ページ管理器.番地空間 番地空間;
    private final ファイル記述子表 ファイル記述子;
    private プロセス状況 状況値 = プロセス状況.用意;
    private int 終了点コード;
    private int プログラム中断 = 0x06000000;
    private int 実行状態開始処理番地;
    private String[] 実行状態引数 = new String[0];
    private String[] 環境値 = new String[0];

    プロセス値(int 識別子値, int 親識別子, ページ管理器.番地空間 番地空間, ファイル記述子表 ファイル記述子) {
        this.識別子値 = 識別子値;
        this.親識別子 = 親識別子;
        this.番地空間 = 番地空間;
        this.ファイル記述子 = ファイル記述子;
    }

    public int 識別子値() {
        return 識別子値;
    }

    public int 親識別子() {
        return 親識別子;
    }

    public ページ管理器.番地空間 番地空間() {
        return 番地空間;
    }

    public ファイル記述子表 ファイル記述子() {
        return ファイル記述子;
    }

    public プロセス状況 状況値() {
        return 状況値;
    }

    public void 状況設定(プロセス状況 新規状況) {
        状況値 = 新規状況;
    }

    public int 終了点コード() {
        return 終了点コード;
    }

    public void 終了点プログラム(int 値) {
        終了点コード = 値 & 0xff;
        状況値 = プロセス状況.終了点プログラム;
    }

    public int プログラム中断() {
        return プログラム中断;
    }

    public void プログラム中断設定(int 新規終端位置) {
        if (新規終端位置 < 0x06000000 || 新規終端位置 > 0x07000000) {
            throw new IllegalArgumentException("プログラム 終端 범위를 벗어났습니다.");
        }
        プログラム中断 = 新規終端位置;
    }

    public void 実行状態文脈設定(int 番地開始処理, String[] 仮引数引数, String[] 環境) {
        実行状態開始処理番地 = 番地開始処理;
        実行状態引数 = 仮引数引数.clone();
        環境値 = 環境.clone();
    }

    public int 実行状態開始処理番地() { return 実行状態開始処理番地; }
    public String[] 実行状態引数() { return 実行状態引数.clone(); }
    public String[] 環境値() { return 環境値.clone(); }
}
