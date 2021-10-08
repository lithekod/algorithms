def is_prime(p):
    """
    Returns True if p is a prime

    This function uses Fermat's little theorem to quickly remove most
    candidates.
    """
    if p == 2:
        return True
    elif p <= 1 or p % 2 == 0 or 2**(p-1) % p != 1:
        return False
    return all(p % n != 0 for n in range(3,int(p ** 0.5 + 1),2))


def primelist(end):
    """ Primes in the range [0, end] """
    is_prime = [0, 0] + [1] * (end - 1)
    for i in range(int(len(is_prime)**.5 + 1)):
        if is_prime[i]:
            index_length = (end - i*i) // i + 1
            is_prime[i*i::i] = [0] * index_length

    return [n for n, p in enumerate(is_prime) if p]
