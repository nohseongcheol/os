// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 集合测试 {
    public static void main(String[] a) {
        List<String> 条目列表 = new ArrayList<String>(); 条目列表.add("한글"); 条目列表.add("😀"); 条目列表.add("日本語");
        System.out.println(条目列表.get(1)); System.out.println(条目列表.set(1, "更改值")); System.out.println(条目列表.remove(0));
        System.out.println(条目列表.size()); System.out.println(条目列表.get(0));
        Map<String, Integer> 字典 = new HashMap<String, Integer>();
        字典.put("一值", 1); 字典.put("둘", 2); System.out.println(字典.put("一值", 3).intValue());
        System.out.println(字典.get("一值").intValue()); System.out.println(字典.containsKey("둘"));
        System.gc(); System.out.println(字典.remove("둘").intValue()); System.out.println(字典.size());
        条目列表.clear(); 字典.clear(); System.out.println(条目列表.isEmpty()); System.out.println(字典.isEmpty());
        System.out.println("한글😀字符".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("文本")));
        String keep = "남는 文本"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
