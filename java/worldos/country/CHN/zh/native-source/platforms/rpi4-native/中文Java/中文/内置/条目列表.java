// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
import java.util.ArrayList;
/** 有序的项目集合；本版提供字符串列表。 */
public final class 条目列表 {
    private final ArrayList<String> 条目值 = new ArrayList<String>();
    public void 添加值列(String 值) { 条目值.add(值); }
    public String 读取(int 排序值) { return 条目值.get(排序值); }
    public String 替换值(int 排序值, String 值) { return 条目值.set(排序值, 值); }
    public String 擦除条目(int 排序值) { return 条目值.remove(排序值); }
    public int 大小() { return 条目值.size(); }
    public boolean 是否空值() { return 条目值.isEmpty(); }
    public void 清空内容() { 条目值.clear(); }
}
