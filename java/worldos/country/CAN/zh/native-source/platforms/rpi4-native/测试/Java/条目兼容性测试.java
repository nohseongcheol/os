// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 对于具有标准 main 的现有代码，不把私有辅助方法选作入口。 */
public class 条目兼容性测试 {
    private static void 运行() { System.out.println("辅助值 函数 调用"); }
    public static void main(String[] 实参) {
        运行();
        System.out.println("표준 条目分 保持值");
    }
}
