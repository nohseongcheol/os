// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> داخلا_فهرست = new ArrayList<String>(); داخلا_فهرست.add("한글"); داخلا_فهرست.add("😀"); داخلا_فهرست.add("日本語");
        System.out.println(داخلا_فهرست.get(1)); System.out.println(داخلا_فهرست.set(1, "تبديل_ڪريو_قدر")); System.out.println(داخلا_فهرست.remove(0));
        System.out.println(داخلا_فهرست.size()); System.out.println(داخلا_فهرست.get(0));
        Map<String, Integer> ڊڪشنري = new HashMap<String, Integer>();
        ڊڪشنري.put("하나", 1); ڊڪشنري.put("둘", 2); System.out.println(ڊڪشنري.put("하나", 3).intValue());
        System.out.println(ڊڪشنري.get("하나").intValue()); System.out.println(ڊڪشنري.containsKey("둘"));
        System.gc(); System.out.println(ڊڪشنري.remove("둘").intValue()); System.out.println(ڊڪشنري.size());
        داخلا_فهرست.clear(); ڊڪشنري.clear(); System.out.println(داخلا_فهرست.isEmpty()); System.out.println(ڊڪشنري.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 متن"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
