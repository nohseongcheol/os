#ifndef _LIBC_FCNTL_H
#define _LIBC_FCNTL_H

#include <system/data_types.h>

#define open_read_only 0x0000
#define open_write_only 0x0001
#define open_read_write 0x0002
#define access_mode_mask 0x0003
#define create_if_missing 0x0040
#define require_new_file 0x0080
#define truncate_existing_file 0x0200
#define append_at_end 0x0400
#define require_directory 0x10000

#define duplicate_descriptor 0
#define read_descriptor_flags 1
#define set_descriptor_flags 2
#define read_file_status_flags 3
#define set_file_status_flags 4
#define close_on_program_replacement 1

#ifdef __cplusplus
extern "C" {
#endif
int open(const char *path, int oflag, ...);
int creat(const char *path, file_mode_type mode);
int fcntl(int file_descriptor, int cmd, ...);
#ifdef __cplusplus
}
#endif

#endif
