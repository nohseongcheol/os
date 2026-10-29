// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class ThửTậpHợp {
    public static void main(String[] a) {
        List<String> danhSáchMục = new ArrayList<String>(); danhSáchMục.add("한글"); danhSáchMục.add("😀"); danhSáchMục.add("日本語");
        System.out.println(danhSáchMục.get(1)); System.out.println(danhSáchMục.set(1, "đổiGiáTrị")); System.out.println(danhSáchMục.remove(0));
        System.out.println(danhSáchMục.size()); System.out.println(danhSáchMục.get(0));
        Map<String, Integer> TừĐiển = new HashMap<String, Integer>();
        TừĐiển.put("giáTrịMột", 1); TừĐiển.put("둘", 2); System.out.println(TừĐiển.put("giáTrịMột", 3).intValue());
        System.out.println(TừĐiển.get("giáTrịMột").intValue()); System.out.println(TừĐiển.containsKey("둘"));
        System.gc(); System.out.println(TừĐiển.remove("둘").intValue()); System.out.println(TừĐiển.size());
        danhSáchMục.clear(); TừĐiển.clear(); System.out.println(danhSáchMục.isEmpty()); System.out.println(TừĐiển.isEmpty());
        System.out.println("한글😀KýTự".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("vănBản")));
        String keep = "남는 vănBản"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
