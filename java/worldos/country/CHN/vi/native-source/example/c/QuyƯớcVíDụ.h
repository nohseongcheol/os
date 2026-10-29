#ifndef ĐầuMụcVíDụBảnĐịa
#define ĐầuMụcVíDụBảnĐịa
#include <ABITệp.h>
#include <ABIMànHình.h>
static int độDàiVănBản(const char *vănBản) { int độDài=0;while(vănBản[độDài])độDài++;return độDài; }
static int ĐầuRa(const char *vănBản) { int độDài=độDàiVănBản(vănBản);return ghiDữLiệuTệp(1,vănBản,độDài)==độDài?0:1; }
#endif
