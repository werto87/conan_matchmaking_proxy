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
        "with_log_co_spawn_print_exceptions":          [True, False],
        "with_log_my_websocket":                       [True, False],
        "with_my_websocket_read_end":                  [True, False],
        "with_log_for_state_machine":                  [True, False],
        "with_log_object_to_string_with_object_name":  [True, False],
    }

    default_options = {
        "fPIC":                                        True,
        "with_log_co_spawn_print_exceptions":          False,
        "with_log_my_websocket":                       False,
        "with_my_websocket_read_end":                  False,
        "with_log_for_state_machine":                  False,
        "with_log_object_to_string_with_object_name":  False,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["boost"].header_only = True


    def requirements(self):
        self.requires("boost/1.85.0", force=True,transitive_headers=True)
        self.requires("durak/1.0.5", force=True)
        self.requires("confu_soci/[<1]",transitive_headers=True)
        self.requires("magic_enum/[>=0.9.5 <10]")
        self.requires("certify/cci.20201114", force=True,transitive_headers=True)
        self.requires("libsodium/1.0.18", force=True,transitive_headers=True)
        self.requires("confu_json/1.1.0", force=True,transitive_headers=True)
        self.requires("sml/1.1.11")
        self.requires("range-v3/0.12.0")
        self.requires("login_matchmaking_game_shared/0.0.0")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_CO_SPAWN_PRINT_EXCEPTIONS"]  = self.options.with_log_co_spawn_print_exceptions
        tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_MY_WEBSOCKET"]  = self.options.with_log_my_websocket
        tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_MY_WEBSOCKET_READ_END"]  = self.options.with_my_websocket_read_end
        tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_FOR_STATE_MACHINE"]  = self.options.with_log_for_state_machine
        tc.preprocessor_definitions["MATCHMAKING_PROXY_LOG_OBJECT_TO_STRING_WITH_OBJECT_NAME"]  = self.options.with_log_object_to_string_with_object_name
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
        self.cpp_info.libs = [self.name]
