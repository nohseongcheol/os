// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ndebà_ndepụta = new ArrayList<String>(); ndebà_ndepụta.add("한글"); ndebà_ndepụta.add("😀"); ndebà_ndepụta.add("日本語");
        System.out.println(ndebà_ndepụta.get(1)); System.out.println(ndebà_ndepụta.set(1, "gbanwèe_valuu")); System.out.println(ndebà_ndepụta.remove(0));
        System.out.println(ndebà_ndepụta.size()); System.out.println(ndebà_ndepụta.get(0));
        Map<String, Integer> ọkọwa_okwu = new HashMap<String, Integer>();
        ọkọwa_okwu.put("하나", 1); ọkọwa_okwu.put("둘", 2); System.out.println(ọkọwa_okwu.put("하나", 3).intValue());
        System.out.println(ọkọwa_okwu.get("하나").intValue()); System.out.println(ọkọwa_okwu.containsKey("둘"));
        System.gc(); System.out.println(ọkọwa_okwu.remove("둘").intValue()); System.out.println(ọkọwa_okwu.size());
        ndebà_ndepụta.clear(); ọkọwa_okwu.clear(); System.out.println(ndebà_ndepụta.isEmpty()); System.out.println(ọkọwa_okwu.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
