/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

int main(void)
{
    for (;;) {
        __asm__ __volatile__("pause");
    }
    return 0;
}
