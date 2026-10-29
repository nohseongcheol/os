// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 问候例 {
    public static int 运行() {
        用户.写入("Hello from a separate Java ELF!\n");
        用户.写入(用户.执行状态权限() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int 编号 = 0; 编号 < 用户.参数列个数(); 编号++) {
            用户.写入("arg: "); 用户.写入(用户.实参(编号)); 用户.写入("\n");
        }
        return 用户.执行状态权限() == 3 ? 0 : 1;
    }
}
