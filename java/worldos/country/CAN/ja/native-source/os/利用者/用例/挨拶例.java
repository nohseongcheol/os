// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 挨拶例 {
    public static int 起動処理() {
        利用者.書込("Hello from a separate Java ELF!\n");
        利用者.書込(利用者.実行状態許可() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int 番号 = 0; 番号 < 利用者.引数列個数(); 番号++) {
            利用者.書込("arg: "); 利用者.書込(利用者.引数(番号)); 利用者.書込("\n");
        }
        return 利用者.実行状態許可() == 3 ? 0 : 1;
    }
}
