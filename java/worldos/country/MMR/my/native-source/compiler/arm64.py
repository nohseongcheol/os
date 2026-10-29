#!/usr/bin/env python3
"""기존 ARM64 ဘာသာပြန်စက်ကိရိယာတစ်ခု 경로와 Python 호출을 위한 호환 အချက်အမှတ်တစ်ခု."""
from ကြိုတင်ဘာသာပြန် import စက်ကုဒ်ဘာသာပြန်စက်, လုပ်ဆောင်


class ARM64(စက်ကုဒ်ဘာသာပြန်စက်):
    """기존 ARM64(...).generate(...) 호출을 ဆက်လက်တန်ဖိုး 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.ထုတ်လုပ်(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    လုပ်ဆောင်()
