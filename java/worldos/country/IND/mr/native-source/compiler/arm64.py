#!/usr/bin/env python3
"""기존 ARM64 संकलक_साधन 경로와 Python 호출을 위한 호환 प्रविष्टी_गुण."""
from आगाऊ_संबंधित_वेळ_संकलक import मशीन_संहिता_संकलक, सुरू_करा


class ARM64(मशीन_संहिता_संकलक):
    """기존 ARM64(...).generate(...) 호출을 पुढीलक्रम_मूल्य 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.तयार_करा(entry, exports, सार्वत्रिक_वर्ण_संकेतन=True)


if __name__ == '__main__':
    सुरू_करा()
