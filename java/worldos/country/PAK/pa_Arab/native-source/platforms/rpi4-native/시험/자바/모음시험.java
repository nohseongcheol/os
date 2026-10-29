// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> داخلہ_فرست = new ArrayList<String>(); داخلہ_فرست.add("한글"); داخلہ_فرست.add("😀"); داخلہ_فرست.add("日本語");
        System.out.println(داخلہ_فرست.get(1)); System.out.println(داخلہ_فرست.set(1, "تبدیل_کرو_قدر")); System.out.println(داخلہ_فرست.remove(0));
        System.out.println(داخلہ_فرست.size()); System.out.println(داخلہ_فرست.get(0));
        Map<String, Integer> لغت = new HashMap<String, Integer>();
        لغت.put("하나", 1); لغت.put("둘", 2); System.out.println(لغت.put("하나", 3).intValue());
        System.out.println(لغت.get("하나").intValue()); System.out.println(لغت.containsKey("둘"));
        System.gc(); System.out.println(لغت.remove("둘").intValue()); System.out.println(لغت.size());
        داخلہ_فرست.clear(); لغت.clear(); System.out.println(داخلہ_فرست.isEmpty()); System.out.println(لغت.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 متن"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
