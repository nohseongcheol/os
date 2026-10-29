// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> تێنووسین_لیست = new ArrayList<String>(); تێنووسین_لیست.add("한글"); تێنووسین_لیست.add("😀"); تێنووسین_لیست.add("日本語");
        System.out.println(تێنووسین_لیست.get(1)); System.out.println(تێنووسین_لیست.set(1, "گۆڕین_نرخ")); System.out.println(تێنووسین_لیست.remove(0));
        System.out.println(تێنووسین_لیست.size()); System.out.println(تێنووسین_لیست.get(0));
        Map<String, Integer> فەرهەنگ = new HashMap<String, Integer>();
        فەرهەنگ.put("하나", 1); فەرهەنگ.put("둘", 2); System.out.println(فەرهەنگ.put("하나", 3).intValue());
        System.out.println(فەرهەنگ.get("하나").intValue()); System.out.println(فەرهەنگ.containsKey("둘"));
        System.gc(); System.out.println(فەرهەنگ.remove("둘").intValue()); System.out.println(فەرهەنگ.size());
        تێنووسین_لیست.clear(); فەرهەنگ.clear(); System.out.println(تێنووسین_لیست.isEmpty()); System.out.println(فەرهەنگ.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 دەق"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
