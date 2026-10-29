// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> okufakwayo_Uhlu = new ArrayList<String>(); okufakwayo_Uhlu.add("한글"); okufakwayo_Uhlu.add("😀"); okufakwayo_Uhlu.add("日本語");
        System.out.println(okufakwayo_Uhlu.get(1)); System.out.println(okufakwayo_Uhlu.set(1, "guqula_inani")); System.out.println(okufakwayo_Uhlu.remove(0));
        System.out.println(okufakwayo_Uhlu.size()); System.out.println(okufakwayo_Uhlu.get(0));
        Map<String, Integer> iqoqo_lokhiye = new HashMap<String, Integer>();
        iqoqo_lokhiye.put("하나", 1); iqoqo_lokhiye.put("둘", 2); System.out.println(iqoqo_lokhiye.put("하나", 3).intValue());
        System.out.println(iqoqo_lokhiye.get("하나").intValue()); System.out.println(iqoqo_lokhiye.containsKey("둘"));
        System.gc(); System.out.println(iqoqo_lokhiye.remove("둘").intValue()); System.out.println(iqoqo_lokhiye.size());
        okufakwayo_Uhlu.clear(); iqoqo_lokhiye.clear(); System.out.println(okufakwayo_Uhlu.isEmpty()); System.out.println(iqoqo_lokhiye.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Itekisi")));
        String keep = "남는 Itekisi"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
