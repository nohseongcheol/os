// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 马来西亚.JMysOS.文件系统;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** 对应 engos FAT 读取层的只读文件存储管理模型。 */
public final class 文件系统 {
    static final class 已打开文件 {
        final byte[] 数据;
        int 位置;
        int 引用个数 = 1;

        已打开文件(byte[] 数据) {
            this.数据 = 数据;
        }
    }

    private final Map<String, byte[]> 文件条目列 = new LinkedHashMap<String, byte[]>();

    public void 追加文件(String 名称, byte[] 数据) {
        文件条目列.put(规范形式名称(名称), Arrays.copyOf(数据, 数据.length));
    }

    已打开文件 打开(String 名称) {
        byte[] 数据 = 文件条目列.get(规范形式名称(名称));
        if (数据 == null) {
            return null;
        }
        return new 已打开文件(数据);
    }

    public boolean 存在判断值(String 名称) {
        return 文件条目列.containsKey(规范形式名称(名称));
    }

    public 文件信息 系统信息(String 名称) {
        byte[] 数据 = 文件条目列.get(规范形式名称(名称));
        if (数据 == null) {
            return null;
        }
        return new 文件信息(数据.length, 0100444);
    }

    private String 规范形式名称(String 名称) {
        if (名称 == null) {
            throw new NullPointerException("文件 이름이 없습니다.");
        }
        String 结果 = 名称.startsWith("/") ? 名称.substring(1) : 名称;
        return 结果.toUpperCase(Locale.ROOT);
    }
}
