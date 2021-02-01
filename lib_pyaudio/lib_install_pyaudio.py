
import os
import sys
import platform
import subprocess
import pkg_resources



def install():
    # Architecture
    architecture = "win_amd64" if platform.architecture()[0] == "64bit" else "win32"
    # Python Version
    version = sys.version.split(" ", maxsplit=1)[0].split(".")
    # Path WHL
    m = "" if int("".join(version[:2])) >= 37 else "m"
    name_file = "PyAudio-0.2.11-cp{version}-cp{version}{m}-{architecture}.whl".format(version="".join(version[:2]), architecture=architecture, m=m)
    path = os.path.join("lib_pyaudio", name_file)
    print(path)
    if not os.path.exists(path):
        raise Exception("Check your version : Python 3.6 >= 3.9")
    # Install Package
    subprocess.check_call([sys.executable, "-m", "pip", "install", path])



def get_installed_packages():
    """
    :rtype: list[tuple]
    """
    return sorted([(i.key, i.version) for i in pkg_resources.working_set])



if __name__ == '__main__':
    # install()
    import pkg_resources
    installed_packages_list = sorted([(i.key, i.version) for i in pkg_resources.working_set])
    for v in installed_packages_list:
        print(v)
