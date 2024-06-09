from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get

required_conan_version = ">=1.51.1"


class ConfuSociConan(ConanFile):
    name = "matchmaking_proxy"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "CMakeDeps", "CMakeToolchain"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["boost"].header_only = True


    def requirements(self):
        self.requires("boost/1.85.0", force=True)
        self.requires("durak/1.0.5", force=True)
        self.requires("confu_soci/[<1]")
        self.requires("magic_enum/[>=0.9.5 <10]")
        self.requires("certify/cci.20201114")
        self.requires("libsodium/1.0.18")
        self.requires("confu_json/1.1.0", force=True)
        self.requires("sml/1.1.11")
        self.requires("range-v3/0.12.0")
        self.requires("corrade/2020.06")
        self.requires("login_matchmaking_game_shared/latest")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self, src_folder=self.name + "-" + str(self.version))

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]
