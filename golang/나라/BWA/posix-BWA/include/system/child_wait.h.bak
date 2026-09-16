#ifndef _include_system_child_wait
#define _include_system_child_wait

#include <system/data_types.h>

#define do_not_wait_if_unready 1
#define extract_exit_status(status) (((status) >> 8) & 0xff)
#define exited_normally(status) (((status) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
process_identifier_type wait(int *status);
process_identifier_type waitpid(process_identifier_type pid, int *status, int options);
#ifdef __cplusplus
}
#endif

#endif
