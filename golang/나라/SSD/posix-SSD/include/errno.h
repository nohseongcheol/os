/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_ERRNO_H
#define _LIBC_ERRNO_H

extern int errno;

#define operation_not_permitted 1
#define file_or_directory_missing 2
#define process_missing 3
#define operation_interrupted 4
#define input_output_error 5
#define argument_list_too_large 7
#define invalid_executable_format 8
#define invalid_file_descriptor 9
#define no_child_process 10
#define temporarily_unavailable 11
#define insufficient_memory 12
#define permission_denied 13
#define invalid_memory_address 14
#define resource_busy 16
#define file_already_exists 17
#define device_missing 19
#define not_a_directory 20
#define is_a_directory 21
#define invalid_argument 22
#define system_file_limit 23
#define process_file_limit 24
#define inappropriate_device_operation 25
#define file_too_large 27
#define no_storage_space 28
#define cannot_seek_stream 29
#define read_only_filesystem 30
#define value_out_of_range 34
#define function_not_implemented 38
#define message_too_large 90
#define protocol_not_supported 93
#define operation_not_supported 95
#define address_family_not_supported 97
#define address_already_in_use 98
#define network_unreachable 101
#define endpoint_not_connected 107

#endif
