// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> girizmeklik_Sanaw = new ArrayList<String>(); girizmeklik_Sanaw.add("한글"); girizmeklik_Sanaw.add("😀"); girizmeklik_Sanaw.add("日本語");
        System.out.println(girizmeklik_Sanaw.get(1)); System.out.println(girizmeklik_Sanaw.set(1, "üýtget_baha")); System.out.println(girizmeklik_Sanaw.remove(0));
        System.out.println(girizmeklik_Sanaw.size()); System.out.println(girizmeklik_Sanaw.get(0));
        Map<String, Integer> sözlük = new HashMap<String, Integer>();
        sözlük.put("하나", 1); sözlük.put("둘", 2); System.out.println(sözlük.put("하나", 3).intValue());
        System.out.println(sözlük.get("하나").intValue()); System.out.println(sözlük.containsKey("둘"));
        System.gc(); System.out.println(sözlük.remove("둘").intValue()); System.out.println(sözlük.size());
        girizmeklik_Sanaw.clear(); sözlük.clear(); System.out.println(girizmeklik_Sanaw.isEmpty()); System.out.println(sözlük.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Metin")));
        String keep = "남는 Metin"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
