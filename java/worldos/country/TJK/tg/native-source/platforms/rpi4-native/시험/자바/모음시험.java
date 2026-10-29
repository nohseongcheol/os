// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ворида_Рӯйхат = new ArrayList<String>(); ворида_Рӯйхат.add("한글"); ворида_Рӯйхат.add("😀"); ворида_Рӯйхат.add("日本語");
        System.out.println(ворида_Рӯйхат.get(1)); System.out.println(ворида_Рӯйхат.set(1, "тағйир_додан_қимат")); System.out.println(ворида_Рӯйхат.remove(0));
        System.out.println(ворида_Рӯйхат.size()); System.out.println(ворида_Рӯйхат.get(0));
        Map<String, Integer> луғат = new HashMap<String, Integer>();
        луғат.put("하나", 1); луғат.put("둘", 2); System.out.println(луғат.put("하나", 3).intValue());
        System.out.println(луғат.get("하나").intValue()); System.out.println(луғат.containsKey("둘"));
        System.gc(); System.out.println(луғат.remove("둘").intValue()); System.out.println(луғат.size());
        ворида_Рӯйхат.clear(); луғат.clear(); System.out.println(ворида_Рӯйхат.isEmpty()); System.out.println(луғат.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 Матн"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
