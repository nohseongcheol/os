// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ورودی_لیست = new ArrayList<String>(); ورودی_لیست.add("한글"); ورودی_لیست.add("😀"); ورودی_لیست.add("日本語");
        System.out.println(ورودی_لیست.get(1)); System.out.println(ورودی_لیست.set(1, "تغییر_مقدار")); System.out.println(ورودی_لیست.remove(0));
        System.out.println(ورودی_لیست.size()); System.out.println(ورودی_لیست.get(0));
        Map<String, Integer> لغت_نامه = new HashMap<String, Integer>();
        لغت_نامه.put("하나", 1); لغت_نامه.put("둘", 2); System.out.println(لغت_نامه.put("하나", 3).intValue());
        System.out.println(لغت_نامه.get("하나").intValue()); System.out.println(لغت_نامه.containsKey("둘"));
        System.gc(); System.out.println(لغت_نامه.remove("둘").intValue()); System.out.println(لغت_نامه.size());
        ورودی_لیست.clear(); لغت_نامه.clear(); System.out.println(ورودی_لیست.isEmpty()); System.out.println(لغت_نامه.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("متن")));
        String keep = "남는 متن"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
