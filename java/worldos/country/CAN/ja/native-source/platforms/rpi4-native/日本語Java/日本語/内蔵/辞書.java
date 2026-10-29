// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
import java.util.HashMap;
/** 検索キーに値を対応付ける辞書。 */
public final class 辞書 {
    private final HashMap<String, String> 入口値 = new HashMap<String, String>();
    public String 値格納(String キー素材, String 値) { return 入口値.put(キー素材, 値); }
    public String 入口探索(String キー素材) { return 入口値.get(キー素材); }
    public boolean 実施判定存在(String キー素材) { return 入口値.containsKey(キー素材); }
    public String 入口消去処理(String キー素材) { return 入口値.remove(キー素材); }
    public int 容量() { return 入口値.size(); }
    public void 内容消去() { 入口値.clear(); }
}
