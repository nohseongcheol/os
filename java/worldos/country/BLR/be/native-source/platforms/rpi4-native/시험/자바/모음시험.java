// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> увядзенне_Спіс = new ArrayList<String>(); увядзенне_Спіс.add("한글"); увядзенне_Спіс.add("😀"); увядзенне_Спіс.add("日本語");
        System.out.println(увядзенне_Спіс.get(1)); System.out.println(увядзенне_Спіс.set(1, "змяніць_значэнне")); System.out.println(увядзенне_Спіс.remove(0));
        System.out.println(увядзенне_Спіс.size()); System.out.println(увядзенне_Спіс.get(0));
        Map<String, Integer> слоўнік = new HashMap<String, Integer>();
        слоўнік.put("하나", 1); слоўнік.put("둘", 2); System.out.println(слоўнік.put("하나", 3).intValue());
        System.out.println(слоўнік.get("하나").intValue()); System.out.println(слоўнік.containsKey("둘"));
        System.gc(); System.out.println(слоўнік.remove("둘").intValue()); System.out.println(слоўнік.size());
        увядзенне_Спіс.clear(); слоўнік.clear(); System.out.println(увядзенне_Спіс.isEmpty()); System.out.println(слоўнік.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Тэкст")));
        String keep = "남는 Тэкст"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
