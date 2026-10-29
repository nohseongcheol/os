// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
import java.util.HashMap;
/** 將查詢鍵對應到值。 */
public final class 字典 {
    private final HashMap<String, String> 條目值 = new HashMap<String, String>();
    public String 放入值(String 鍵材料, String 值) { return 條目值.put(鍵材料, 值); }
    public String 查找條目(String 鍵材料) { return 條目值.get(鍵材料); }
    public boolean 是否執行存在(String 鍵材料) { return 條目值.containsKey(鍵材料); }
    public String 擦除條目(String 鍵材料) { return 條目值.remove(鍵材料); }
    public int 大小() { return 條目值.size(); }
    public void 清空內容() { 條目值.clear(); }
}
