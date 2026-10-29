// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
import java.util.ArrayList;
/** 順序を持つ項目の集まり。この版では文字列の一覧を提供する。 */
public final class 入口一覧 {
    private final ArrayList<String> 入口値 = new ArrayList<String>();
    public void 値一覧追加(String 値) { 入口値.add(値); }
    public String 読取(int 順序値) { return 入口値.get(順序値); }
    public String 値置換(int 順序値, String 値) { return 入口値.set(順序値, 値); }
    public String 入口消去処理(int 順序値) { return 入口値.remove(順序値); }
    public int 容量() { return 入口値.size(); }
    public boolean 判定空値() { return 入口値.isEmpty(); }
    public void 内容消去() { 入口値.clear(); }
}
