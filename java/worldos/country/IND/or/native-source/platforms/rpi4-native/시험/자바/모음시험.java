// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ଏଣ୍ଟ୍ରି_ତାଲିକା = new ArrayList<String>(); ଏଣ୍ଟ୍ରି_ତାଲିକା.add("한글"); ଏଣ୍ଟ୍ରି_ତାଲିକା.add("😀"); ଏଣ୍ଟ୍ରି_ତାଲିକା.add("日本語");
        System.out.println(ଏଣ୍ଟ୍ରି_ତାଲିକା.get(1)); System.out.println(ଏଣ୍ଟ୍ରି_ତାଲିକା.set(1, "ପରିବର୍ତ୍ତନ_ମୂଲ୍ୟ")); System.out.println(ଏଣ୍ଟ୍ରି_ତାଲିକା.remove(0));
        System.out.println(ଏଣ୍ଟ୍ରି_ତାଲିକା.size()); System.out.println(ଏଣ୍ଟ୍ରି_ତାଲିକା.get(0));
        Map<String, Integer> ଅଭିଧାନ = new HashMap<String, Integer>();
        ଅଭିଧାନ.put("하나", 1); ଅଭିଧାନ.put("둘", 2); System.out.println(ଅଭିଧାନ.put("하나", 3).intValue());
        System.out.println(ଅଭିଧାନ.get("하나").intValue()); System.out.println(ଅଭିଧାନ.containsKey("둘"));
        System.gc(); System.out.println(ଅଭିଧାନ.remove("둘").intValue()); System.out.println(ଅଭିଧାନ.size());
        ଏଣ୍ଟ୍ରି_ତାଲିକା.clear(); ଅଭିଧାନ.clear(); System.out.println(ଏଣ୍ଟ୍ରି_ତାଲିକା.isEmpty()); System.out.println(ଅଭିଧାନ.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("ପାଠ୍ଯ")));
        String keep = "남는 ପାଠ୍ଯ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
