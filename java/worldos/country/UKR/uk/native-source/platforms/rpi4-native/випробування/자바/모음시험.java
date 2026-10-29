// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> запис_список = new ArrayList<String>(); запис_список.add("한글"); запис_список.add("😀"); запис_список.add("日本語");
        System.out.println(запис_список.get(1)); System.out.println(запис_список.set(1, "змінювати_значення")); System.out.println(запис_список.remove(0));
        System.out.println(запис_список.size()); System.out.println(запис_список.get(0));
        Map<String, Integer> словник = new HashMap<String, Integer>();
        словник.put("하나", 1); словник.put("둘", 2); System.out.println(словник.put("하나", 3).intValue());
        System.out.println(словник.get("하나").intValue()); System.out.println(словник.containsKey("둘"));
        System.gc(); System.out.println(словник.remove("둘").intValue()); System.out.println(словник.size());
        запис_список.clear(); словник.clear(); System.out.println(запис_список.isEmpty()); System.out.println(словник.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("текст")));
        String keep = "남는 текст"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
