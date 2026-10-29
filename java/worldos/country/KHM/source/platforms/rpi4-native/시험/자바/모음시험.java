// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ការបញ្ចូល_បញ្ជី = new ArrayList<String>(); ការបញ្ចូល_បញ្ជី.add("한글"); ការបញ្ចូល_បញ្ជី.add("😀"); ការបញ្ចូល_បញ្ជី.add("日本語");
        System.out.println(ការបញ្ចូល_បញ្ជី.get(1)); System.out.println(ការបញ្ចូល_បញ្ជី.set(1, "កែប្រែ_តំលៃ")); System.out.println(ការបញ្ចូល_បញ្ជី.remove(0));
        System.out.println(ការបញ្ចូល_បញ្ជី.size()); System.out.println(ការបញ្ចូល_បញ្ជី.get(0));
        Map<String, Integer> វចនានុក្រម = new HashMap<String, Integer>();
        វចនានុក្រម.put("하나", 1); វចនានុក្រម.put("둘", 2); System.out.println(វចនានុក្រម.put("하나", 3).intValue());
        System.out.println(វចនានុក្រម.get("하나").intValue()); System.out.println(វចនានុក្រម.containsKey("둘"));
        System.gc(); System.out.println(វចនានុក្រម.remove("둘").intValue()); System.out.println(វចនានុក្រម.size());
        ការបញ្ចូល_បញ្ជី.clear(); វចនានុក្រម.clear(); System.out.println(ការបញ្ចូល_បញ្ជី.isEmpty()); System.out.println(វចនានុក្រម.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("អត្ថបទ")));
        String keep = "남는 អត្ថបទ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
