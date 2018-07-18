#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import ConfigParser


class ConfigFile:

    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser.ConfigParser()
        if os.path.exists(self.filename):
            self.config.read(self.filename)
        else:
            self.config.write(open(self.filename, "w"))

    def sync(self):
        self.config.write(open(self.filename, 'r+'))

    def __del__(self):
        self.config.write(open(self.filename, 'r+'))

    def __setattr__(self, name, value):
        if name not in self.__dict__:
            index = name.find('_')
            if index != -1:
                section = name[0:index]
                option = name[index+1:]
                sections = self.config.sections()
                if section not in sections:
                    self.config.add_section(section)
                self.config.set(section, option, value)
                return
        self.__dict__[name] = value

    def __getattr__(self, name):
        if name not in self.__dict__:
            try:
                index = name.find('_')
                if index == -1:
                    return None
                section = name[0:index]
                option = name[index+1:]
                return self.config.get(section, option)
            except:
                return None
        return self.__dict__[name]


if __name__ == "__main__":
    conf = ConfigFile('config.ini')

    conf.login_platform_uid = '2882303761517537982'
    print conf.login_platform_uid

    conf.login_channelName = 'Official'
    print conf.login_channelName

    conf.login_packageName = 'com.ushaqi.zhuishushenqi'
    print conf.login_packageName

    conf.login_promoterId = '200000107'
    print conf.login_promoterId

    conf.login_platform_token = 'V2_NRf3U65Cs_m90kTy6ZQQ-RQ0T0Qda8-1JTr2l_h5bfNGQKbj0_gOOTjXNOPfZpfQTPrcf2L_5xf8C63Gqk-Xx2iq0wvP0rfOlj96f6Q4rvGIlB7AQZa8FXdRfa1xEX9OmeLqWWY8hqG1uCfsRS1ZDQ'
    print conf.login_platform_token

    conf.login_platform_code = 'Xiaomi'
    print conf.login_platform_code

    conf.login_version = '2'
    print conf.login_version
