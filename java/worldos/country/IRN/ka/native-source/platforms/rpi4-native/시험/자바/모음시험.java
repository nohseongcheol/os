// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> შენატანი_სია = new ArrayList<String>(); შენატანი_სია.add("한글"); შენატანი_სია.add("😀"); შენატანი_სია.add("日本語");
        System.out.println(შენატანი_სია.get(1)); System.out.println(შენატანი_სია.set(1, "შეცვლა_მნიშვნელობა")); System.out.println(შენატანი_სია.remove(0));
        System.out.println(შენატანი_სია.size()); System.out.println(შენატანი_სია.get(0));
        Map<String, Integer> ლექსიკონი = new HashMap<String, Integer>();
        ლექსიკონი.put("하나", 1); ლექსიკონი.put("둘", 2); System.out.println(ლექსიკონი.put("하나", 3).intValue());
        System.out.println(ლექსიკონი.get("하나").intValue()); System.out.println(ლექსიკონი.containsKey("둘"));
        System.gc(); System.out.println(ლექსიკონი.remove("둘").intValue()); System.out.println(ლექსიკონი.size());
        შენატანი_სია.clear(); ლექსიკონი.clear(); System.out.println(შენატანი_სია.isEmpty()); System.out.println(ლექსიკონი.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("ტექსტი")));
        String keep = "남는 ტექსტი"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
