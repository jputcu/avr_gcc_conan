from conans import ConanFile, CMake, tools
from conans import AutoToolsBuildEnvironment

class AvrGccConan(ConanFile):
    name = "AvrGcc"
    version = "10.2"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    binutils_fullname = "binutils-2.34"
    gcc_fullname = "gcc-10.2.0"
    gdb_fullname = "gdb-9.2"
    libc_fullname = "avr-libc-2.0.0"

    def source_binutils(self):
        binutils_zip = "%s.tar.xz" % (self.binutils_fullname)
        tools.download("https://ftpmirror.gnu.org/binutils/%s" % (binutils_zip), binutils_zip)
        tools.unzip(binutils_zip)

    def build_binutils(self):
        tools.mkdir(self.binutils_fullname)
        with tools.chdir(self.binutils_fullname):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=["--disable-nls","--disable-werror"],
                configure_dir="%s/%s" % (self.source_folder, self.binutils_fullname), target="avr")
            autotools.make()
            autotools.install()

    def source_gcc(self):
        gcc_zip = "%s.tar.xz" % (self.gcc_fullname)
        tools.download("https://ftpmirror.gnu.org/gcc/%s/%s" % (self.gcc_fullname, gcc_zip), gcc_zip)
        tools.unzip(gcc_zip)
        with tools.chdir(self.gcc_fullname):
            self.run("contrib/download_prerequisites")

    def build_gcc(self):
        tools.mkdir(self.gcc_fullname)
        with tools.chdir(self.gcc_fullname):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=[
                "--disable-nls",
                "--enable-languages=c,c++",
                "--disable-libssp",
                "--disable-libada",
                "--with-dwarf2",
                "--disable-shared",
                "--enable-static",
                "--enable-mingw-wildcard",
                "--enable-plugin",
                "--with-gnu-as"
                ],
                configure_dir="%s/%s" % (self.source_folder, self.gcc_fullname), target="avr")
            autotools.make()
            autotools.install()

    def source_gdb(self):
        gdb_zip = "%s.tar.xz" % (self.gdb_fullname)
        tools.download("https://ftpmirror.gnu.org/gdb/%s" % (gdb_zip), gdb_zip)
        tools.unzip(gdb_zip)

    def build_gdb(self):
        tools.mkdir(self.gdb_fullname)
        with tools.chdir(self.gdb_fullname):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=[
                "--with-static-standard-libraries",
                "--disable-source-highlight"],
                configure_dir="%s/%s" % (self.source_folder, self.gdb_fullname), target="avr")
            autotools.make()
            autotools.install()

    def source_libc(self):
        libc_zip = "%s.tar.bz2" % (self.libc_fullname)
        tools.download("http://download.savannah.gnu.org/releases/avr-libc/%s" % (libc_zip), libc_zip)
        tools.unzip(libc_zip)

    def build_libc(self):
        tools.mkdir(self.libc_fullname)
        with tools.chdir(self.libc_fullname):
            with tools.environment_append({"PATH":["%s/bin" % (self.package_folder)]}):
                autotools = AutoToolsBuildEnvironment(self)
                autotools.configure(host="avr", configure_dir="%s/%s" % (self.source_folder, self.libc_fullname))
                autotools.make()
                autotools.install()

    def source(self):
        self.source_binutils()
        self.source_gcc()
        self.source_gdb()
        self.source_libc()

    def build(self):
        self.build_binutils()
        self.build_gcc()
        self.build_gdb()
        self.build_libc()

    def package(self):
        self.copy("*", src="%s/package" % (self.build_folder))

