import hashlib

salt = 'fhsafsaf'


def get_md5(content):
    '''
    加密函数
    :param content: 要加密的内容
    :return: 加密后的内容
    '''
    md5 = hashlib.md5(salt.encode('utf-8'))
    md5.update(content.encode('utf-8'))
    return md5.hexdigest()
