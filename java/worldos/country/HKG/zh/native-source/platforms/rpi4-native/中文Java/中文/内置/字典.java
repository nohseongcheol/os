// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.内置;
import java.util.HashMap;
/** 把查询键映射到值。 */
public final class 字典 {
    private final HashMap<String, String> 条目值 = new HashMap<String, String>();
    public String 放入值(String 键材料, String 值) { return 条目值.put(键材料, 值); }
    public String 查找条目(String 键材料) { return 条目值.get(键材料); }
    public boolean 是否执行存在(String 键材料) { return 条目值.containsKey(键材料); }
    public String 擦除条目(String 键材料) { return 条目值.remove(键材料); }
    public int 大小() { return 条目值.size(); }
    public void 清空内容() { 条目值.clear(); }
}
