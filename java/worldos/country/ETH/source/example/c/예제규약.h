#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int ጽሁፍ_ርዝመት(const char *ጽሁፍ) { int ርዝመት_እሴት=0;while(ጽሁፍ[ርዝመት_እሴት])ርዝመት_እሴት++;return ርዝመት_እሴት; }
static int ውጤት(const char *ጽሁፍ) { int ርዝመት_እሴት=ጽሁፍ_ርዝመት(ጽሁፍ);return ጻፍ_ፋይል_ውሂብ(1,ጽሁፍ,ርዝመት_እሴት)==ርዝመት_እሴት?0:1; }
#endif
