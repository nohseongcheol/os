// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.中核;

/** Java 管理カーネルと CPU 固有コードを隔てる唯一の境界。 */
public interface 機器値 {
    void 直列出力(String 内容物値);

    int ポートバイト読取(int 機器ポート番号);

    void ポートバイト書込(int 機器ポート番号, int 値);

    void 機械停止CPU();
}

