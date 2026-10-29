// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> մուտքագրում_Ցուցակ = new ArrayList<String>(); մուտքագրում_Ցուցակ.add("한글"); մուտքագրում_Ցուցակ.add("😀"); մուտքագրում_Ցուցակ.add("日本語");
        System.out.println(մուտքագրում_Ցուցակ.get(1)); System.out.println(մուտքագրում_Ցուցակ.set(1, "փոխել_արժեք")); System.out.println(մուտքագրում_Ցուցակ.remove(0));
        System.out.println(մուտքագրում_Ցուցակ.size()); System.out.println(մուտքագրում_Ցուցակ.get(0));
        Map<String, Integer> բառացանկ = new HashMap<String, Integer>();
        բառացանկ.put("하나", 1); բառացանկ.put("둘", 2); System.out.println(բառացանկ.put("하나", 3).intValue());
        System.out.println(բառացանկ.get("하나").intValue()); System.out.println(բառացանկ.containsKey("둘"));
        System.gc(); System.out.println(բառացանկ.remove("둘").intValue()); System.out.println(բառացանկ.size());
        մուտքագրում_Ցուցակ.clear(); բառացանկ.clear(); System.out.println(մուտքագրում_Ցուցակ.isEmpty()); System.out.println(բառացանկ.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Տեքստ")));
        String keep = "남는 Տեքստ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
