#!/usr/bin/env python3
"""기존 ARM64 编译器工具 경로와 Python 호출을 위한 호환 条目分."""
from 提前所属时间编译器 import 计算机代码编译器, 运行


class ARM64(计算机代码编译器):
    """기존 ARM64(...).generate(...) 호출을 继续状态值 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.生成(entry, exports, 通用字符表示法=True)


if __name__ == '__main__':
    运行()
