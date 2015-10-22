import os
import hashlib
import shutil
import platform


def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)


def build_run_example(settings):
    current_dir = os.getcwd()
    sha = hashlib.sha1(settings).hexdigest()
    build_folder = os.path.join(current_dir, "build", sha)
    shutil.copytree("test", build_folder)
    try:
        os.chdir(build_folder)
        system('conan install %s' % (settings))
        system('conan build')
        system("cd bin && .%senough" % (os.sep))
    finally:
        os.chdir(current_dir)


if __name__ == "__main__":
    system('conan export lasote/stable')

    shutil.rmtree("build", ignore_errors=True)
    if platform.system() == "Windows":
        compiler = '-s compiler="Visual Studio" -s compiler.version=12 '
        # Static x86
        build_run_example(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=False')
        build_run_example(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=False')
        build_run_example(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=False')
        build_run_example(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=False')

        # Static x86_64
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=False')
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=False')
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=False')
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=False')

        # Shared x86
        build_run_example(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=True')
        build_run_example(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=True')
        build_run_example(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=True')
        build_run_example(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=True')

        # Shared x86_64
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=True')
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=True')
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=True')
        build_run_example(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=True')

    else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)
        # Static x86
        build_run_example('-s arch=x86 -s build_type=Debug -o zlib:shared=False')
        build_run_example('-s arch=x86 -s build_type=Release -o zlib:shared=False')

        # Shared x86
        build_run_example('-s arch=x86 -s build_type=Debug -o zlib:shared=True')
        build_run_example('-s arch=x86 -s build_type=Release -o zlib:shared=True')

        # Static x86_64
        build_run_example('-s arch=x86_64 -s build_type=Debug -o zlib:shared=False')
        build_run_example('-s arch=x86_64 -s build_type=Release -o zlib:shared=False')

        # Shared x86_64
        build_run_example('-s arch=x86_64 -s build_type=Debug -o zlib:shared=True')
        build_run_example('-s arch=x86_64 -s build_type=Release -o zlib:shared=True')