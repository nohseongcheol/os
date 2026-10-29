// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> cur_a_steach_Liosta = new ArrayList<String>(); cur_a_steach_Liosta.add("한글"); cur_a_steach_Liosta.add("😀"); cur_a_steach_Liosta.add("日本語");
        System.out.println(cur_a_steach_Liosta.get(1)); System.out.println(cur_a_steach_Liosta.set(1, "atharraich_VALUE")); System.out.println(cur_a_steach_Liosta.remove(0));
        System.out.println(cur_a_steach_Liosta.size()); System.out.println(cur_a_steach_Liosta.get(0));
        Map<String, Integer> faclair = new HashMap<String, Integer>();
        faclair.put("하나", 1); faclair.put("둘", 2); System.out.println(faclair.put("하나", 3).intValue());
        System.out.println(faclair.get("하나").intValue()); System.out.println(faclair.containsKey("둘"));
        System.gc(); System.out.println(faclair.remove("둘").intValue()); System.out.println(faclair.size());
        cur_a_steach_Liosta.clear(); faclair.clear(); System.out.println(cur_a_steach_Liosta.isEmpty()); System.out.println(faclair.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
