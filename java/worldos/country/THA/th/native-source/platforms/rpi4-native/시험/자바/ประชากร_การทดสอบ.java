// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class ประชากร_การทดสอบ {
    public static void main(String[] a) {
        List<String> รายการ_รายการ = new ArrayList<String>(); รายการ_รายการ.add("한글"); รายการ_รายการ.add("😀"); รายการ_รายการ.add("日本語");
        System.out.println(รายการ_รายการ.get(1)); System.out.println(รายการ_รายการ.set(1, "เปลี่ยนแปลง_ค่า")); System.out.println(รายการ_รายการ.remove(0));
        System.out.println(รายการ_รายการ.size()); System.out.println(รายการ_รายการ.get(0));
        Map<String, Integer> พจนานุกรม = new HashMap<String, Integer>();
        พจนานุกรม.put("하나", 1); พจนานุกรม.put("둘", 2); System.out.println(พจนานุกรม.put("하나", 3).intValue());
        System.out.println(พจนานุกรม.get("하나").intValue()); System.out.println(พจนานุกรม.containsKey("둘"));
        System.gc(); System.out.println(พจนานุกรม.remove("둘").intValue()); System.out.println(พจนานุกรม.size());
        รายการ_รายการ.clear(); พจนานุกรม.clear(); System.out.println(รายการ_รายการ.isEmpty()); System.out.println(พจนานุกรม.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("ข้อความ")));
        String keep = "남는 ข้อความ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
