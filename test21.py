from hashlib import sha1
import codecs
import base64
from Crypto.Cipher import AES
import binascii


# 求未知数，是到期日的校验位，根据校验规则计算
def Unknown_Number() -> int:
    Unknown_Number = 0
    number = "111116"  # 预设的数字
    weight = "731"  # 权重
    for i in range(0, len(number)):
        Unknown_Number += int(number[i]) * int(weight[i % 3])
    return Unknown_Number % 10  # 返回校验位


# 计算k_seed
def cal_Kseed() -> str:
    MRZ_information = "12345678<811101821111167"  # 护照信息
    H_information = sha1(MRZ_information.encode()).hexdigest()  # 使用SHA1进行哈希
    K_seed = H_information[0:32]  # 取哈希值的前32位作为K_seed
    return K_seed


def cal_Ka_Kb(K_seed):
    c = "00000001"
    d = K_seed + c
    H_d = sha1(codecs.decode(d, "hex")).hexdigest()  # 对K_seed进行哈希
    ka = H_d[0:16]  # 取前16位作为ka
    kb = H_d[16:32]  # 取后16位作为kb
    return ka, kb


# 对Ka和Kb分别进行奇偶校验，得到新的k1和k2
def Parity_Check(x):
    k_list = []
    a = bin(int(x, 16))[2:]  # 将16进制转为2进制
    for i in range(0, len(a), 8):
        # 7位一组分块，计算一个校验位，使1的个数为偶数
        if (a[i:i + 7].count("1")) % 2 == 0:
            k_list.append(a[i:i + 7])
            k_list.append('1')
        else:
            k_list.append(a[i:i + 7])
            k_list.append('0')
    k = hex(int(''.join(k_list), 2))  # 将2进制转为16进制
    return k


if __name__ == "__main__":
    K_seed = cal_Kseed()  # 计算K_seed
    ka, kb = cal_Ka_Kb(K_seed)  # 计算ka和kb
    k_1 = Parity_Check(ka)  # 对ka进行奇偶校验
    k_2 = Parity_Check(kb)  # 对kb进行奇偶校验
    key = k_1[2:] + k_2[2:]  # 合并k_1和k_2作为最终的密钥
    print(key)  # 输出密钥

    # 待解密的密文
    ciphertext = base64.b64decode(
        "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI")
    IV = '0' * 32  # 初始化向量

    # 使用AES进行解密
    m = AES.new(binascii.unhexlify(key), AES.MODE_CBC, binascii.unhexlify(IV)).decrypt(ciphertext)
    print(m)  # 输出解密后的明文