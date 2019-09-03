import os
import platform
from cffi import FFI

ffi = FFI()

ffi.cdef('''
    typedef void wrap_nvml_handle;
    wrap_nvml_handle* wrap_nvml_create();
    int wrap_nvml_destroy(wrap_nvml_handle* nvmlh);
    int wrap_nvml_get_gpucount(wrap_nvml_handle* nvmlh, int* gpucount);
    int wrap_nvml_get_gpu_name(wrap_nvml_handle* nvmlh, int gpuindex, char* namebuf, int bufsize);
    int wrap_nvml_get_tempC(wrap_nvml_handle* nvmlh, int gpuindex, unsigned int* tempC);
    int wrap_nvml_get_fanpcnt(wrap_nvml_handle* nvmlh, int gpuindex, unsigned int* fanpcnt);
    int wrap_nvml_get_power_usage(wrap_nvml_handle* nvmlh, int gpuindex, unsigned int* milliwatts);

    typedef void wrap_adl_handle;
    wrap_adl_handle* wrap_adl_create();
    int wrap_adl_destroy(wrap_adl_handle* adlh);
    int wrap_adl_get_gpucount(wrap_adl_handle* adlh, int* gpucount);
    int wrap_adl_get_gpu_name(wrap_adl_handle* adlh, int gpuindex, char* namebuf, int bufsize);
    int wrap_adl_get_gpu_pci_id(wrap_adl_handle* adlh, int gpuindex, char* idbuf, int bufsize);
    int wrap_adl_get_tempC(wrap_adl_handle* adlh, int gpuindex, unsigned int* tempC);
    int wrap_adl_get_fanpcnt(wrap_adl_handle* adlh, int gpuindex, unsigned int* fanpcnt);
    int wrap_adl_get_power_usage(wrap_adl_handle* adlh, int gpuindex, unsigned int* milliwatts);

''')

if platform.system() == 'Linux':
    lib = ffi.dlopen('./gpumon/libgpumon.so')
    nvHandle = lib.wrap_nvml_create()
    amdHandle = lib.wrap_adl_create()
else:
    nvHandle = None
    amdHandle = None

def nvmlGetGpuInfo():
    info = []
    if nvHandle:
        count = ffi.new("int*", 0)
        lib.wrap_nvml_get_gpucount(nvHandle, count)
        name = ffi.new("char[128]")
        tempC = ffi.new("unsigned int*", 0)
        fanpcnt = ffi.new("unsigned int*", 0)
        power_usage = ffi.new("unsigned int*", 0)
        for i in range(count[0]):
            deviceinfo = {}
            lib.wrap_nvml_get_gpu_name(nvHandle, i, name, 128)
            deviceinfo['name'] = ffi.string(name).decode()
            lib.wrap_nvml_get_tempC(nvHandle, i, tempC)
            deviceinfo['tempC'] = tempC[0]
            lib.wrap_nvml_get_fanpcnt(nvHandle, i, fanpcnt)
            deviceinfo['fanpcnt'] = fanpcnt[0]
            lib.wrap_nvml_get_power_usage(nvHandle, i, power_usage)
            deviceinfo['power_usage'] = power_usage[0]
            info.append(deviceinfo)
        ffi.release(count)
        ffi.release(name)
        ffi.release(tempC)
        ffi.release(fanpcnt)
        ffi.release(power_usage)
    return info

def amdGetGpuInfo():
    info = []
    if amdHandle:
        count = ffi.new("int*", 0)
        lib.wrap_adl_get_gpucount(amdHandle, count)
        name = ffi.new("char[128]")
        tempC = ffi.new("unsigned int*", 0)
        fanpcnt = ffi.new("unsigned int*", 0)
        power_usage = ffi.new("unsigned int*", 0)
        for i in range(count[0]):
            deviceinfo = {}
            lib.wrap_adl_get_gpu_name(amdHandle, i, name, 128)
            deviceinfo['name'] = ffi.string(name).decode()
            lib.wrap_adl_get_tempC(amdHandle, i, tempC)
            deviceinfo['tempC'] = tempC[0]
            lib.wrap_adl_get_fanpcnt(amdHandle, i, fanpcnt)
            deviceinfo['fanpcnt'] = fanpcnt[0]
            lib.wrap_adl_get_power_usage(amdHandle, i, power_usage)
            deviceinfo['power_usage'] = power_usage[0]
            info.append(deviceinfo)
        ffi.release(count)
        ffi.release(name)
        ffi.release(tempC)
        ffi.release(fanpcnt)
        ffi.release(power_usage)
    return info

if __name__ == '__main__':
    print(amdGetGpuInfo())
    print(nvmlGetGpuInfo())
    pass
