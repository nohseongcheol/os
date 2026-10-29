// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
import java.util.ArrayList;
/** 有順序的項目集合；本版提供字串清單。 */
public final class 條目列表 {
    private final ArrayList<String> 條目值 = new ArrayList<String>();
    public void 添加值列(String 值) { 條目值.add(值); }
    public String 讀取(int 排序值) { return 條目值.get(排序值); }
    public String 替換值(int 排序值, String 值) { return 條目值.set(排序值, 值); }
    public String 擦除條目(int 排序值) { return 條目值.remove(排序值); }
    public int 大小() { return 條目值.size(); }
    public boolean 是否空值() { return 條目值.isEmpty(); }
    public void 清空內容() { 條目值.clear(); }
}
