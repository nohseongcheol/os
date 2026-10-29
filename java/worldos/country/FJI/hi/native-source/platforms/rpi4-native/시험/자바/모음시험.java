// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> एन्ट्री_सूची = new ArrayList<String>(); एन्ट्री_सूची.add("한글"); एन्ट्री_सूची.add("😀"); एन्ट्री_सूची.add("日本語");
        System.out.println(एन्ट्री_सूची.get(1)); System.out.println(एन्ट्री_सूची.set(1, "परिवर्तित_करें_मान")); System.out.println(एन्ट्री_सूची.remove(0));
        System.out.println(एन्ट्री_सूची.size()); System.out.println(एन्ट्री_सूची.get(0));
        Map<String, Integer> कोश = new HashMap<String, Integer>();
        कोश.put("하나", 1); कोश.put("둘", 2); System.out.println(कोश.put("하나", 3).intValue());
        System.out.println(कोश.get("하나").intValue()); System.out.println(कोश.containsKey("둘"));
        System.gc(); System.out.println(कोश.remove("둘").intValue()); System.out.println(कोश.size());
        एन्ट्री_सूची.clear(); कोश.clear(); System.out.println(एन्ट्री_सूची.isEmpty()); System.out.println(कोश.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("पाठ")));
        String keep = "남는 पाठ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
