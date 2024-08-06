import yaml


class ConfigParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = None
        self.load_config()

    def load_config(self):
        """从YAML文件加载配置"""
        with open(self.config_file, 'r') as file:
            self.config_data = yaml.safe_load(file)

    def get_project(self):
        """获取项目名称"""
        return self.config_data.get('project', None)

    def get_script(self):
        """获取剧本"""
        return self.config_data.get('script', None)

    def get_video_file(self):
        """获取视频文件路径"""
        return self.config_data.get('video', None)

    def get_bigtitle(self):
        return self.config_data.get('bigtitle', None)

    def get_smalltitle(self):
        return self.config_data.get('smalltitle', None)

    def get_output_file(self):
        """获取输出文件路径"""
        return self.config_data.get('output', None)

    def get_bg_music(self):
        """获取背景音乐文件"""
        return self.config_data.get('bgmusic', None)

    def get_background_picture(self):
        """获取背景图片列表及其持续时间"""
        return self.config_data.get('bgpic', [])

    def pass_to_function(self, func):
        """将配置数据传递给其他函数"""
        if self.config_data:
            func(self.config_data)


# 示例使用
def use_config(config):
    print("项目名称:", config.get_project())
    print("视频文件:", config.get_video_file())
    print("输出文件:", config.get_output_file())
    print("背景音乐:", config.get_bg_music())
    print("背景图片信息:", config.get_background_picture())


# # 假设配置文件名为 config.yaml
# config_parser = ConfigParser('config.yaml')
# use_config(config_parser)  # 直接传递ConfigParser实例
