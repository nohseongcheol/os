// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 標準の main を持つ既存コードでは、非公開の補助メソッドを入口に選ばない。 */
public class 入口互換性試験 {
    private static void 起動処理() { System.out.println("補助値 関数 呼出"); }
    public static void main(String[] 引数) {
        起動処理();
        System.out.println("표준 入口点 値維持");
    }
}
