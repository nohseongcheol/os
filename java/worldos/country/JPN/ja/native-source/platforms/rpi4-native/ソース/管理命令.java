// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 管理命令 {
    static String 完了済み語() { return "通信設定 ソケット番地 応答試験 経路表 通信状況 作業一覧 稼働状況 記憶状況 保存容量 稼働時間 電源を切る 使い方"; }
    static String 語本文(int 番号) {
        if (番号==0) return "通信設定";
        if (番号==1) return "ソケット番地";
        if (番号==2) return "応答試験";
        if (番号==3) return "経路表";
        if (番号==4) return "通信状況";
        if (番号==5) return "作業一覧";
        if (番号==6) return "稼働状況";
        if (番号==7) return "記憶状況";
        if (番号==8) return "保存容量";
        if (番号==9) return "稼働時間";
        if (番号==10) return "電源を切る";
        return "使い方";
    }
    static String 説明(int 番号) {
        if (番号==0) return "IPv4 の番地・マスク・ゲートウェイ設定";
        if (番号==1) return "IPv4 の接続口と経路";
        if (番号==2) return "ICMP 応答と往復時間";
        if (番号==3) return "接続先の網と既定経路";
        if (番号==4) return "TCP/UDP の接続と通信量";
        if (番号==5) return "中核の作業と利用者の実行過程";
        if (番号==6) return "作業と記憶の表示更新; q / Ctrl+C で終了";
        if (番号==7) return "中核の記憶領域と利用者の割当量";
        if (番号==8) return "RAM 文書領域の容量と使用枠";
        if (番号==9) return "起動からの時間";
        if (番号==10) return "電源を切る; RAM 文書は消えます";
        return "命令と日本語の名前";
    }
}
