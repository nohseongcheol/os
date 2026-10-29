// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class مجموعة_يختبر {
    public static void main(String[] a) {
        List<String> إدخال_قائمة_f07b3200 = new ArrayList<String>(); إدخال_قائمة_f07b3200.add("한글"); إدخال_قائمة_f07b3200.add("😀"); إدخال_قائمة_f07b3200.add("日本語");
        System.out.println(إدخال_قائمة_f07b3200.get(1)); System.out.println(إدخال_قائمة_f07b3200.set(1, "يغيّر_قيمة")); System.out.println(إدخال_قائمة_f07b3200.remove(0));
        System.out.println(إدخال_قائمة_f07b3200.size()); System.out.println(إدخال_قائمة_f07b3200.get(0));
        Map<String, Integer> قاموس = new HashMap<String, Integer>();
        قاموس.put("하나", 1); قاموس.put("둘", 2); System.out.println(قاموس.put("하나", 3).intValue());
        System.out.println(قاموس.get("하나").intValue()); System.out.println(قاموس.containsKey("둘"));
        System.gc(); System.out.println(قاموس.remove("둘").intValue()); System.out.println(قاموس.size());
        إدخال_قائمة_f07b3200.clear(); قاموس.clear(); System.out.println(إدخال_قائمة_f07b3200.isEmpty()); System.out.println(قاموس.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("نص")));
        String keep = "남는 نص"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
