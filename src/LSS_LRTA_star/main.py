from lss_lrta import lss_lrta_star, manhattan_distance
from search import SearchTreePQS
from validating import simple_test, hard_test, toy_test, base_test

if __name__ == '__main__':
    res = simple_test(lss_lrta_star, 1, manhattan_distance, SearchTreePQS, 10)
    #res = hard_test(lss_lrta_star, 1, manhattan_distance, SearchTreePQS, 20)
    #res = toy_test(lss_lrta_star, 0, manhattan_distance, SearchTreePQS, 100)
    #res = base_test(lss_lrta_star, 0, manhattan_distance, SearchTreePQS, 3)
