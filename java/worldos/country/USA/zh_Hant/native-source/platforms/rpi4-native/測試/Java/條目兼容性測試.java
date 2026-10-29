// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 對於具有標準 main 的既有程式，不把私有輔助方法選作進入點。 */
public class 條目兼容性測試 {
    private static void 運行() { System.out.println("輔助值 函數 調用"); }
    public static void main(String[] 實參) {
        運行();
        System.out.println("표준 條目分 保持值");
    }
}
