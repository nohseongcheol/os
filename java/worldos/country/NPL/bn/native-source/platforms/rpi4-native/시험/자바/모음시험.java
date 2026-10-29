// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ভুক্তি_তালিকা = new ArrayList<String>(); ভুক্তি_তালিকা.add("한글"); ভুক্তি_তালিকা.add("😀"); ভুক্তি_তালিকা.add("日本語");
        System.out.println(ভুক্তি_তালিকা.get(1)); System.out.println(ভুক্তি_তালিকা.set(1, "পরিবর্তন_করা_মান")); System.out.println(ভুক্তি_তালিকা.remove(0));
        System.out.println(ভুক্তি_তালিকা.size()); System.out.println(ভুক্তি_তালিকা.get(0));
        Map<String, Integer> অভিধান = new HashMap<String, Integer>();
        অভিধান.put("하나", 1); অভিধান.put("둘", 2); System.out.println(অভিধান.put("하나", 3).intValue());
        System.out.println(অভিধান.get("하나").intValue()); System.out.println(অভিধান.containsKey("둘"));
        System.gc(); System.out.println(অভিধান.remove("둘").intValue()); System.out.println(অভিধান.size());
        ভুক্তি_তালিকা.clear(); অভিধান.clear(); System.out.println(ভুক্তি_তালিকা.isEmpty()); System.out.println(অভিধান.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("পাঠ")));
        String keep = "남는 পাঠ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
