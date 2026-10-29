// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> енгізу_Тізім = new ArrayList<String>(); енгізу_Тізім.add("한글"); енгізу_Тізім.add("😀"); енгізу_Тізім.add("日本語");
        System.out.println(енгізу_Тізім.get(1)); System.out.println(енгізу_Тізім.set(1, "өзгерту_мән")); System.out.println(енгізу_Тізім.remove(0));
        System.out.println(енгізу_Тізім.size()); System.out.println(енгізу_Тізім.get(0));
        Map<String, Integer> сөздік = new HashMap<String, Integer>();
        сөздік.put("하나", 1); сөздік.put("둘", 2); System.out.println(сөздік.put("하나", 3).intValue());
        System.out.println(сөздік.get("하나").intValue()); System.out.println(сөздік.containsKey("둘"));
        System.gc(); System.out.println(сөздік.remove("둘").intValue()); System.out.println(сөздік.size());
        енгізу_Тізім.clear(); сөздік.clear(); System.out.println(енгізу_Тізім.isEmpty()); System.out.println(сөздік.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Мәтін")));
        String keep = "남는 Мәтін"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
