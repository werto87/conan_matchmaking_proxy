from conans import ConanFile, tools
from conans.tools import check_min_cppstd
import os


class MatchmakingProxy(ConanFile):
    name = "matchmaking_proxy"
    homepage = "https://github.com/werto87/matchmaking_proxy"
    description = "used to login user and make a match. Then sends data to the user defined game server to start the game."
    topics = ("server", "login", "proxy", "matchmaking")
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "compiler"
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, "20")
        self.options["boost"].header_only = True

    def requirements(self):
        self.requires("range-v3/0.12.0@werto87/stable")
        self.requires("certify/0.0.1@werto87/stable")
        self.requires("boost/1.77.0")
        self.requires("confu_soci/0.2.0@werto87/stable")
        self.requires("libsodium/1.0.18")
        self.requires("confu_json/0.0.8@werto87/stable")
        self.requires("magic_enum/0.7.2")
        self.requires("catch2/2.13.7")
        self.requires("pipes/1.0.0")

    def source(self):
        if self.version != "latest":
            tools.get(**self.conan_data["sources"][self.version])
            extracted_dir = self.name + "-" + self.version
            os.rename(extracted_dir, self._source_subfolder)
        else:
            tools.get(url="https://github.com/werto87/matchmaking_proxy/archive/refs/heads/main.zip")
            extracted_dir = self.name +"-main"
            os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        # This should lead to an Include path like #include "include_folder/IncludeFile.hxx"
        self.copy("*.h*", dst="include/"+self.name,
                  src="source_subfolder/"+self.name)

    def package_id(self):
        self.info.header_only()
