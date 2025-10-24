from typing import List


def product_except_self(nums: List[int]):
    n = len(nums)
    results = []

    for i in range(n):
        product = 1
        for j in range(n):
            if i != j:
                product = product * nums[j]
        results.append(product)
    return results

if __name__ == "__main__":
    print(product_except_self([1,2,3,4]))
    print(product_except_self([5,2]))
    print(product_except_self([0, 3, 0]))