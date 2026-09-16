/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <प्रणाली/stat.h>
#include <प्रणाली/प्रणाली_पहचान.h>
#include <प्रणाली/संतान_प्रतीक्षा.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct संचिका_स्थिति st;
    struct utsname प्रणाली_की_पहचान;
    int संचिका_विवरणक = खोलना("/USER1", O_RDONLY);
    int copy = संचिका_विवरणक >= 0 ? खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना(संचिका_विवरणक) : -1;
    if (copy >= 0) बंद_करना(copy);
    if (संचिका_विवरणक >= 0) {
        खुली_संचिका_स्थिति_पाना(संचिका_विवरणक, &st);
        पठन_लेखन_स्थिति_बदलना(संचिका_विवरणक, 0, SEEK_SET);
        बंद_करना(संचिका_विवरणक);
    }
    संचिका_स्थिति("/", &st);
    प्रणाली_जानकारी_पाना(&प्रणाली_की_पहचान);
    कार्य_निर्देशिका_पथ_पाना(cwd, sizeof(cwd));
    return errno + प्रक्रिया_पहचान_पाना() + जनक_प्रक्रिया_पहचान_पाना();
}
