import re


def replace_command(content, name, n):
    # 定义正则表达式来匹配/audio{...}{...}的模式
    pattern = r'/' + name + '\{([^\}]+)\}\{([^\}]+)\}'

    # 使用re.sub进行替换，lambda函数用来选择第n个花括号里的内容
    replaced_content = re.sub(pattern, lambda m: m.group(n), content)

    return replaced_content


import unittest

class TestSort(unittest.TestCase):
    def setUp(self):
        pass

    def test_normal(self):
        text = "相比于/audio{二点零}{2.0}HTTP3.0最重要的升级是/audio{quick}{QUIC}协议"
        ans1 = "相比于二点零HTTP3.0最重要的升级是quick协议"
        ans2 = "相比于2.0HTTP3.0最重要的升级是QUIC协议"

        text2 = "对于HTTP\audio{二点零}{2.0}"
        ans21 = "对于HTTP\audio{二点零}{2.0}"

        self.assertEqual(replace_command(text, 'audio', 1), ans1)
        self.assertEqual(replace_command(text, 'audio', 2), ans2)
