#!/usr/bin/env python3
"""기존 ARM64 कंपाइलर_उपकरण 경로와 Python 호출을 위한 호환 प्रवेश_बिदुं."""
from पूर्वसंकलक import यंत्र_कोड_कंपाइलर, चलाएँ


class ARM64(यंत्र_कोड_कंपाइलर):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.जनरेट_करें(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    चलाएँ()
