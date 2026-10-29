// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ເຂົ້າໃນ_ລາຍຊື່ = new ArrayList<String>(); ເຂົ້າໃນ_ລາຍຊື່.add("한글"); ເຂົ້າໃນ_ລາຍຊື່.add("😀"); ເຂົ້າໃນ_ລາຍຊື່.add("日本語");
        System.out.println(ເຂົ້າໃນ_ລາຍຊື່.get(1)); System.out.println(ເຂົ້າໃນ_ລາຍຊື່.set(1, "ປ່ຽນ_ແປງ_ຄ່າ")); System.out.println(ເຂົ້າໃນ_ລາຍຊື່.remove(0));
        System.out.println(ເຂົ້າໃນ_ລາຍຊື່.size()); System.out.println(ເຂົ້າໃນ_ລາຍຊື່.get(0));
        Map<String, Integer> ວັດ_ຈະ_ນາ_ນຸ_ກົມ = new HashMap<String, Integer>();
        ວັດ_ຈະ_ນາ_ນຸ_ກົມ.put("하나", 1); ວັດ_ຈະ_ນາ_ນຸ_ກົມ.put("둘", 2); System.out.println(ວັດ_ຈະ_ນາ_ນຸ_ກົມ.put("하나", 3).intValue());
        System.out.println(ວັດ_ຈະ_ນາ_ນຸ_ກົມ.get("하나").intValue()); System.out.println(ວັດ_ຈະ_ນາ_ນຸ_ກົມ.containsKey("둘"));
        System.gc(); System.out.println(ວັດ_ຈະ_ນາ_ນຸ_ກົມ.remove("둘").intValue()); System.out.println(ວັດ_ຈະ_ນາ_ນຸ_ກົມ.size());
        ເຂົ້າໃນ_ລາຍຊື່.clear(); ວັດ_ຈະ_ນາ_ນຸ_ກົມ.clear(); System.out.println(ເຂົ້າໃນ_ລາຍຊື່.isEmpty()); System.out.println(ວັດ_ຈະ_ນາ_ນຸ_ກົມ.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 ຂໍ້ຄວາມ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
