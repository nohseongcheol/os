#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int ጽሑፍ_ንውሓት(const char *ጽሑፍ) { int ንውሓት_ዋጋ=0;while(ጽሑፍ[ንውሓት_ዋጋ])ንውሓት_ዋጋ++;return ንውሓት_ዋጋ; }
static int 출력(const char *ጽሑፍ) { int ንውሓት_ዋጋ=ጽሑፍ_ንውሓት(ጽሑፍ);return ጸሓፍ_ፋይል_ሓበሬታ(1,ጽሑፍ,ንውሓት_ዋጋ)==ንውሓት_ዋጋ?0:1; }
#endif
