// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> প্রবিষ্ট_সূচী = new ArrayList<String>(); প্রবিষ্ট_সূচী.add("한글"); প্রবিষ্ট_সূচী.add("😀"); প্রবিষ্ট_সূচী.add("日本語");
        System.out.println(প্রবিষ্ট_সূচী.get(1)); System.out.println(প্রবিষ্ট_সূচী.set(1, "পৰিবৰ্তন_কৰক_মান")); System.out.println(প্রবিষ্ট_সূচী.remove(0));
        System.out.println(প্রবিষ্ট_সূচী.size()); System.out.println(প্রবিষ্ট_সূচী.get(0));
        Map<String, Integer> অভিধান = new HashMap<String, Integer>();
        অভিধান.put("하나", 1); অভিধান.put("둘", 2); System.out.println(অভিধান.put("하나", 3).intValue());
        System.out.println(অভিধান.get("하나").intValue()); System.out.println(অভিধান.containsKey("둘"));
        System.gc(); System.out.println(অভিধান.remove("둘").intValue()); System.out.println(অভিধান.size());
        প্রবিষ্ট_সূচী.clear(); অভিধান.clear(); System.out.println(প্রবিষ্ট_সূচী.isEmpty()); System.out.println(অভিধান.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("টেক্সট")));
        String keep = "남는 টেক্সট"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
