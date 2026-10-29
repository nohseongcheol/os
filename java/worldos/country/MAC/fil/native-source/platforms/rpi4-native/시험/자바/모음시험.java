// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> pagpasok_list = new ArrayList<String>(); pagpasok_list.add("한글"); pagpasok_list.add("😀"); pagpasok_list.add("日本語");
        System.out.println(pagpasok_list.get(1)); System.out.println(pagpasok_list.set(1, "baguhin_VALUE")); System.out.println(pagpasok_list.remove(0));
        System.out.println(pagpasok_list.size()); System.out.println(pagpasok_list.get(0));
        Map<String, Integer> diksyunaryo = new HashMap<String, Integer>();
        diksyunaryo.put("하나", 1); diksyunaryo.put("둘", 2); System.out.println(diksyunaryo.put("하나", 3).intValue());
        System.out.println(diksyunaryo.get("하나").intValue()); System.out.println(diksyunaryo.containsKey("둘"));
        System.gc(); System.out.println(diksyunaryo.remove("둘").intValue()); System.out.println(diksyunaryo.size());
        pagpasok_list.clear(); diksyunaryo.clear(); System.out.println(pagpasok_list.isEmpty()); System.out.println(diksyunaryo.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
