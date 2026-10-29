// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国.JChnOS.存储装置设备;

import java.util.Arrays;

/** 与 ATA 28 位命令层一致的 512 字节逻辑扇区设备。 */
public final class 高级技术附件 {
    public static final int 区段大小 = 512;
    private final byte[] 数据;
    private final boolean 读取仅用值;

    public 高级技术附件(int 区段个数, boolean 读取仅用值) {
        if (区段个数 <= 0) {
            throw new IllegalArgumentException("区段值 수가 올바르지 않습니다.");
        }
        数据 = new byte[Math.multiplyExact(区段个数, 区段大小)];
        this.读取仅用值 = 读取仅用值;
    }

    public int 区段个数() {
        return 数据.length / 区段大小;
    }

    public void 读取(int 区段索引, byte[] 接收目的地址) {
        检查范围(区段索引, 接收目的地址);
        System.arraycopy(数据, 区段索引 * 区段大小, 接收目的地址, 0, 区段大小);
    }

    public void 写入(int 区段索引, byte[] 数据目标侧写入) {
        if (读取仅用值) {
            throw new IllegalStateException("读取 전용 장치입니다.");
        }
        检查范围(区段索引, 数据目标侧写入);
        System.arraycopy(数据目标侧写入, 0, 数据, 区段索引 * 区段大小, 区段大小);
    }

    public void 擦除条目() {
        if (读取仅用值) {
            throw new IllegalStateException("读取 전용 장치입니다.");
        }
        Arrays.fill(数据, (byte) 0);
    }

    private void 检查范围(int 区段索引, byte[] 临时空间) {
        if (区段索引 < 0 || 区段索引 >= 区段个数() || 临时空间.length < 区段大小) {
            throw new IllegalArgumentException("ATA 区段值 범위가 올바르지 않습니다.");
        }
    }
}

