import rsa


def flashsigner_verify(message, signature, hash_method="SHA-256"):
    try:
        pubkey = bytearray.fromhex(signature[:520])
        e = pubkey[0:4]
        n = pubkey[4:]
        pub = rsa.PublicKey(int.from_bytes(n, "little"),
                            int.from_bytes(e, "little"))
        signature_ = bytearray.fromhex(signature[520:])
        compare_hash_method = hash_method

        hash_m = rsa.verify(message.encode(), signature_, pub)
        if hash_m == compare_hash_method:
            return True
        else:
            return False
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
    return False
