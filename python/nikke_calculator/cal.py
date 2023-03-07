from math import ceil

# constants
REQUIRED = {
    'gold': 17412500,
    'exp': 208313700,
    'ball': 18000
}

BONUS = {
    'gold': {
        '1h': 32543,
        '2h': 65087,
        '8h': 260000,
        '12h': 390000,
        '24h': 781000,
    },
    'exp': {
        '1h': 359000,
        '2h': 718000,
        '8h': 2873000,
        '12h': 4309000,
        '24h': 8619000,
    },
    'ball': {
        '1h': 46,
        '2h': 93,
        '8h': 375,
        '12h': 563,
        '24h': 1126,
    },
}

RESOURCES_LIST = ['gold', 'exp', 'ball']

ALLOCATION_PRIORITY = [
    '24h', '12h', '8h', '2h', '1h'
]


def main():
    current = {
        'gold': 6808719,
        'exp': 110789524,
        'ball': 64841,
    }
    stock = {
        'gold': {
            '1h': 370,
            '2h': 101,
            '8h': 22,
            '12h': 4,
            '24h': 3,
        },
        'exp': {
            '1h': 1303,
            '2h': 36,
            '8h': 1,
            '12h': 6,
            '24h': 1,
        },
        'ball': {
            '1h': 868,
            '2h': 87,
            '8h': 3,
            '12h': 8,
            '24h': 3,
        },
    }

    member_number = 2
    use = {}
    for rsc in RESOURCES_LIST:
        gap = REQUIRED[rsc] * member_number - current[rsc]
        if gap <= 0:
            print(f'curren {rsc} is enough ^_^ ')
            continue

        use[rsc] = {}
        for item in ALLOCATION_PRIORITY:
            use[rsc][item] = min(
                ceil(gap / BONUS[rsc][item]), stock[rsc][item])
            gap -= use[rsc][item] * BONUS[rsc][item]
            if gap <= 0:
                break

        if (gap > 0):
            print(f'{rsc} is not enough >,<')
        else:
            for item in use[rsc]:
                print(f'{rsc} {item} needs: {use[rsc][item]}')


if __name__ == "__main__":
    main()
