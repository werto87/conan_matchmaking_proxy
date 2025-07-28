from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain
from conan.tools.files import get

required_conan_version = ">=1.51.1"

class ConfuSociConan(ConanFile):
    name = "matchmaking_proxy"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    options = {
        "fPIC":                                        [True, False],
        "with_log_for_state_machine":                  [True, False],
        "with_log_object_to_string_with_object_name":  [True, False],
        "with_ssl_verification":                       [True, False],
    }

    default_options = {
        "fPIC":                                        True,
        "with_log_for_state_machine":                  False,
        "with_log_object_to_string_with_object_name":  False,
        "with_ssl_verification":                       True
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        self.requires("boost/1.86.0",force=True,transitive_headers=True)
        self.requires("confu_soci/1.0.0",transitive_headers=True)
        self.requires("magic_enum/0.9.6")
        if self.options.with_ssl_verification:
            self.requires("certify/cci.20201114@modern-durak", force=True,transitive_headers=True)
        self.requires("libsodium/1.0.18", force=True,transitive_headers=True)
        self.requires("confu_json/1.1.1@modern-durak", force=True,transitive_headers=True)
        self.requires("sml/1.1.11")
        self.requires("confu_algorithm/1.2.1")
        self.requires("login_matchmaking_game_shared/latest")
        self.requires("my_web_socket/1.0.0",transitive_headers=True)
        self.requires("sqlite3/3.44.2")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        if self.options.with_log_for_state_machine:    
            tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_FOR_STATE_MACHINE"]  = None
        if self.options.with_log_object_to_string_with_object_name:
            tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_OBJECT_TO_STRING_WITH_OBJECT_NAME"]  = None
        tc.generate()

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
        self.cpp_info.components[self.name].requires = ["sqlite3::sqlite3","confu_algorithm::confu_algorithm", "sml::sml","my_web_socket::my_web_socket","login_matchmaking_game_shared::login_matchmaking_game_shared", "boost::headers","boost::filesystem","confu_soci::confu_soci","libsodium::libsodium","confu_json::confu_json","magic_enum::magic_enum"]
        if self.options.with_ssl_verification:
            self.cpp_info.components[self.name].requires += ["certify::_certify"]
        self.cpp_info.components[self.name].libs = [self.name]
