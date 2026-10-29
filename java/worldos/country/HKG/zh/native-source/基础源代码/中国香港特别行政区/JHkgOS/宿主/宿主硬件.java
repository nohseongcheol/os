// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国香港特别行政区.JHkgOS.宿主;

import java.util.HashMap;
import java.util.Map;
import 中国香港特别行政区.JHkgOS.内核.硬件值;

/** 在普通 JVM 上对受管理内核进行确定性测试的硬件替身。 */
public final class 宿主硬件 implements 硬件值 {
    private final Map<Integer, Integer> 硬件端口值 = new HashMap<Integer, Integer>();
    private final StringBuilder 串行日志 = new StringBuilder();

    @Override
    public void 串行输出(String 内容值) {
        串行日志.append(内容值);
        System.out.print(内容值);
    }

    @Override
    public int 读取端口字节(int 硬件端口编号) {
        Integer 值 = 硬件端口值.get(Integer.valueOf(硬件端口编号));
        return 值 == null ? 0 : 值.intValue();
    }

    @Override
    public void 写入端口字节(int 硬件端口编号, int 值) {
        硬件端口值.put(Integer.valueOf(硬件端口编号), Integer.valueOf(值 & 0xff));
    }

    @Override
    public void 停机CPU() {
        // 宿主测试中立即返回，不等待下一事件。
    }

    public String 串行日志() {
        return 串行日志.toString();
    }
}

