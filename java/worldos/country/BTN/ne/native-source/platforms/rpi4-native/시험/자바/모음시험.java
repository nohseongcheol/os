// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> प्रविष्टि_सूची = new ArrayList<String>(); प्रविष्टि_सूची.add("한글"); प्रविष्टि_सूची.add("😀"); प्रविष्टि_सूची.add("日本語");
        System.out.println(प्रविष्टि_सूची.get(1)); System.out.println(प्रविष्टि_सूची.set(1, "परिवर्तन_मान")); System.out.println(प्रविष्टि_सूची.remove(0));
        System.out.println(प्रविष्टि_सूची.size()); System.out.println(प्रविष्टि_सूची.get(0));
        Map<String, Integer> शब्दकोष = new HashMap<String, Integer>();
        शब्दकोष.put("하나", 1); शब्दकोष.put("둘", 2); System.out.println(शब्दकोष.put("하나", 3).intValue());
        System.out.println(शब्दकोष.get("하나").intValue()); System.out.println(शब्दकोष.containsKey("둘"));
        System.gc(); System.out.println(शब्दकोष.remove("둘").intValue()); System.out.println(शब्दकोष.size());
        प्रविष्टि_सूची.clear(); शब्दकोष.clear(); System.out.println(प्रविष्टि_सूची.isEmpty()); System.out.println(शब्दकोष.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("पाठ")));
        String keep = "남는 पाठ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
