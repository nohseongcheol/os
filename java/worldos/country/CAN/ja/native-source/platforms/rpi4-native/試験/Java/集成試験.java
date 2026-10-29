// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 集成試験 {
    public static void main(String[] a) {
        List<String> 入口一覧 = new ArrayList<String>(); 入口一覧.add("한글"); 入口一覧.add("😀"); 入口一覧.add("日本語");
        System.out.println(入口一覧.get(1)); System.out.println(入口一覧.set(1, "値変更")); System.out.println(入口一覧.remove(0));
        System.out.println(入口一覧.size()); System.out.println(入口一覧.get(0));
        Map<String, Integer> 辞書 = new HashMap<String, Integer>();
        辞書.put("一値", 1); 辞書.put("둘", 2); System.out.println(辞書.put("一値", 3).intValue());
        System.out.println(辞書.get("一値").intValue()); System.out.println(辞書.containsKey("둘"));
        System.gc(); System.out.println(辞書.remove("둘").intValue()); System.out.println(辞書.size());
        入口一覧.clear(); 辞書.clear(); System.out.println(入口一覧.isEmpty()); System.out.println(辞書.isEmpty());
        System.out.println("한글😀文字".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("文")));
        String keep = "남는 文"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
