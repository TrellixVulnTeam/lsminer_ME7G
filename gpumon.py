import os 
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
              
#dirs = os.path.split(os.path.realpath(__file__))[0]                   
lib = ffi.dlopen('./gpumon/libgpumon.so')

nvHandle = lib.wrap_nvml_create()
amdHandle = lib.wrap_adl_create()

def nvmlGetGpuInfo():
    info = []
    if nvHandle:
        count = ffi.new("int*", 0)
        lib.wrap_nvml_get_gpucount(nvHandle, count)
        deviceinfo = {}
        for i in range(count):
            name = ffi.new("char[128]")
            tmp = ffi.new("unsigned int*", 0)
            lib.wrap_nvml_get_gpu_name(nvHandle, i, name)
            deviceinfo['name'] = ffi.string(name).decode()
            lib.wrap_nvml_get_tempC(nvHandle, i, tmp)
            deviceinfo['tempC'] = tmp[0]
            lib.wrap_nvml_get_fanpcnt(nvHandle, i, tmp)
            deviceinfo['fanpcnt'] = tmp[0]
            lib.wrap_nvml_get_power_usage(nvHandle, i, tmp)
            deviceinfo['power_usage'] = tmp[0]
            info.append(deviceinfo)
            deviceinfo.clear()
    return info

def amdGetGpuInfo():
    info = []
    if amdHandle:
        count = ffi.new("int*", 0)
        lib.wrap_adl_get_gpucount(amdHandle, count)
        deviceinfo = {}
        for i in range(count):
            name = ffi.new("char[128]")
            tmp = ffi.new("unsigned int*", 0)
            lib.wrap_adl_get_gpu_name(amdHandle, i, name)
            deviceinfo['name'] = ffi.string(name).decode()
            lib.wrap_adl_get_tempC(amdHandle, i, tmp)
            deviceinfo['tempC'] = tmp[0]
            lib.wrap_adl_get_fanpcnt(amdHandle, i, tmp)
            deviceinfo['fanpcnt'] = tmp[0]
            lib.wrap_adl_get_power_usage(amdHandle, i, tmp)
            deviceinfo['power_usage'] = tmp[0]
            info.append(deviceinfo)
            deviceinfo.clear()
    return info

if __name__ == '__main__':
    print(amdGetGpuInfo())
    print(nvmlGetGpuInfo())
