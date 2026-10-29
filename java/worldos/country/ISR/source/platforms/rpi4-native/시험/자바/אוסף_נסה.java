// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class אוסף_נסה {
    public static void main(String[] a) {
        List<String> ערך_רשימה = new ArrayList<String>(); ערך_רשימה.add("한글"); ערך_רשימה.add("😀"); ערך_רשימה.add("日本語");
        System.out.println(ערך_רשימה.get(1)); System.out.println(ערך_רשימה.set(1, "שנה_ערך")); System.out.println(ערך_רשימה.remove(0));
        System.out.println(ערך_רשימה.size()); System.out.println(ערך_רשימה.get(0));
        Map<String, Integer> מילון = new HashMap<String, Integer>();
        מילון.put("하나", 1); מילון.put("둘", 2); System.out.println(מילון.put("하나", 3).intValue());
        System.out.println(מילון.get("하나").intValue()); System.out.println(מילון.containsKey("둘"));
        System.gc(); System.out.println(מילון.remove("둘").intValue()); System.out.println(מילון.size());
        ערך_רשימה.clear(); מילון.clear(); System.out.println(ערך_רשימה.isEmpty()); System.out.println(מילון.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("טקסט")));
        String keep = "남는 טקסט"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
