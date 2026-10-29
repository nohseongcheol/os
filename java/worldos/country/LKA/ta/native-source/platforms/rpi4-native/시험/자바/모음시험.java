// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> உள்ளீடு_பட்டியல் = new ArrayList<String>(); உள்ளீடு_பட்டியல்.add("한글"); உள்ளீடு_பட்டியல்.add("😀"); உள்ளீடு_பட்டியல்.add("日本語");
        System.out.println(உள்ளீடு_பட்டியல்.get(1)); System.out.println(உள்ளீடு_பட்டியல்.set(1, "மாற்று_மதிப்பு_16f64fe4")); System.out.println(உள்ளீடு_பட்டியல்.remove(0));
        System.out.println(உள்ளீடு_பட்டியல்.size()); System.out.println(உள்ளீடு_பட்டியல்.get(0));
        Map<String, Integer> அகராதி = new HashMap<String, Integer>();
        அகராதி.put("하나", 1); அகராதி.put("둘", 2); System.out.println(அகராதி.put("하나", 3).intValue());
        System.out.println(அகராதி.get("하나").intValue()); System.out.println(அகராதி.containsKey("둘"));
        System.gc(); System.out.println(அகராதி.remove("둘").intValue()); System.out.println(அகராதி.size());
        உள்ளீடு_பட்டியல்.clear(); அகராதி.clear(); System.out.println(உள்ளீடு_பட்டியல்.isEmpty()); System.out.println(அகராதி.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("உரை")));
        String keep = "남는 உரை"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
